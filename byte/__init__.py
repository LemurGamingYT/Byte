from sys import exit as sys_exit
from pathlib import Path
from logging import info

from colorama import Fore, Style

from byte.test_factory import TestFactory, PythonTestHandler, CTestHandler, ByteTestHandler
# from byte.project import create_new_project
from byte.pipeline import Pipeline
from byte import ast


TESTS_DIR = ast.BYTE_DIR / 'tests'

def test_text_colour(num_tests: int, passed_count: int):
    if passed_count == num_tests:
        return Fore.GREEN
    elif passed_count >= num_tests // 2:
        return Fore.YELLOW
    else:
        return Fore.RED

class ArgParser:
    def __init__(self, args: list[str]):
        self.test_factory = TestFactory()
        self.test_factory.register('.py', PythonTestHandler())
        self.test_factory.register('.c', CTestHandler())
        self.test_factory.register('.byte', ByteTestHandler())
        
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
        print(f'Byte v{ast.VERSION}')

    # def _init(self):
    #     name = self.arg(1)
    #     if name is None:
    #         print('Usage: byte init <name> [<directory>]')
    #         print('no name specified')
    #         sys_exit(1)
            
    #     directory_path = self.arg(2)
    #     if directory_path is None:
    #         directory = Path.cwd()
    #     else:
    #         directory = Path(directory_path)

    #     if not directory.exists():
    #         print('Usage: byte init <name> [<directory>]')
    #         print('directory does not exist')
    #         sys_exit(1)

    #     if not directory.is_dir():
    #         print('Usage: byte init <name> [<directory>]')
    #         print('given directory is not a directory')
    #         sys_exit(1)

    #     create_new_project(name, directory)

    def test_list(self, paths: list[Path]):
        passed_count = 0
        for path in paths:
            success = self.test_single(path)
            if not success:
                continue
            
            passed_count += 1

        return passed_count

    def test_dir(self, path: Path):
        possible_suffixes = list(self.test_factory.handlers)
        num_tests = passed_count = 0
        for suffix in possible_suffixes:
            tests = list(path.rglob(f'*{suffix}'))
            num_tests += len(tests)
            passed_count += self.test_list(tests)

        colour = test_text_colour(num_tests, passed_count)
        print(f'{colour}{Style.BRIGHT}{passed_count}/{num_tests} tests passed{Style.RESET_ALL}')

    def test_single(self, path: Path):
        info(f'running test path {path}')
        success = self.test_factory.test_file(path)
        if success:
            print(f'{Fore.GREEN}{Style.BRIGHT}successfully ran test {path.stem}{Style.RESET_ALL}')
        else:
            print(f'{Fore.RED}{Style.BRIGHT}test {path.stem} failed{Style.RESET_ALL}')

        return success

    def _test(self):
        test_name = self.arg(1)
        if test_name is None:
            return self.test_dir(TESTS_DIR)

        test_file = self.find_first_file(TESTS_DIR, test_name)
        if test_file is None:
            print('Usage: byte test <test-name>')
            print(f'no test named {test_name}')
            sys_exit(1)

        if not test_file.is_file():
            print('Usage: byte test <test-name>')
            print(f'invalid test file {test_name} ({test_file})')
            sys_exit(1)

        return self.test_single(test_file)
    
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

        pipeline = Pipeline()
        options = ast.CompileOptions.from_arg_parser(self)
        file = ast.File(path, options=options)
        return pipeline.compile_to_exe(file)
