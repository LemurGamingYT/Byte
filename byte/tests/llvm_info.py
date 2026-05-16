from llvmlite import binding as llvm


llvm.initialize()
llvm.initialize_all_targets()
llvm.initialize_all_asmprinters()

def test_llvm_info():
    triple = llvm.get_process_triple()

    print(f'Default Triple: {llvm.get_default_triple()}')
    print(f'Process Triple: {triple}')
    print(f'Object Format: {llvm.get_object_format(triple)}')

    llvm_version = '.'.join(map(str, llvm.llvm_version_info))
    print(f'LLVM version: {llvm_version}')
    
    target = llvm.Target.from_triple(triple)
    print(f'Target: {target}')
    
    target_machine = target.create_target_machine(cpu='generic', reloc='pic', codemodel='default')
    print(f'Target Machine Triple: {target_machine.triple}')
    print(f'Target Data: {target_machine.target_data}')
    return True
