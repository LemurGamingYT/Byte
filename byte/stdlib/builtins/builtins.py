from math import pi, e

from llvmlite import ir

from byte.intrinsics import intrinsic, IntrinsicLib, IntrinsicCallContext
from byte.llvm_extensions import llint, max_int, min_int
from byte.stdlib.builtins.operations import operations
from byte.stdlib.builtins.intrinsics import intrinsics
from byte.stdlib.builtins.registry import registry
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

        self.add(registry)
        self.add(operations)
        self.add(intrinsics)

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

        @intrinsic(
            self, int_type, [ast.Param(ast.Position(), bool_type, 'self')], flags=ast.FunctionFlags(method=True),
            override_name=f'{bool_type}.to_int'
        )
        def bool_to_int(ctx: IntrinsicCallContext):
            return ctx.builder.zext(ctx.arg(0), ir.IntType(32), ctx.name)

        @intrinsic(self, float_type, flags=ast.FunctionFlags(static=True, property=True), override_name=f'{Math_type}.pi')
        def Math_pi(_: IntrinsicCallContext):
            return ir.Constant(ir.FloatType(), pi)

        @intrinsic(self, float_type, flags=ast.FunctionFlags(static=True, property=True), override_name=f'{Math_type}.e')
        def Math_e(_: IntrinsicCallContext):
            return ir.Constant(ir.FloatType(), e)

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
