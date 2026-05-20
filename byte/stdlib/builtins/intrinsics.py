from llvmlite import ir

from byte.intrinsics import intrinsic, IntrinsicLib, IntrinsicCallContext
from byte.llvm_extensions import NULL
from byte import ast


class intrinsics(IntrinsicLib):
    def init(self):
        int_type = self.file.type_map.get('int')
        bool_type = self.file.type_map.get('bool')
        string_type = self.file.type_map.get('string')
        pointer_type = self.file.type_map.get('pointer')

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
        
        @intrinsic(self, pointer_type)
        def _null(_: IntrinsicCallContext):
            return NULL()
