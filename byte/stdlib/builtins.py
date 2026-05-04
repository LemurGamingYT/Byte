from llvmlite import ir

from byte.intrinsics import IntrinsicLib, IntrinsicCallContext, intrinsic, intrinsic_op
from byte.llvm_extensions import NULL, llint
from byte import ast


class builtins(IntrinsicLib):
    def init(self):
        int_type = self.file.type_map.get('int')
        float_type = self.file.type_map.get('float')
        bool_type = self.file.type_map.get('bool')
        string_type = self.file.type_map.get('string')
        pointer_type = self.file.type_map.get('pointer')
        any_type = self.file.type_map.get('any')
        Math_type = self.file.type_map.get('Math')
        System_type = self.file.type_map.get('System')

        @intrinsic_op(self, '+', int_type, int_type, int_type)
        def add_ints(ctx: IntrinsicCallContext):
            a, b = ctx.args
            return ctx.builder.add(a, b, ctx.name)

        @intrinsic_op(self, '-', int_type, int_type, int_type)
        def sub_ints(ctx: IntrinsicCallContext):
            a, b = ctx.args
            return ctx.builder.sub(a, b, ctx.name)

        @intrinsic_op(self, '*', int_type, int_type, int_type)
        def mul_ints(ctx: IntrinsicCallContext):
            a, b = ctx.args
            return ctx.builder.mul(a, b, ctx.name)

        @intrinsic_op(self, '/', int_type, int_type, int_type)
        def div_ints(ctx: IntrinsicCallContext):
            a, b = ctx.args
            return ctx.builder.sdiv(a, b, ctx.name)

        @intrinsic_op(self, '%', int_type, int_type, int_type)
        def mod_ints(ctx: IntrinsicCallContext):
            a, b = ctx.args
            return ctx.builder.srem(a, b, ctx.name)

        @intrinsic_op(self, '==', bool_type, int_type, int_type)
        def eq_ints(ctx: IntrinsicCallContext):
            a, b = ctx.args
            return ctx.builder.icmp_signed('==', a, b, ctx.name)

        @intrinsic_op(self, '!=', bool_type, int_type, int_type)
        def neq_ints(ctx: IntrinsicCallContext):
            a, b = ctx.args
            return ctx.builder.icmp_signed('!=', a, b, ctx.name)

        @intrinsic_op(self, '<', bool_type, int_type, int_type)
        def lt_ints(ctx: IntrinsicCallContext):
            a, b = ctx.args
            return ctx.builder.icmp_signed('<', a, b, ctx.name)

        @intrinsic_op(self, '>', bool_type, int_type, int_type)
        def gt_ints(ctx: IntrinsicCallContext):
            a, b = ctx.args
            return ctx.builder.icmp_signed('>', a, b, ctx.name)

        @intrinsic_op(self, '<=', bool_type, int_type, int_type)
        def lte_ints(ctx: IntrinsicCallContext):
            a, b = ctx.args
            return ctx.builder.icmp_signed('<=', a, b, ctx.name)

        @intrinsic_op(self, '>=', bool_type, int_type, int_type)
        def gte_ints(ctx: IntrinsicCallContext):
            a, b = ctx.args
            return ctx.builder.icmp_signed('>=', a, b, ctx.name)

        @intrinsic_op(self, '+', float_type, float_type, float_type)
        def add_floats(ctx: IntrinsicCallContext):
            a, b = ctx.args
            return ctx.builder.fadd(a, b, ctx.name)

        @intrinsic_op(self, '-', float_type, float_type, float_type)
        def sub_floats(ctx: IntrinsicCallContext):
            a, b = ctx.args
            return ctx.builder.fsub(a, b, ctx.name)

        @intrinsic_op(self, '*', float_type, float_type, float_type)
        def mul_floats(ctx: IntrinsicCallContext):
            a, b = ctx.args
            return ctx.builder.fmul(a, b, ctx.name)

        @intrinsic_op(self, '/', float_type, float_type, float_type)
        def div_floats(ctx: IntrinsicCallContext):
            a, b = ctx.args
            return ctx.builder.fdiv(a, b, ctx.name)

        @intrinsic_op(self, '%', float_type, float_type, float_type)
        def mod_floats(ctx: IntrinsicCallContext):
            a, b = ctx.args
            return ctx.builder.frem(a, b, ctx.name)

        @intrinsic_op(self, '==', bool_type, float_type, float_type)
        def eq_floats(ctx: IntrinsicCallContext):
            a, b = ctx.args
            return ctx.builder.fcmp_ordered('==', a, b, ctx.name)

        @intrinsic_op(self, '!=', bool_type, float_type, float_type)
        def neq_floats(ctx: IntrinsicCallContext):
            a, b = ctx.args
            return ctx.builder.fcmp_ordered('!=', a, b, ctx.name)

        @intrinsic_op(self, '<', bool_type, float_type, float_type)
        def lt_floats(ctx: IntrinsicCallContext):
            a, b = ctx.args
            return ctx.builder.fcmp_ordered('<', a, b, ctx.name)

        @intrinsic_op(self, '>', bool_type, float_type, float_type)
        def gt_floats(ctx: IntrinsicCallContext):
            a, b = ctx.args
            return ctx.builder.fcmp_ordered('>', a, b, ctx.name)

        @intrinsic_op(self, '<=', bool_type, float_type, float_type)
        def lte_floats(ctx: IntrinsicCallContext):
            a, b = ctx.args
            return ctx.builder.fcmp_ordered('<=', a, b, ctx.name)

        @intrinsic_op(self, '>=', bool_type, float_type, float_type)
        def gte_floats(ctx: IntrinsicCallContext):
            a, b = ctx.args
            return ctx.builder.fcmp_ordered('>=', a, b, ctx.name)

        @intrinsic_op(self, '==', bool_type, bool_type, bool_type)
        def eq_bools(ctx: IntrinsicCallContext):
            a, b = ctx.args
            return ctx.builder.icmp_signed('==', a, b, ctx.name)

        @intrinsic_op(self, '!=', bool_type, bool_type, bool_type)
        def neq_bools(ctx: IntrinsicCallContext):
            a, b = ctx.args
            return ctx.builder.icmp_signed('!=', a, b, ctx.name)

        @intrinsic_op(self, '&&', bool_type, bool_type, bool_type)
        def and_bools(ctx: IntrinsicCallContext):
            a, b = ctx.args
            return ctx.builder.and_(a, b, ctx.name)

        @intrinsic_op(self, '||', bool_type, bool_type, bool_type)
        def or_bools(ctx: IntrinsicCallContext):
            a, b = ctx.args
            return ctx.builder.or_(a, b, ctx.name)

        @intrinsic_op(self, '!', bool_type, bool_type)
        def not_bool(ctx: IntrinsicCallContext):
            a, *_ = ctx.args
            return ctx.builder.not_(a, ctx.name)

        @intrinsic_op(self, '+', pointer_type, pointer_type, int_type)
        def offset_ptr(ctx: IntrinsicCallContext):
            a, b = ctx.args
            return ctx.builder.gep(a, [b], True, ctx.name)

        @intrinsic_op(self, '==', bool_type, pointer_type, pointer_type)
        def eq_ptrs(ctx: IntrinsicCallContext):
            a, b = ctx.args
            return ctx.builder.icmp_signed('==', a, b, ctx.name)

        @intrinsic_op(self, '!=', bool_type, pointer_type, pointer_type)
        def neq_ptrs(ctx: IntrinsicCallContext):
            a, b = ctx.args
            return ctx.builder.icmp_signed('!=', a, b, ctx.name)

        @intrinsic(self, params=[ast.Param(ast.Position(), string_type, 's')])
        def _print_string(ctx: IntrinsicCallContext):
            printf = ctx.module.registry.get('printf')

            s, *_ = ctx.args
            fmt = ctx.module.try_get_global('string_fmt', lambda: ctx.module.global_string('%.*s\n', 'string_fmt'))
            ptr = ctx.builder.first_elem(fmt, 'string_fmt_ptr')
            s_ptr = ctx.builder.extract_value(s, 0, 's_ptr')
            s_length = ctx.builder.extract_value(s, 1, 's_length')
            ctx.builder.call(printf, [ptr, s_length, s_ptr])

        @intrinsic(self, params=[ast.Param(ast.Position(), string_type, 's')])
        def _print_literal(ctx: IntrinsicCallContext):
            printf = ctx.module.registry.get('printf')

            s, *_ = ctx.args
            fmt = ctx.module.try_get_global('string_lit_fmt', lambda: ctx.module.global_string('%.*s', 'string_lit_fmt'))
            ptr = ctx.builder.first_elem(fmt, 'string_lit_fmt_ptr')
            s_ptr = ctx.builder.extract_value(s, 0, 's_ptr')
            s_length = ctx.builder.extract_value(s, 1, 's_length')
            ctx.builder.call(printf, [ptr, s_length, s_ptr])

        @intrinsic(self, string_type, [
            ast.Param(ast.Position(), pointer_type, 'ptr'), ast.Param(ast.Position(), int_type, 'length'),
            ast.Param(ast.Position(), bool_type, 'is_allocated')
        ])
        def _string_struct(ctx: IntrinsicCallContext):
            string_struct = ctx.module.context.get_identified_type('string')
            return ctx.builder.struct(string_struct, ctx.args, ctx.name)

        @intrinsic(self, pointer_type, [ast.Param(ast.Position(), int_type, 'length')])
        def _buffer(ctx: IntrinsicCallContext):
            length, *_ = ctx.args
            if not isinstance(length, ir.Constant):
                ctx.pos.comptime_error(self.file, 'expected literal integer')
            
            buf = ctx.module.global_buffer(ir.IntType(8), length.constant, ctx.module.get_unique_name('buffer'))
            return ctx.builder.first_elem(buf, ctx.name)

        @intrinsic(self, params=[ast.Param(ast.Position(), string_type, 'msg')])
        def _error(ctx: IntrinsicCallContext):
            acrt_iob_func = ctx.module.registry.get('acrt_iob_func')
            fprintf = ctx.module.registry.get('fprintf')
            exit = ctx.module.registry.get('exit')
            
            msg, *_ = ctx.args
            stderr = ctx.builder.call(acrt_iob_func, [llint(2)], 'stderr')
            fmt = ctx.module.try_get_global('error_fmt', lambda: ctx.module.global_string('error: %.*s\n', 'error_fmt'))
            ptr = ctx.builder.first_elem(fmt, 'error_fmt_ptr')
            s_ptr = ctx.builder.extract_value(msg, 0, 's_ptr')
            s_length = ctx.builder.extract_value(msg, 1, 's_length')
            ctx.builder.call(fprintf, [stderr, ptr, s_length, s_ptr])
            ctx.builder.call(exit, [llint(1)])
            ctx.builder.unreachable()
        
        @intrinsic(self, pointer_type)
        def _null(_: IntrinsicCallContext):
            return NULL()
