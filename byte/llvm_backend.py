from ctypes import CFUNCTYPE, c_int
from subprocess import run
from logging import info
from pathlib import Path
from shutil import which

from llvmlite import ir, binding as llvm


def run_cmd(cmd: list[str]):
    cmd_str = ' '.join(cmd)
    info(f'running \'{cmd_str}\'')
    return run(cmd, check=True)


llvm.initialize()
llvm.initialize_native_target()
llvm.initialize_native_asmprinter()

class LLVMBackend:
    def __init__(self, module: ir.Module):
        self.module = module
        self.triple = module.triple
        self.target = llvm.Target.from_triple(self.triple)
        self.target_machine = self.target.create_target_machine(cpu='generic', reloc='pic', codemodel='default', opt=2)
        self.llvm_ir = str(module)

    def emit_ir(self, ll_file: Path):
        ll_file.write_text(self.llvm_ir)

    def emit_object(self, obj_file: Path):
        mod = llvm.parse_assembly(self.llvm_ir)
        mod.verify()

        obj = self.target_machine.emit_object(mod)
        obj_file.write_bytes(obj)
        return True

    def emit_executable(self, obj_files: list[Path], exe_file: Path):
        if which('lld-link') is not None:
            runtimes = ['kernel32.lib', 'ucrt.lib', 'vcruntime.lib', 'msvcrt.lib', 'legacy_stdio_definitions.lib']
            res = run_cmd(['lld-link', f'/OUT:{exe_file}', *map(str, obj_files), *runtimes, '/SUBSYSTEM:CONSOLE'])
        else:
            res = run_cmd(['clang', '-o', str(exe_file), *map(str, obj_files)])
        
        return res.returncode == 0

    def jit(self):
        mod = llvm.parse_assembly(self.llvm_ir)
        mod.verify()
        
        with llvm.create_mcjit_compiler(mod, self.target_machine) as ee:
            ee.finalize_object()
            ee.run_static_constructors()

            main_ptr = ee.get_function_address('main')
            main = CFUNCTYPE(c_int)(main_ptr)
            res = main()
            print(f'main returned with exit code {res}')
