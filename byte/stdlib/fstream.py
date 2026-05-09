from llvmlite import ir

from byte.intrinsics import intrinsic, IntrinsicLib, IntrinsicCallContext
from byte import ast


class fstream(IntrinsicLib):
    def init(self):
        string_type = self.file.type_map.get('string')
        File_type = self.file.type_map.add('File', ast.ClassType('File', [string_type]))

        @intrinsic(
            self, File_type, [ast.Param(ast.Position(), string_type, 'filename', flags=ast.ParamFlags(copy=True))],
            flags=ast.FunctionFlags(static=True, method=True), override_name=f'{File_type}.new'
        )
        def File_new(ctx: IntrinsicCallContext):
            filename = ctx.arg(0)

            File = ctx.codegen.visit(File_type)
            return ctx.builder.struct(File, [filename], ctx.name)
