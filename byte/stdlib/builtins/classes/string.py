from byte.intrinsics import intrinsic, IntrinsicClass, IntrinsicCallContext
from byte import ast


class string(IntrinsicClass):
    def init(self):
        int_type = self.file.type_map.get('int')
        bool_type = self.file.type_map.get('bool')
        string_type = self.file.type_map.get('string')
        pointer_type = self.file.type_map.get('pointer')

        @intrinsic(self, pointer_type, [ast.Param(ast.Position(), string_type, 'self')], flags=ast.FunctionFlags(property=True))
        def _ptr(ctx: IntrinsicCallContext):
            s = ctx.arg(0)
            return ctx.builder.extract_value(s, 0, ctx.name)

        @intrinsic(self, int_type, [ast.Param(ast.Position(), string_type, 'self')], flags=ast.FunctionFlags(property=True))
        def _length(ctx: IntrinsicCallContext):
            s = ctx.arg(0)
            return ctx.builder.extract_value(s, 1, ctx.name)

        @intrinsic(self, bool_type, [ast.Param(ast.Position(), string_type, 'self')], flags=ast.FunctionFlags(property=True))
        def _is_allocated(ctx: IntrinsicCallContext):
            s = ctx.arg(0)
            return ctx.builder.extract_value(s, 2, ctx.name)

        @intrinsic(self, string_type, [ast.Param(ast.Position(), string_type, 'self')], flags=ast.FunctionFlags(method=True))
        def _to_string(ctx: IntrinsicCallContext):
            ptr = ctx.call('string.ptr', ctx.args)
            length = ctx.call('string.length', ctx.args)
            return ctx.call('string.new.pointer.int', [
                ast.Arg(ctx.pos, ctx.file.type_map.get('pointer'), ptr),
                ast.Arg(ctx.pos, ctx.file.type_map.get('int'), length)
            ])
