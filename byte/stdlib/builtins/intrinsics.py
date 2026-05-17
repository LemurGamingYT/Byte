from llvmlite import ir

from byte.intrinsics import intrinsic, IntrinsicLib, IntrinsicCallContext
from byte.llvm_extensions import NULL, llint
from byte import ast


class intrinsics(IntrinsicLib):
    def init(self):
        int_type = self.file.type_map.get('int')
        bool_type = self.file.type_map.get('bool')
        string_type = self.file.type_map.get('string')
        pointer_type = self.file.type_map.get('pointer')
        IOFile_type = self.file.type_map.get('IOFile')
        
        @intrinsic(self, params=[ast.Param(ast.Position(), string_type, 's')])
        def _print_string(ctx: IntrinsicCallContext):
            printf = ctx.module.registry.get('printf')

            fmt = ctx.module.try_get_global('string_fmt', lambda: ctx.module.global_string('%.*s\n', 'string_fmt'))
            ptr = ctx.builder.first_elem(fmt, 'string_fmt_ptr')
            s_ptr = ctx.call('string.ptr', ctx.args)
            s_length = ctx.call('string.length', ctx.args)
            ctx.builder.call(printf, [ptr, s_length, s_ptr])

        @intrinsic(self, params=[ast.Param(ast.Position(), string_type, 's')])
        def _print_literal(ctx: IntrinsicCallContext):
            printf = ctx.module.registry.get('printf')

            fmt = ctx.module.try_get_global('string_lit_fmt', lambda: ctx.module.global_string('%.*s', 'string_lit_fmt'))
            ptr = ctx.builder.first_elem(fmt, 'string_lit_fmt_ptr')
            s_ptr = ctx.call('string.ptr', ctx.args)
            s_length = ctx.call('string.length', ctx.args)
            ctx.builder.call(printf, [ptr, s_length, s_ptr])

        @intrinsic(self, string_type, [
            ast.Param(ast.Position(), pointer_type, 'ptr'), ast.Param(ast.Position(), int_type, 'length'),
            ast.Param(ast.Position(), bool_type, 'is_allocated')
        ])
        def _string_struct(ctx: IntrinsicCallContext):
            string_struct = ctx.module.context.get_identified_type('string')

            ptr = ctx.arg(0)
            length = ctx.arg(1)
            is_allocated = ctx.arg(2)
            return ctx.builder.struct(string_struct, [ptr, length, is_allocated], ctx.name)

        @intrinsic(self, pointer_type, [ast.Param(ast.Position(), int_type, 'length')])
        def _buffer(ctx: IntrinsicCallContext):
            length = ctx.arg(0)
            if not isinstance(length, ir.Constant):
                ctx.pos.comptime_error(self.file, 'expected literal integer')
            
            buf = ctx.module.global_buffer(ir.IntType(8), length.constant, ctx.module.get_unique_name('buffer'))
            return ctx.builder.first_elem(buf, ctx.name)

        @intrinsic(self, IOFile_type, [ast.Param(ast.Position(), int_type, 'fd'), ast.Param(ast.Position(), pointer_type, 'mode')])
        def _get_fd(ctx: IntrinsicCallContext):
            fd = ctx.arg(0)
            mode = ctx.arg(1)
            
            if ctx.file.target == ast.Target.WINDOWS:
                acrt_iob_func = ctx.module.registry.get('acrt_iob_func')
                return ctx.builder.call(acrt_iob_func, [fd], 'acrt_iob_func')
            else:
                fdopen = ctx.module.registry.get('fdopen')
                return ctx.builder.call(fdopen, [fd, mode], 'fdopen')

        @intrinsic(self, params=[ast.Param(ast.Position(), string_type, 'msg')])
        def _error(ctx: IntrinsicCallContext):
            fprintf = ctx.module.registry.get('fprintf')
            exit = ctx.module.registry.get('exit')

            write_mode = ctx.module.try_get_global('write_mode', lambda: ctx.module.global_string('w', 'write_mode'))
            write_mode_ptr = ctx.builder.first_elem(write_mode, 'write_mode.ptr')
            stderr = ctx.call('get_fd', [ast.Arg(ctx.pos, int_type, llint(0)), ast.Arg(ctx.pos, pointer_type, write_mode_ptr)])
            fmt = ctx.module.try_get_global('error_fmt', lambda: ctx.module.global_string('error: %.*s\n', 'error_fmt'))
            ptr = ctx.builder.first_elem(fmt, 'error_fmt_ptr')
            msg_ptr = ctx.call('string.ptr', ctx.args)
            msg_length = ctx.call('string.length', ctx.args)
            ctx.builder.call(fprintf, [stderr, ptr, msg_length, msg_ptr])
            ctx.builder.call(exit, [llint(1)])
            ctx.builder.unreachable()
        
        @intrinsic(self, pointer_type)
        def _null(_: IntrinsicCallContext):
            return NULL()
