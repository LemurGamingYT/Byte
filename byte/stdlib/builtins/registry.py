from byte.intrinsics import intrinsic, IntrinsicLib, IntrinsicCallContext
from byte.llvm_extensions import Registry
from byte import ast


class registry(IntrinsicLib):
    def init(self):
        for definition in Registry.get_all_definitions():
            name = definition.display_name or definition.llvm_name
            param_types = [ast.Type.from_llvm(self.file, ir_type) for ir_type in definition.type.args]
            params = [ast.Param(ast.Position(), type, str(i)) for i, type in enumerate(param_types)]
            ret_type = ast.Type.from_llvm(self.file, definition.type.return_type)

            @intrinsic(self, ret_type, params, override_name=name)
            def _(_: IntrinsicCallContext):
                # never called
                raise NotImplementedError('This should never run')
