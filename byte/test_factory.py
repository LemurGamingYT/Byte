from importlib import import_module
from typing import Protocol
from subprocess import run
from logging import error
from pathlib import Path

from colorama import Fore, Style

from byte.pipeline import Pipeline
from byte import ast


class TestFactory:
    def __init__(self) -> None:
        self.handlers = {}

    def register(self, suffix: str, handler_type: 'TestFileHandler'):
        self.handlers[suffix] = handler_type

    def test_file(self, path: Path):
        try:
            return self.handlers[path.suffix].test(path)
        except KeyError:
            raise NotImplementedError(path.suffix)

class TestFileHandler(Protocol):
    def test(self, path: Path) -> bool:
        ...

class PythonTestHandler:
    def test(self, path: Path):
        module = import_module(f'byte.tests.{path.stem}')
        method = getattr(module, f'test_{path.stem}')
        return method()

class CTestHandler:
    def test(self, path: Path):
        exe_file = path.with_suffix('.exe')
        res = run(['clang', str(path), '-o', str(exe_file), '-D_TEST'], shell=True)
        if res.returncode != 0:
            print(f'{Style.BRIGHT}{Fore.RED}C exe compilation failed{Style.RESET_ALL}')
            return False
        
        res = run([str(exe_file)], shell=True)
        if res.returncode != 0:
            print(f'{Style.BRIGHT}{Fore.RED}error occurred running exe file (error code {res.returncode}){Style.RESET_ALL}')
            return False
        
        exe_file.unlink()
        return True

class ByteTestHandler:
    def run_byte(self, path: Path):
        expected_error = path.stem.endswith('_error')
        
        pipeline = Pipeline()
        file = ast.File(path)
        exe_file = pipeline.compile_to_exe(file)
        if not exe_file.is_file():
            return False
        
        res = run([str(exe_file)], text=True, capture_output=True)
        exe_file.unlink()
        if res.returncode != 0:
            return expected_error

        expected_file = path.with_suffix('.out')
        if not expected_file.is_file():
            return True
        
        output = res.stdout.strip()
        expected_output = expected_file.read_text().strip()
        success = output == expected_output
        if not success:
            error(f"""test {path.stem} failed: expected output does not match output:
Expected: {expected_output}
Got: {output}""")

            return expected_error

        return success
    
    def test(self, path: Path):
        try:
            return self.run_byte(path)
        except SystemExit:
            return False
