from logging import info, basicConfig, DEBUG
from platform import platform, architecture
from sys import argv

from llvmlite import binding
from colorama import init

from byte import ArgParser, VERSION


def main():
    info(f"""Byte compiler v{VERSION}
backend: LLVM
platform: {platform()}
architecture: {architecture()[0]}
LLVM target (triple): {binding.get_default_triple()}""")
    arg_parser = ArgParser(argv[1:])
    arg_parser.parse()


if __name__ == '__main__':
    init()
    basicConfig(
        filename='debug.log', filemode='w',
        format='%(filename)s (line %(lineno)d) [%(levelname)s] - %(message)s',
        encoding='utf-8', level=DEBUG
    )
    main()
