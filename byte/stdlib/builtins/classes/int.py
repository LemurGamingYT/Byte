from llvmlite import ir

from byte.intrinsics import intrinsic, IntrinsicClass, IntrinsicCallContext
from byte.llvm_extensions import llint, max_int, min_int
from byte import ast


class int(IntrinsicClass):
    def init(self):
        int_type = self.file.type_map.get('int')
        float_type = self.file.type_map.get('float')
        string_type = self.file.type_map.get('string')
        
        @intrinsic(self, int_type, flags=ast.FunctionFlags(static=True, property=True))
        def _max(_: IntrinsicCallContext):
            return llint(max_int())

        @intrinsic(self, int_type, flags=ast.FunctionFlags(static=True, property=True))
        def _min(_: IntrinsicCallContext):
            return llint(min_int())

        @intrinsic(self, string_type, [ast.Param(ast.Position(), int_type, 'self')], flags=ast.FunctionFlags(method=True))
        def _to_string(ctx: IntrinsicCallContext):
            snprintf = ctx.module.registry.get('snprintf')
            
            int_fmt = ctx.module.try_get_global('int_fmt', lambda: ctx.module.global_string('%d', 'int_fmt'))
            int_fmt_ptr = ctx.builder.first_elem(int_fmt, 'int_fmt_ptr')
            
            BUF_SIZE = 16
            int_buf = ctx.builder.first_elem(
                ctx.module.global_buffer(ir.IntType(8), BUF_SIZE, ctx.module.get_unique_name('int_buf')),
                'int_buf_ptr'
            )

            s = ctx.arg(0)
            written = ctx.builder.call(snprintf, [int_buf, llint(BUF_SIZE), int_fmt_ptr, s], 'written')
            # TODO: check if snprintf failed

            return ctx.call('string.new', [
                ast.Arg(ctx.pos, ctx.file.type_map.get('pointer'), int_buf),
                ast.Arg(ctx.pos, ctx.file.type_map.get('int'), written),
                ast.Arg(ctx.pos, ctx.file.type_map.get('bool'), llint(0, 1))
            ])

        @intrinsic(self, float_type, [ast.Param(ast.Position(), int_type, 'self')], flags=ast.FunctionFlags(method=True))
        def _to_float(ctx: IntrinsicCallContext):
            return ctx.builder.sitofp(ctx.arg(0), ir.FloatType(), ctx.name)
