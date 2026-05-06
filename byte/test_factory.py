from importlib import import_module
from abc import ABC, abstractmethod
from subprocess import run
from pathlib import Path

from colorama import Fore, Style

from byte.io_disabler import disable_io
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

class TestFileHandler(ABC):
    @abstractmethod
    def test(self, path: Path) -> bool:
        ...

class PythonTestHandler(TestFileHandler):
    def test(self, path: Path):
        module = import_module(f'byte.tests.{path.stem}')
        method = getattr(module, f'test_{path.stem}')
        return not method()

class CTestHandler(TestFileHandler):
    def test(self, path: Path):
        exe_file = path.with_suffix('.exe')
        res = run(['clang', str(path), '-o', str(exe_file), '-D_TEST'], shell=True)
        if res.returncode != 0:
            print(f'{Style.BRIGHT}{Fore.RED}C exe compilation failed{Style.RESET_ALL}')
            return True
        
        with disable_io():
            res = run([str(exe_file)], shell=True)
        
        if res.returncode != 0:
            print(f'{Style.BRIGHT}{Fore.RED}error occurred running exe file (error code {res.returncode}){Style.RESET_ALL}')
            return True
        
        exe_file.unlink()
        return False

class ByteTestHandler(TestFileHandler):
    def test(self, path: Path):
        with disable_io():
            try:
                pipeline = Pipeline()
                file = ast.File(path)
                exe_file = pipeline.compile_to_exe(file)
                if exe_file.is_file():
                    run(f'{exe_file}', shell=True)
                
                return False
            except SystemExit:
                return True
