from math import pi, e

from llvmlite import ir

from byte.intrinsics import intrinsic, IntrinsicClass, IntrinsicCallContext
from byte import ast


class Math(IntrinsicClass):
    def init(self):
        float_type = self.file.type_map.get('float')
        
        @intrinsic(self, float_type, flags=ast.FunctionFlags(static=True, property=True))
        def _pi(_: IntrinsicCallContext):
            return ir.Constant(ir.FloatType(), pi)

        @intrinsic(self, float_type, flags=ast.FunctionFlags(static=True, property=True))
        def _e(_: IntrinsicCallContext):
            return ir.Constant(ir.FloatType(), e)
