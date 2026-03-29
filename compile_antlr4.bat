@echo off
antlr4 -Dlanguage=Python3 -o byte/parser -visitor -no-listener byte/Byte.g4
