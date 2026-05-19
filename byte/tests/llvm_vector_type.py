from pathlib import Path

from llvmlite import ir, binding as llvm

from byte.llvm_extensions import llint, ModuleExt, IRBuilderExt


def test_llvm_vector_type():
    module = ModuleExt()
    module.triple = llvm.get_default_triple()

    main = ir.Function(module, ir.FunctionType(ir.IntType(32), []), 'main')
    entry_block = main.append_basic_block('entry')
    builder = IRBuilderExt(entry_block)

    vec_type = ir.VectorType(ir.IntType(32), 3)
    vec = ir.Constant(vec_type, None)
    new_vec = builder.insert_element(vec, llint(5), llint(0), 'vec')
    added_vecs = builder.add(vec, new_vec, 'added_vecs')
    print(added_vecs)
    
    builder.ret(llint(0))

    ll_file = Path(__file__).parent / 'vector.ll'
    ll_file.write_text(str(module))
    return True
