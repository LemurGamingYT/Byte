from argparse import ArgumentParser, Namespace
from pathlib import Path
from logging import info
from typing import cast

from colorama import Fore, Style

from byte.test_factory import TestFactory, PythonTestHandler, CTestHandler, ByteTestHandler
from byte.project_manager import create_project, get_entry_file
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
    def __init__(self):
        self.test_factory = TestFactory()
        self.test_factory.register('.py', PythonTestHandler())
        self.test_factory.register('.c', CTestHandler())
        self.test_factory.register('.byte', ByteTestHandler())

        self.arg_parser = ArgumentParser(prog='byte', description='The Byte programming language compiler')
        self.subparsers = self.arg_parser.add_subparsers(dest='action', required=True)

        self.build_parser = self.subparsers.add_parser('build', help='Builds the given file')
        self.build_parser.add_argument('file', type=Path, help='The target file to build', nargs='?')
        self.build_parser.add_argument('--debug', action='store_true',
            help='Whether to enable debug mode (used mostly for development of the programming language)')
        self.build_parser.add_argument('-opt', '--optimise', action='store_true', help='Whether to optimise the code')
        self.build_parser.add_argument('--emit-llvm', action='store_true', help='Whether to emit the .ll (LLVM IR) file')
        self.build_parser.set_defaults(func=self.build_command)

        self.test_parser = self.subparsers.add_parser('test', help='Run language tests')
        self.test_parser.add_argument('test_name', help='The name of the test to run', nargs='?')
        self.test_parser.set_defaults(func=self.test_command)

        self.version_parser = self.subparsers.add_parser('version', help='Get the language version')
        self.version_parser.set_defaults(func=self.version_command)

        self.init_parser = self.subparsers.add_parser('init', help='Creates a new Byte project folder')
        self.init_parser.add_argument('project_name', help='The name of the project')
        self.init_parser.set_defaults(func=self.init_command)

    def parse(self):
        args = self.arg_parser.parse_args()
        args.func(args)
        return args

    def init_command(self, args: Namespace):
        project_name = str(args.project_name)
        project_folder = Path.cwd() / project_name

        try:
            project_folder.mkdir()
        except FileExistsError:
            self.init_parser.error('a file already exists with that name')

        create_project(project_folder, project_name)

    def build(self, path: Path, options: ast.CompileOptions):
        pipeline = Pipeline()
        file = ast.File(path, options=options)
        return pipeline.compile_to_exe(file)

    def build_dir(self, path: Path, options: ast.CompileOptions):
        success, data = get_entry_file(path)
        if not success:
            self.build_parser.error(str(data))
        
        return self.build(cast(Path, data), options)

    def build_command(self, args: Namespace):
        options = ast.CompileOptions(args.debug, args.optimise, args.emit_llvm)
        if args.file is None:
            return self.build_dir(Path.cwd(), options)
        
        file: Path = args.file
        if not file.exists():
            self.build_parser.error('file does not exist')

        if file.is_dir():
            return self.build_dir(file, options)
        
        return self.build(file, options)

    def test_command(self, args: Namespace):
        test_name = args.test_name
        if test_name is None:
            return self.test_dir(TESTS_DIR)

        test_file = self.find_first_file(TESTS_DIR, test_name)
        if test_file is None:
            self.test_parser.error(f'no test named {test_name}')

        if not test_file.is_file():
            self.test_parser.error(f'invalid test file {test_name} ({test_file})')

        return self.test_single(test_file)

    def version_command(self, _):
        print(f'Byte v{ast.VERSION}')
    
    def find_first_file(self, path: Path, name: str):
        for file in path.iterdir():
            if file.stem == name:
                return file

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
