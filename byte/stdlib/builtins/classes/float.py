from llvmlite import ir

from byte.intrinsics import intrinsic, IntrinsicClass, IntrinsicCallContext
from byte.llvm_extensions import llint
from byte import ast


class float(IntrinsicClass):
    def init(self):
        int_type = self.file.type_map.get('int')
        float_type = self.file.type_map.get('float')
        string_type = self.file.type_map.get('string')

        # @intrinsic(self, float_type, flags=ast.FunctionFlags(static=True, property=True))
        # def _max(_: IntrinsicCallContext):
        #     return ir.Constant(ir.FloatType(), 3.402823e+38)

        # @intrinsic(self, float_type, flags=ast.FunctionFlags(static=True, property=True))
        # def _min(_: IntrinsicCallContext):
        #     return ir.Constant(ir.FloatType(), 1.175494e-38)

        @intrinsic(self, float_type, [ast.Param(ast.Position(), float_type, 'self')], flags=ast.FunctionFlags(property=True))
        def _decimal(ctx: IntrinsicCallContext):
            s = ctx.arg(0)
            return ctx.builder.frem(s, ir.Constant(ir.FloatType(), 1), ctx.name)

        @intrinsic(self, string_type, [ast.Param(ast.Position(), float_type, 'self')], flags=ast.FunctionFlags(method=True))
        def _to_string(ctx: IntrinsicCallContext):
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

        @intrinsic(self, int_type, [ast.Param(ast.Position(), float_type, 'self')], flags=ast.FunctionFlags(method=True))
        def _to_int(ctx: IntrinsicCallContext):
            return ctx.builder.fptosi(ctx.arg(0), ir.IntType(32), ctx.name)
