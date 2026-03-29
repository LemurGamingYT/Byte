from importlib import import_module
from sys import exit as sys_exit
from subprocess import run
from logging import info
from pathlib import Path

from byte.passes.code_generation import CodeGeneration
from byte.passes.node_expansion import NodeExpansion
from byte.passes.memory_manager import MemoryManager
from byte.passes.preprocessor import Preprocessor
from byte.passes.type_checker import TypeChecker
from byte.ast_builder import ByteASTBuilder
from byte import ast


TESTS_DIR = Path(__file__).parent / 'tests'
VERSION = '0.0.1'
PASS_CLASSES = [Preprocessor, TypeChecker, MemoryManager, NodeExpansion]

def parse(file: ast.File):
    builder = ByteASTBuilder(file)
    return builder.build()

def compile_to_str(file: ast.File):
    ast_file = file.path.with_suffix('.byteast')
    
    program = parse(file)
    ast_file.write_text(str(program))
    
    for cls in PASS_CLASSES:
        info(f'running pass {cls.__name__}')
        program = cls.run(file, program)
        ast_file.write_text(str(program))
    
    return str(CodeGeneration.run(file, program))

def compile_to_obj(file: ast.File):
    code = compile_to_str(file)
    ll_file = file.path.with_suffix('.ll')
    ll_file.write_text(code)
    
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
    exe_file = file.path.with_suffix('.exe')
    obj_files_str = ' '.join(map(str, obj_files))
    link_cmd = f'clang {obj_files_str} -o {exe_file}'
    info(f'running clang link command \'{link_cmd}\'')
    run(link_cmd, shell=True)
    
    return exe_file

class ArgParser:
    def __init__(self, args: list[str]):
        self.args = args
    
    def parse(self):
        action = self.arg(0)
        match action:
            case 'build':
                self.build()
            case 'test':
                self.test()
            case 'version':
                self.version()
            case _:
                print('Usage: byte <action> <file>')
                if action is None:
                    print('No action')
                else:
                    print(f'Unknown action \'{action}\'')
                
                sys_exit(1)

    def arg(self, index: int):
        if index < len(self.args):
            return self.args[index]
        
        return None
    
    def version(self):
        print(f'Byte v{VERSION}')
    
    def test(self):
        test_name = self.arg(1)
        if test_name is None:
            print('Usage: byte test <test-name>')
            print('No test name')
            sys_exit(1)
        
        test = TESTS_DIR / f'{test_name}.py'
        if not test.is_file():
            print('Usage: byte test <test-name>')
            print('Unknown test name')
            sys_exit(1)
        
        module = import_module(f'byte.tests.{test_name}')
        method = getattr(module, f'test_{test_name}')
        method()
    
    def build(self, file_path: str | None = None):
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
