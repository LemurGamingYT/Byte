from time import perf_counter

from byte.llvm_backend import LLVMBackend
from byte.pipeline import Pipeline
from byte import ast


def test_time_comp():
    builtins_byte = ast.STDLIB_PATH / 'builtins' / 'builtins.byte'
    file = ast.File(builtins_byte)
    pipeline = Pipeline()

    start = perf_counter()
    res = pipeline.compile_file(file)
    end = perf_counter()
    print(f'Time taken to compile builtins.byte: {end - start}s')
    
    backend = LLVMBackend(res.module)
    obj_file = builtins_byte.with_suffix('.o')

    start = perf_counter()
    backend.emit_object(obj_file)
    end = perf_counter()
    print(f'Time taken to compile builtins to .o file: {end - start}s')

    obj_file.unlink()
    return True
