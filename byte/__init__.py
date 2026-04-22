import sys
from contextlib import contextmanager
from importlib import import_module
from sys import exit as sys_exit
from subprocess import run
from io import TextIOBase
from logging import info
from pathlib import Path
from typing import cast

from colorama import Fore, Style

from byte.passes.code_generation import CodeGeneration, CompileResult
from byte.passes.memory_manager import MemoryManager
from byte.passes.preprocessor import Preprocessor
from byte.passes.type_checker import TypeChecker
from byte.ast_builder import ByteASTBuilder
from byte import ast


BYTE_DIR = Path(__file__).parent
TESTS_DIR = BYTE_DIR / 'tests'
CRUNTIME_DIR = BYTE_DIR / 'cruntime'
VERSION = '0.0.1'
PASS_CLASSES = [Preprocessor, TypeChecker, MemoryManager]

def parse(file: ast.File):
    builder = ByteASTBuilder(file)
    return builder.build()

def compile_file(file: ast.File):
    ast_file = file.path.with_suffix('.byteast')
    
    program = parse(file)
    ast_file.write_text(str(program))
    
    for cls in PASS_CLASSES:
        info(f'running pass {cls.__name__}')
        program = cls.run(file, program)
        ast_file.write_text(str(program))
    
    return cast(CompileResult, CodeGeneration.run(file, program))

def compile_to_obj(file: ast.File):
    res = compile_file(file)
    ll_file = file.path.with_suffix('.ll')
    ll_file.write_text(str(res.module))
    
    obj_file = file.path.with_suffix('.o')
    flags = ['-Wno-override-module', '-Wall', '-Werror', '-Wpedantic', '-Wextra']
    flags_str = ' '.join(flags)
    compile_cmd = f'clang -c -o {obj_file} {ll_file} {flags_str}'
    info(f'running clang compile command \'{compile_cmd}\'')
    run(compile_cmd, shell=True)
    
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
    link_cmd = f'clang {obj_files_str} -o {exe_file}'
    info(f'running clang link command \'{link_cmd}\'')
    run(link_cmd, shell=True)
    
    return exe_file

@contextmanager
def disable_io():
    stdout = sys.stdout
    stdin = sys.stdin
    stderr = sys.stderr
    
    sys.stdout = DummyIO()
    sys.stdin = DummyIO()
    sys.stderr = DummyIO()
    
    yield
    
    sys.stdout = stdout
    sys.stdin = stdin
    sys.stderr = stderr


class DummyIO(TextIOBase):
    def write(self, _: str, /) -> int:
        return 0
    
    def read(self, _: int | None = -1, /) -> str:
        return ''

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
        if index < len(self.args):
            return self.args[index]
        
        return None
    
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
            print('Usage: byte test <test-name>')
            print('No test name')
            sys_exit(1)
        
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
        
        try:
            self.test_file(test)
            print('test passed')
        except SystemExit:
            print('test failed')
    
    def test_dir(self, path: Path):
        tests = list(path.glob('*.byte'))
        passed_count = 0
        for byte_file in tests:
            with disable_io():
                try:
                    self.test_file(byte_file)
                    had_error = False
                except SystemExit:
                    had_error = True
            
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
                method()
            case '.c':
                exe_file = test.with_suffix('.exe')
                res = run(f'clang {test.absolute().as_posix()} -o {exe_file.absolute().as_posix()} -D_TEST')
                if res.returncode != 0:
                    print(f'{Style.BRIGHT}{Fore.RED}C exe compilation failed{Style.RESET_ALL}')
                    sys_exit(1)
                
                res = run(f'{exe_file}')
                if res.returncode != 0:
                    print(f'{Style.BRIGHT}{Fore.RED}error occurred running exe file{Style.RESET_ALL}')
                    sys_exit(1)
                
                exe_file.unlink()
            case '.byte':
                self._build(str(test))
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
        
        file = ast.File(path)
        compile_to_exe(file)
