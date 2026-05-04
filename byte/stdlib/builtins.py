from byte.intrinsics import IntrinsicLib, IntrinsicCallContext, intrinsic
from byte.llvm_extensions import NULL


class builtins(IntrinsicLib):
    def init(self):
        @intrinsic(self, self.file.type_map.get('pointer'))
        def _null(_: IntrinsicCallContext):
            return NULL()
