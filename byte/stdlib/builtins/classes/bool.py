from llvmlite import ir

from byte.intrinsics import intrinsic, IntrinsicClass, IntrinsicCallContext
from byte.llvm_extensions import llint
from byte import ast


class bool(IntrinsicClass):
    def init(self):
        int_type = self.file.type_map.get('int')
        bool_type = self.file.type_map.get('bool')
        string_type = self.file.type_map.get('string')
        
        @intrinsic(self, string_type, [ast.Param(ast.Position(), bool_type, 'self')], flags=ast.FunctionFlags(method=True))
        def _to_string(ctx: IntrinsicCallContext):
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

        @intrinsic(self, int_type, [ast.Param(ast.Position(), bool_type, 'self')], flags=ast.FunctionFlags(method=True))
        def _to_int(ctx: IntrinsicCallContext):
            return ctx.builder.zext(ctx.arg(0), ir.IntType(32), ctx.name)
