from sys import exit as sys_exit
from pathlib import Path

from byte.test_factory import TestFactory, PythonTestHandler, CTestHandler, ByteTestHandler
from byte.pipeline import Pipeline
from byte import ast


BYTE_DIR = Path(__file__).parent
TESTS_DIR = BYTE_DIR / 'tests'
VERSION = '0.0.1'

class ArgParser:
    def __init__(self, args: list[str]):
        self.test_factory = TestFactory()
        self.test_factory.register('.py', PythonTestHandler())
        self.test_factory.register('.c', CTestHandler())
        self.test_factory.register('.byte', ByteTestHandler())

        self.pipeline = Pipeline()
        
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
        
        had_error = self.test_factory.test_file(test)
        if had_error:
            print('test failed')
        else:
            print('test passed')
    
    def test_dir(self, path: Path):
        tests = list(path.glob('*.byte'))
        passed_count = 0
        for byte_file in tests:
            had_error = self.test_factory.test_file(byte_file)
            
            dir_name = byte_file.parent.name
            success = (dir_name == 'fail' and had_error) or (dir_name == 'pass' and not had_error)
            if success:
                print(f'{byte_file.stem} test passed')
                passed_count += 1
            else:
                print(f'{byte_file.stem} test failed')
        
        return passed_count, len(tests)
    
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
        return self.pipeline.compile_to_exe(file)
