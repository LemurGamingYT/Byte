from llvmlite import binding as llvm, ir

from byte.llvm_extensions import ModuleExt
from byte.llvm_backend import LLVMBackend


llvm.initialize()
llvm.initialize_all_targets()
llvm.initialize_all_asmprinters()

def test_llvm_info():
    module = ModuleExt('temp', ir.Context())
    module.triple = llvm.get_default_triple()
    
    backend = LLVMBackend(module)

    print(f'Default Triple: {llvm.get_default_triple()}')
    print(f'Process Triple: {llvm.get_process_triple()}')
    print(f'Object Format: {llvm.get_object_format(backend.triple)}')

    llvm_version = '.'.join(map(str, llvm.llvm_version_info))
    print(f'LLVM version: {llvm_version}')
    
    print(f'Target: {backend.target}')
    print(f'Target Machine Triple: {backend.target_machine.triple}')
    print(f'Target Data: {backend.target_machine.target_data}')
    return True
