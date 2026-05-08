from subprocess import run

from llvmlite import ir, binding as llvm


llvm.initialize()
llvm.initialize_all_targets()
llvm.initialize_all_asmprinters()

triple = llvm.get_default_triple()

module = ir.Module(name='test')
module.triple = triple

fn_type = ir.FunctionType(ir.IntType(32), [])
fn = ir.Function(module, fn_type, name='main')

block = fn.append_basic_block('entry')
builder = ir.IRBuilder(block)
builder.ret(ir.Constant(ir.IntType(32), 0))

print(f'Triple: {triple}')
print(f'Format: {llvm.get_object_format(triple)}')

target = llvm.Target.from_triple(triple)
print(f'Target: {target}')

target_machine = target.create_target_machine(cpu='generic', reloc='pic', codemodel='default')
print(f'Target Machine Triple: {target_machine.triple}')
print(f'Target Data: {target_machine.target_data}')

module.data_layout = str(target_machine.target_data)

mod = llvm.parse_assembly(str(module))
mod.verify()

obj = target_machine.emit_object(mod)
with open('test.o', 'wb') as fp:
    fp.write(obj)

run(['llvm-readobj', 'test.o'], check=True)
run(['clang', 'test.o', '-o', 'test.exe'], check=True)
