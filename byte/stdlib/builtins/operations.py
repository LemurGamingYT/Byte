from byte.intrinsics import intrinsic_op, IntrinsicLib, IntrinsicCallContext


class operations(IntrinsicLib):
    def init(self):
        int_type = self.file.type_map.get('int')
        float_type = self.file.type_map.get('float')
        bool_type = self.file.type_map.get('bool')
        pointer_type = self.file.type_map.get('pointer')

        @intrinsic_op(self, '+', int_type, int_type, int_type)
        def add_ints(ctx: IntrinsicCallContext):
            a = ctx.arg(0)
            b = ctx.arg(1)
            return ctx.builder.add(a, b, ctx.name)

        @intrinsic_op(self, '-', int_type, int_type, int_type)
        def sub_ints(ctx: IntrinsicCallContext):
            a = ctx.arg(0)
            b = ctx.arg(1)
            return ctx.builder.sub(a, b, ctx.name)

        @intrinsic_op(self, '*', int_type, int_type, int_type)
        def mul_ints(ctx: IntrinsicCallContext):
            a = ctx.arg(0)
            b = ctx.arg(1)
            return ctx.builder.mul(a, b, ctx.name)

        @intrinsic_op(self, '/', int_type, int_type, int_type)
        def div_ints(ctx: IntrinsicCallContext):
            a = ctx.arg(0)
            b = ctx.arg(1)
            return ctx.builder.sdiv(a, b, ctx.name)

        @intrinsic_op(self, '%', int_type, int_type, int_type)
        def mod_ints(ctx: IntrinsicCallContext):
            a = ctx.arg(0)
            b = ctx.arg(1)
            return ctx.builder.srem(a, b, ctx.name)

        @intrinsic_op(self, '==', bool_type, int_type, int_type)
        def eq_ints(ctx: IntrinsicCallContext):
            a = ctx.arg(0)
            b = ctx.arg(1)
            return ctx.builder.icmp_signed('==', a, b, ctx.name)

        @intrinsic_op(self, '!=', bool_type, int_type, int_type)
        def neq_ints(ctx: IntrinsicCallContext):
            a = ctx.arg(0)
            b = ctx.arg(1)
            return ctx.builder.icmp_signed('!=', a, b, ctx.name)

        @intrinsic_op(self, '<', bool_type, int_type, int_type)
        def lt_ints(ctx: IntrinsicCallContext):
            a = ctx.arg(0)
            b = ctx.arg(1)
            return ctx.builder.icmp_signed('<', a, b, ctx.name)

        @intrinsic_op(self, '>', bool_type, int_type, int_type)
        def gt_ints(ctx: IntrinsicCallContext):
            a = ctx.arg(0)
            b = ctx.arg(1)
            return ctx.builder.icmp_signed('>', a, b, ctx.name)

        @intrinsic_op(self, '<=', bool_type, int_type, int_type)
        def lte_ints(ctx: IntrinsicCallContext):
            a = ctx.arg(0)
            b = ctx.arg(1)
            return ctx.builder.icmp_signed('<=', a, b, ctx.name)

        @intrinsic_op(self, '>=', bool_type, int_type, int_type)
        def gte_ints(ctx: IntrinsicCallContext):
            a = ctx.arg(0)
            b = ctx.arg(1)
            return ctx.builder.icmp_signed('>=', a, b, ctx.name)

        @intrinsic_op(self, '-', int_type, int_type)
        def neg_int(ctx: IntrinsicCallContext):
            a = ctx.arg(0)
            return ctx.builder.neg(a, ctx.name)

        @intrinsic_op(self, '+', float_type, float_type, float_type)
        def add_floats(ctx: IntrinsicCallContext):
            a = ctx.arg(0)
            b = ctx.arg(1)
            return ctx.builder.fadd(a, b, ctx.name)

        @intrinsic_op(self, '-', float_type, float_type, float_type)
        def sub_floats(ctx: IntrinsicCallContext):
            a = ctx.arg(0)
            b = ctx.arg(1)
            return ctx.builder.fsub(a, b, ctx.name)

        @intrinsic_op(self, '*', float_type, float_type, float_type)
        def mul_floats(ctx: IntrinsicCallContext):
            a = ctx.arg(0)
            b = ctx.arg(1)
            return ctx.builder.fmul(a, b, ctx.name)

        @intrinsic_op(self, '/', float_type, float_type, float_type)
        def div_floats(ctx: IntrinsicCallContext):
            a = ctx.arg(0)
            b = ctx.arg(1)
            return ctx.builder.fdiv(a, b, ctx.name)

        @intrinsic_op(self, '%', float_type, float_type, float_type)
        def mod_floats(ctx: IntrinsicCallContext):
            a = ctx.arg(0)
            b = ctx.arg(1)
            return ctx.builder.frem(a, b, ctx.name)

        @intrinsic_op(self, '==', bool_type, float_type, float_type)
        def eq_floats(ctx: IntrinsicCallContext):
            a = ctx.arg(0)
            b = ctx.arg(1)
            return ctx.builder.fcmp_ordered('==', a, b, ctx.name)

        @intrinsic_op(self, '!=', bool_type, float_type, float_type)
        def neq_floats(ctx: IntrinsicCallContext):
            a = ctx.arg(0)
            b = ctx.arg(1)
            return ctx.builder.fcmp_ordered('!=', a, b, ctx.name)

        @intrinsic_op(self, '<', bool_type, float_type, float_type)
        def lt_floats(ctx: IntrinsicCallContext):
            a = ctx.arg(0)
            b = ctx.arg(1)
            return ctx.builder.fcmp_ordered('<', a, b, ctx.name)

        @intrinsic_op(self, '>', bool_type, float_type, float_type)
        def gt_floats(ctx: IntrinsicCallContext):
            a = ctx.arg(0)
            b = ctx.arg(1)
            return ctx.builder.fcmp_ordered('>', a, b, ctx.name)

        @intrinsic_op(self, '<=', bool_type, float_type, float_type)
        def lte_floats(ctx: IntrinsicCallContext):
            a = ctx.arg(0)
            b = ctx.arg(1)
            return ctx.builder.fcmp_ordered('<=', a, b, ctx.name)

        @intrinsic_op(self, '>=', bool_type, float_type, float_type)
        def gte_floats(ctx: IntrinsicCallContext):
            a = ctx.arg(0)
            b = ctx.arg(1)
            return ctx.builder.fcmp_ordered('>=', a, b, ctx.name)

        @intrinsic_op(self, '-', float_type, float_type)
        def neg_float(ctx: IntrinsicCallContext):
            a = ctx.arg(0)
            return ctx.builder.fneg(a, ctx.name)

        @intrinsic_op(self, '==', bool_type, bool_type, bool_type)
        def eq_bools(ctx: IntrinsicCallContext):
            a = ctx.arg(0)
            b = ctx.arg(1)
            return ctx.builder.icmp_signed('==', a, b, ctx.name)

        @intrinsic_op(self, '!=', bool_type, bool_type, bool_type)
        def neq_bools(ctx: IntrinsicCallContext):
            a = ctx.arg(0)
            b = ctx.arg(1)
            return ctx.builder.icmp_signed('!=', a, b, ctx.name)

        @intrinsic_op(self, '&&', bool_type, bool_type, bool_type)
        def and_bools(ctx: IntrinsicCallContext):
            a = ctx.arg(0)
            b = ctx.arg(1)
            return ctx.builder.and_(a, b, ctx.name)

        @intrinsic_op(self, '||', bool_type, bool_type, bool_type)
        def or_bools(ctx: IntrinsicCallContext):
            a = ctx.arg(0)
            b = ctx.arg(1)
            return ctx.builder.or_(a, b, ctx.name)

        @intrinsic_op(self, '!', bool_type, bool_type)
        def not_bool(ctx: IntrinsicCallContext):
            a = ctx.arg(0)
            return ctx.builder.not_(a, ctx.name)

        @intrinsic_op(self, '+', pointer_type, pointer_type, int_type)
        def offset_ptr(ctx: IntrinsicCallContext):
            a = ctx.arg(0)
            b = ctx.arg(1)
            return ctx.builder.gep(a, [b], True, ctx.name)

        @intrinsic_op(self, '==', bool_type, pointer_type, pointer_type)
        def eq_ptrs(ctx: IntrinsicCallContext):
            a = ctx.arg(0)
            b = ctx.arg(1)
            return ctx.builder.icmp_signed('==', a, b, ctx.name)

        @intrinsic_op(self, '!=', bool_type, pointer_type, pointer_type)
        def neq_ptrs(ctx: IntrinsicCallContext):
            a = ctx.arg(0)
            b = ctx.arg(1)
            return ctx.builder.icmp_signed('!=', a, b, ctx.name)
