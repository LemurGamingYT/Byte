from importlib import import_module
from sys import exit as sys_exit
from subprocess import run
from logging import info
from pathlib import Path
from typing import cast

from colorama import Fore, Style

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
from byte.io_disabler import disable_io
from byte import ast


BYTE_DIR = Path(__file__).parent
TESTS_DIR = BYTE_DIR / 'tests'
CRUNTIME_DIR = BYTE_DIR / 'cruntime'
VERSION = '0.0.1'
PASS_CLASSES = [Preprocessor, CodeAnalysis, ForwardDeclaration, NameResolver, TypeChecker, MemoryManager]

def parse(file: ast.File):
    builder = ByteASTBuilder(file)
    return builder.build()

def run_passes(file: ast.File, stop_idx: int = -1):
    program = parse(file)
    for i, cls in enumerate(PASS_CLASSES):
        if i == stop_idx:
            break

        program = cls.run(file, program)

    return program

def compile_file(file: ast.File):
    ast_file = file.path.with_suffix('.byteast')
    
    program = parse(file)
    if file.options.debug:
        ast_file.write_text(str(program))
    else:
        ast_file.unlink(True)
    
    for cls in PASS_CLASSES:
        info(f'running pass {cls.__name__} on file {file.path}')
        ast_file = ast_file.with_stem(f'{file.path.stem}_{cls.__name__.lower()}')
        
        program = cls.run(file, program)
        if file.options.debug:
            ast_file.write_text(str(program))
        else:
            ast_file.unlink(True)
    
    return cast(CompileResult, CodeGeneration.run(file, program))

def compile_to_obj(file: ast.File):
    res = compile_file(file)

    ll_file = file.path.with_suffix('.ll')
    ll_file.write_text(str(res.module))

    flags = ['-Wno-override-module', '-Wall', '-Werror', '-Wpedantic', '-Wextra']
    if file.options.optimise:
        flags.append('-O3')
    
    flags_str = ' '.join(flags)

    obj_file = file.path.with_suffix('.o')
    compile_cmd = f'clang -c -o {obj_file} {ll_file} {flags_str}'
    info(f'running clang compile command \'{compile_cmd}\'')
    run(compile_cmd, shell=True)

    if file.options.emit_asm:
        asm_file = file.path.with_suffix('.asm')
        asm_compile_cmd = f'clang -S -o {asm_file} {ll_file} {flags_str}'
        info(f'running clang compile (to assembly) command \'{asm_compile_cmd}\'')
        run(asm_compile_cmd, shell=True)

    if not file.options.emit_llvm:
        ll_file.unlink()
    
    return obj_file

def compile_to_exe(file: ast.File):
    obj_file = compile_to_obj(file)
    obj_files = [obj_file] + [dependency for dependency in file.dependencies if dependency.suffix == '.o']
    for cfile in CRUNTIME_DIR.rglob('*.c'):
        c_obj = cfile.with_suffix('.o')
        run(f'clang -c {cfile} -o {c_obj}')
        
        obj_files.append(c_obj)
    
    exe_file = file.path.with_suffix('.exe')
    obj_files_str = ' '.join(map(str, obj_files))
    flags = []
    if file.options.optimise:
        flags.append('-O3')

    flags_str = ' '.join(flags)
    link_cmd = f'{find_linker()} {obj_files_str} -o {exe_file} {flags_str}'
    info(f'running clang link command \'{link_cmd}\'')
    run(link_cmd, shell=True)
    
    for obj in obj_files:
        obj.unlink()
    
    return exe_file


class ArgParser:
    def __init__(self, args: list[str]):
        self.args = args
    
    def parse(self):
        action = self.arg(0)
        if action is None:
            print('Usage: byte <action> <file>')
            print('No action')
            sys_exit(1)
        
        method_name = f'_{action}'
        if method_name.startswith('__'):
            method_name = method_name[1:]
        
        method = getattr(self, method_name, None)
        if method is None:
            print('Usage: byte <action> <file>')
            print(f'Unknown action \'{action}\'')
            sys_exit(1)
        
        return method()

    def arg(self, index: int):
        while index < len(self.args):
            arg = self.args[index]
            if not arg.startswith('--'):
                return arg
            
            index += 1
        
        return None
    
    def flag(self, name: str):
        return any(f'--{name}' == arg for arg in self.args)
    
    def find_first_file(self, path: Path, name: str):
        for file in path.iterdir():
            if file.stem == name:
                return file
    
    def _version(self):
        print(f'Byte v{VERSION}')
    
    def _test(self, test_name: str | None = None):
        if test_name is None:
            test_name = self.arg(1)
        
        if test_name is None:
            fail_pass_count, num_fail_tests = self.test_dir(TESTS_DIR / 'fail')
            pass_pass_count, num_pass_tests = self.test_dir(TESTS_DIR / 'pass')
            passed_count = fail_pass_count + pass_pass_count
            num_tests = num_fail_tests + num_pass_tests
            print(f'{passed_count}/{num_tests} tests passed')
            return
        
        folder_test = TESTS_DIR / test_name
        if folder_test.is_dir():
            passed_count, num_tests = self.test_dir(folder_test)
            print(f'{passed_count}/{num_tests} tests passed')
            return
        
        test = self.find_first_file(TESTS_DIR, test_name)
        if test is None:
            print('Usage: byte test <test-name>')
            print('Unknown test name')
            sys_exit(1)
        
        had_error = self.test_file(test)
        if had_error:
            print('test failed')
        else:
            print('test passed')
    
    def test_dir(self, path: Path):
        tests = list(path.glob('*.byte'))
        passed_count = 0
        for byte_file in tests:
            had_error = self.test_file(byte_file)
            
            dir_name = byte_file.parent.name
            success = (dir_name == 'fail' and had_error) or (dir_name == 'pass' and not had_error)
            if success:
                print(f'{byte_file.stem} test passed')
                passed_count += 1
            else:
                print(f'{byte_file.stem} test failed')
        
        return passed_count, len(tests)
    
    def test_file(self, test: Path):
        match test.suffix:
            case '.py':
                module = import_module(f'byte.tests.{test.stem}')
                method = getattr(module, f'test_{test.stem}')
                return not method()
            case '.c':
                exe_file = test.with_suffix('.exe')
                res = run(f'clang {test.absolute().as_posix()} -o {exe_file.absolute().as_posix()} -D_TEST')
                if res.returncode != 0:
                    print(f'{Style.BRIGHT}{Fore.RED}C exe compilation failed{Style.RESET_ALL}')
                    return True
                
                with disable_io():
                    res = run(f'{exe_file}')
                
                if res.returncode != 0:
                    print(f'{Style.BRIGHT}{Fore.RED}error occurred running exe file{Style.RESET_ALL}')
                    return True
                
                exe_file.unlink()
                return False
            case '.byte':
                with disable_io():
                    try:
                        self._build(str(test))
                        return False
                    except SystemExit:
                        return True
            case _:
                raise NotImplementedError(f'test suffix {test.suffix}')
    
    def _build(self, file_path: str | None = None):
        if file_path is None:
            file_path = self.arg(1)
        
        if file_path is None:
            print('Usage: byte build <file>')
            print('No file')
            sys_exit(1)
        
        path = Path(file_path)
        if not path.exists():
            print('Usage: byte build <file>')
            print(f'File \'{file_path}\' does not exist')
            sys_exit(1)
        
        if not path.is_file():
            print('Usage: byte build <file>')
            print(f'File \'{file_path}\' is not a file')
            sys_exit(1)
        
        options = ast.CompileOptions.from_arg_parser(self)
        file = ast.File(path, options=options)
        compile_to_exe(file)
