from math import pi, e

from llvmlite import ir

from byte.intrinsics import IntrinsicLib, IntrinsicCallContext, intrinsic, intrinsic_op
from byte.llvm_extensions import NULL, llint, Registry, max_int, min_int
from byte import ast


class builtins(IntrinsicLib):
    def init(self):
        int_type = self.file.type_map.get('int')
        float_type = self.file.type_map.get('float')
        bool_type = self.file.type_map.get('bool')
        string_type = self.file.type_map.get('string')
        pointer_type = self.file.type_map.get('pointer')
        Math_type = self.file.type_map.get('Math')
        System_type = self.file.type_map.get('System')

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

        @intrinsic(self, params=[ast.Param(ast.Position(), string_type, 'msg')])
        def _error(ctx: IntrinsicCallContext):
            acrt_iob_func = ctx.module.registry.get('acrt_iob_func')
            fprintf = ctx.module.registry.get('fprintf')
            exit = ctx.module.registry.get('exit')
            
            stderr = ctx.builder.call(acrt_iob_func, [llint(2)], 'stderr')
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

        @intrinsic(self, int_type, flags=ast.FunctionFlags(static=True, property=True), override_name=f'{int_type}.max')
        def int_max(_: IntrinsicCallContext):
            return llint(max_int())

        @intrinsic(self, int_type, flags=ast.FunctionFlags(static=True, property=True), override_name=f'{int_type}.min')
        def int_min(_: IntrinsicCallContext):
            return llint(min_int())

        @intrinsic(
            self, string_type, [ast.Param(ast.Position(), int_type, 'self')], flags=ast.FunctionFlags(method=True),
            override_name=f'{int_type}.to_string'
        )
        def int_to_string(ctx: IntrinsicCallContext):
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

        @intrinsic(
            self, float_type, [ast.Param(ast.Position(), int_type, 'self')], flags=ast.FunctionFlags(method=True),
            override_name=f'{int_type}.to_float'
        )
        def int_to_float(ctx: IntrinsicCallContext):
            return ctx.builder.sitofp(ctx.arg(0), ir.FloatType(), ctx.name)

        # @intrinsic(self, float_type, flags=ast.FunctionFlags(static=True, property=True), override_name=f'{float_type}.max')
        # def float_max(_: IntrinsicCallContext):
        #     return ir.Constant(ir.FloatType(), 3.402823e+38)

        # @intrinsic(self, float_type, flags=ast.FunctionFlags(static=True, property=True), override_name=f'{float_type}.min')
        # def float_min(_: IntrinsicCallContext):
        #     return ir.Constant(ir.FloatType(), 1.175494e-38)

        @intrinsic(
            self, string_type, [ast.Param(ast.Position(), float_type, 'self')], flags=ast.FunctionFlags(method=True),
            override_name=f'{float_type}.to_string'
        )
        def float_to_string(ctx: IntrinsicCallContext):
            snprintf = ctx.module.registry.get('snprintf')
            
            float_fmt = ctx.module.try_get_global('float_fmt', lambda: ctx.module.global_string('%f', 'float_fmt'))
            float_fmt_ptr = ctx.builder.first_elem(float_fmt, 'float_fmt_ptr')

            s = ctx.arg(0)
            f_double = ctx.builder.fpext(s, ir.DoubleType(), 'f_double')
            
            BUF_SIZE = 64
            float_buf = ctx.builder.first_elem(
                ctx.module.global_buffer(ir.IntType(8), BUF_SIZE, ctx.module.get_unique_name('float_buf')),
                'float_buf'
            )

            written = ctx.builder.call(snprintf, [float_buf, llint(BUF_SIZE), float_fmt_ptr, f_double], 'written')
            return ctx.call('string.new', [
                ast.Arg(ctx.pos, ctx.file.type_map.get('pointer'), float_buf),
                ast.Arg(ctx.pos, ctx.file.type_map.get('int'), written),
                ast.Arg(ctx.pos, ctx.file.type_map.get('bool'), llint(0, 1))
            ])

        @intrinsic(
            self, int_type, [ast.Param(ast.Position(), float_type, 'self')], flags=ast.FunctionFlags(method=True),
            override_name=f'{float_type}.to_int'
        )
        def float_to_int(ctx: IntrinsicCallContext):
            return ctx.builder.fptosi(ctx.arg(0), ir.IntType(32), ctx.name)

        @intrinsic(
            self, pointer_type, [ast.Param(ast.Position(), string_type, 'self')], flags=ast.FunctionFlags(property=True),
            override_name=f'{string_type}.ptr'
        )
        def string_ptr(ctx: IntrinsicCallContext):
            s = ctx.arg(0)
            return ctx.builder.extract_value(s, 0, ctx.name)

        @intrinsic(
            self, int_type, [ast.Param(ast.Position(), string_type, 'self')], flags=ast.FunctionFlags(property=True),
            override_name=f'{string_type}.length'
        )
        def string_length(ctx: IntrinsicCallContext):
            s = ctx.arg(0)
            return ctx.builder.extract_value(s, 1, ctx.name)

        @intrinsic(
            self, bool_type, [ast.Param(ast.Position(), string_type, 'self')], flags=ast.FunctionFlags(property=True),
            override_name=f'{string_type}.is_allocated'
        )
        def string_is_allocated(ctx: IntrinsicCallContext):
            s = ctx.arg(0)
            return ctx.builder.extract_value(s, 2, ctx.name)

        @intrinsic(
            self, string_type, [ast.Param(ast.Position(), string_type, 'self')], flags=ast.FunctionFlags(method=True),
            override_name=f'{string_type}.to_string'
        )
        def string_to_string(ctx: IntrinsicCallContext):
            ptr = ctx.call('string.ptr', ctx.args)
            length = ctx.call('string.length', ctx.args)
            return ctx.call('string.new.pointer.int', [
                ast.Arg(ctx.pos, ctx.file.type_map.get('pointer'), ptr),
                ast.Arg(ctx.pos, ctx.file.type_map.get('int'), length)
            ])

        @intrinsic(
            self, string_type, [ast.Param(ast.Position(), bool_type, 'self')], flags=ast.FunctionFlags(method=True),
            override_name=f'{bool_type}.to_string'
        )
        def bool_to_string(ctx: IntrinsicCallContext):
            true_str = ctx.module.global_string('true', ctx.module.get_unique_name('true_str'))
            false_str = ctx.module.global_string('false', ctx.module.get_unique_name('false_str'))
            true_ptr = ctx.builder.first_elem(true_str, 'true_ptr')
            false_ptr = ctx.builder.first_elem(false_str, 'false_ptr')

            b = ctx.arg(0)
            ptr = ctx.builder.select(b, true_ptr, false_ptr, 'b_ptr')
            length = ctx.builder.select(b, llint(4), llint(5), 'b_length')
            return ctx.call('string.new', [
                ast.Arg(ctx.pos, ctx.file.type_map.get('pointer'), ptr),
                ast.Arg(ctx.pos, ctx.file.type_map.get('int'), length),
                ast.Arg(ctx.pos, ctx.file.type_map.get('bool'), llint(0, 1))
            ])

        @intrinsic(self, float_type, flags=ast.FunctionFlags(static=True, property=True), override_name=f'{Math_type}.pi')
        def Math_pi(_: IntrinsicCallContext):
            return ir.Constant(ir.FloatType(), pi)

        @intrinsic(self, float_type, flags=ast.FunctionFlags(static=True, property=True), override_name=f'{Math_type}.e')
        def Math_e(_: IntrinsicCallContext):
            return ir.Constant(ir.FloatType(), e)

        @intrinsic(
            self, int_type, [ast.Param(ast.Position(), float_type, 'x')], flags=ast.FunctionFlags(static=True, method=True),
            override_name=f'{Math_type}.floor'
        )
        def Math_floor(ctx: IntrinsicCallContext):
            floor = ctx.module.registry.get('floor')
            x = ctx.arg(0)
            res_float = ctx.builder.call(floor, [x], 'res_float')
            return ctx.builder.fptosi(res_float, ir.IntType(32), 'res')

        @intrinsic(
            self, int_type, [ast.Param(ast.Position(), float_type, 'x')], flags=ast.FunctionFlags(static=True, method=True),
            override_name=f'{Math_type}.ceil'
        )
        def Math_ceil(ctx: IntrinsicCallContext):
            ceil = ctx.module.registry.get('ceil')
            x = ctx.arg(0)
            res_float = ctx.builder.call(ceil, [x], 'res_float')
            return ctx.builder.fptosi(res_float, ir.IntType(32), 'res')

        @intrinsic(
            self, string_type, flags=ast.FunctionFlags(static=True, property=True), override_name=f'{System_type}.os'
        )
        def System_os(ctx: IntrinsicCallContext):
            text = self.file.target.name.title()
            os_name = ctx.module.global_string(text, 'os_name')
            os_name_ptr = ctx.builder.first_elem(os_name, 'os_name_ptr')
            return ctx.call('string.new', [
                ast.Arg(ctx.pos, ctx.file.type_map.get('pointer'), os_name_ptr),
                ast.Arg(ctx.pos, ctx.file.type_map.get('int'), llint(len(text))),
                ast.Arg(ctx.pos, ctx.file.type_map.get('bool'), llint(0, 1))
            ])

        @intrinsic(
            self, params=[ast.Param(ast.Position(), int_type, 'duration')], flags=ast.FunctionFlags(static=True, method=True),
            override_name=f'{System_type}.sleep'
        )
        def System_sleep(ctx: IntrinsicCallContext):
            duration = ctx.arg(0)
            if self.file.target == ast.Target.WINDOWS:
                Sleep = ctx.module.registry.get('Sleep')
                ctx.builder.call(Sleep, [duration])
            else:
                usleep = ctx.module.registry.get('usleep')
                duration_microseconds = ctx.builder.mul(duration, llint(1000), 'duration_microseconds')
                ctx.builder.call(usleep, [duration_microseconds])

        @intrinsic(self, int_type, flags=ast.FunctionFlags(static=True, property=True), override_name=f'{System_type}.pid')
        def System_pid(ctx: IntrinsicCallContext):
            if self.file.target == ast.Target.WINDOWS:
                GetCurrentProcessId = ctx.module.registry.get('GetCurrentProcessId')
                return ctx.builder.call(GetCurrentProcessId, [], 'System.pid')
            else:
                getpid = ctx.module.registry.get('getpid')
                return ctx.builder.call(getpid, [], 'System.pid')

        for definition in Registry.get_all_definitions():
            name = definition.display_name or definition.llvm_name
            param_types = [ast.Type.from_llvm(self.file, ir_type) for ir_type in definition.type.args]
            params = [ast.Param(ast.Position(), type, str(i)) for i, type in enumerate(param_types)]
            ret_type = ast.Type.from_llvm(self.file, definition.type.return_type)

            @intrinsic(self, ret_type, params, override_name=name)
            def _(_: IntrinsicCallContext):
                # never called
                raise NotImplementedError('This should never run')
