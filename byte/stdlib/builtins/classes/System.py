from byte.intrinsics import intrinsic, IntrinsicClass, IntrinsicCallContext
from byte.llvm_extensions import llint
from byte import ast


class System(IntrinsicClass):
    def init(self):
        int_type = self.file.type_map.get('int')
        string_type = self.file.type_map.get('string')
        
        @intrinsic(self, string_type, flags=ast.FunctionFlags(static=True, property=True))
        def _os(ctx: IntrinsicCallContext):
            text = self.file.target.name.title()
            os_name = ctx.module.global_string(text, 'os_name')
            os_name_ptr = ctx.builder.first_elem(os_name, 'os_name_ptr')
            return ctx.call('string.new', [
                ast.Arg(ctx.pos, ctx.file.type_map.get('pointer'), os_name_ptr),
                ast.Arg(ctx.pos, ctx.file.type_map.get('int'), llint(len(text))),
                ast.Arg(ctx.pos, ctx.file.type_map.get('bool'), llint(0, 1))
            ])

        @intrinsic(self, int_type, flags=ast.FunctionFlags(static=True, property=True))
        def _pid(ctx: IntrinsicCallContext):
            getpid = ctx.module.registry.get('getpid')
            return ctx.builder.call(getpid, [], 'System.pid')

        @intrinsic(self, params=[ast.Param(ast.Position(), int_type, 'duration')], flags=ast.FunctionFlags(static=True, method=True))
        def _sleep(ctx: IntrinsicCallContext):
            sleep = ctx.module.registry.get('sleep')
            duration = ctx.arg(0)
            return ctx.builder.call(sleep, [duration], 'sleep')
