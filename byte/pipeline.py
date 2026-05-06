from sys import exit as sys_exit
from subprocess import run
from logging import info
from pathlib import Path
from typing import cast

from byte.passes.code_generation import CodeGeneration, CompileResult
from byte.passes.forward_decl import ForwardDeclaration
# from byte.passes.return_checker import ReturnChecker
from byte.passes.memory_manager import MemoryManager
from byte.passes.name_resolver import NameResolver
from byte.passes.code_analysis import CodeAnalysis
from byte.passes.preprocessor import Preprocessor
from byte.passes.type_checker import TypeChecker
from byte.llvm_extensions import find_linker
from byte.ast_builder import ByteASTBuilder
from byte.passes import ByteCompilerPass
from byte import ast


CRUNTIME_DIR = Path(__file__).parent / 'cruntime'
DEFAULT_PASSES = [Preprocessor, CodeAnalysis, ForwardDeclaration, NameResolver, TypeChecker, MemoryManager]

def run_cmd(cmd: list[str]):
    cmd_str = ' '.join(cmd)
    info(f'running \'{cmd_str}\'')
    return run(cmd, shell=True)


class Pipeline:
    def __init__(self, passes: list[type[ByteCompilerPass]] | None = None):
        self.passes = passes or DEFAULT_PASSES.copy()

    def pass_index(self, pass_type: type[ByteCompilerPass]):
        return self.passes.index(pass_type)

    def end_at_pass(self, pass_type: type[ByteCompilerPass]):
        idx = self.pass_index(pass_type)
        new = Pipeline(self.passes[:idx + 1])
        assert new.passes[-1] == pass_type, f'last pass is of type {new.passes[-1]}, not {pass_type}'
        return new

    def run(self, file: ast.File, program: ast.Node):
        ast_file = file.path.with_suffix('.byteast')
        for p in self.passes:
            pass_name = p.__name__
            info(f'running pass {pass_name} on file {file.path}')
            program = p.run(file, program)

            if file.options.debug:
                ast_file = ast_file.with_stem(f'{file.path.stem}_{pass_name.lower()}')
                ast_file.write_text(str(program))
            else:
                ast_file.unlink(missing_ok=True)

        return program
    
    def parse(self, file: ast.File):
        builder = ByteASTBuilder(file)
        return builder.build()
    
    def run_passes(self, file: ast.File):
        program = self.parse(file)
        return self.run(file, program)
    
    def compile_file(self, file: ast.File):
        program = self.parse(file)
    
        if file.options.debug:
            file.path.with_suffix('.byteast').write_text(str(program))
    
        program = self.run(file, program)
        return cast(CompileResult, CodeGeneration.run(file, program))
    
    def compile_to_obj(self, file: ast.File):
        res = self.compile_file(file)
    
        ll_file = file.path.with_suffix('.ll')
        ll_file.write_text(str(res.module))
    
        flags = file.options.to_clang_flags()
    
        obj_file = file.path.with_suffix('.o')
        run_cmd(['clang', '-c', '-o', str(obj_file), str(ll_file), *flags])
    
        if not file.options.emit_llvm:
            ll_file.unlink()
        
        return obj_file
    
    def compile_to_exe(self, file: ast.File):
        obj_file = self.compile_to_obj(file)
        obj_files = [obj_file] + [dependency for dependency in file.dependencies if dependency.suffix == '.o']
        for cfile in CRUNTIME_DIR.rglob('*.c'):
            c_obj = cfile.with_suffix('.o')
            run_cmd(['clang', '-c', str(cfile), '-o', str(c_obj)])
            
            obj_files.append(c_obj)
        
        exe_file = file.path.with_suffix('.exe')
        flags = []
        if file.options.optimise:
            flags.append('-O3')
    
        linker = find_linker()
        if linker is None:
            print('unable to find a valid linker command')
            sys_exit(1)
        
        run_cmd([linker, *[str(obj) for obj in obj_files], '-o', str(exe_file), *flags])
        
        for obj in obj_files:
            obj.unlink()
        
        return exe_file
