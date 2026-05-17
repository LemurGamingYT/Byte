from time import perf_counter
from pathlib import Path

from byte.ast_builder import ByteASTBuilder
from byte import ast


def time_lex_parse(path: Path):
    file = ast.File(path)

    builder = ByteASTBuilder(file)
    start = perf_counter()
    token_stream = builder.lex()
    end = perf_counter()
    print(f'Time taken to lex {path.name}: {end - start}s')

    start = perf_counter()
    _ = builder.parse(token_stream)
    end = perf_counter()
    print(f'Time taken to parse {path.name}: {end - start}s')

def test_time_parse():
    time_lex_parse(ast.STDLIB_PATH / 'builtins' / 'builtins.byte')
    time_lex_parse(ast.BYTE_DIR.parent / 'examples' / 'test.byte')
    return True
