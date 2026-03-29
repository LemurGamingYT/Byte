from sys import argv

from colorama import init

from byte import ArgParser


def main():
    arg_parser = ArgParser(argv[1:])
    arg_parser.parse()


if __name__ == '__main__':
    init()
    main()
