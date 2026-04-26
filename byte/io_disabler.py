import sys
from contextlib import contextmanager
from io import TextIOBase


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
