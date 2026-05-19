from dataclasses import dataclass, field, fields
from typing import Callable, Union, Any
from contextlib import contextmanager
from abc import ABC, abstractmethod
from importlib import import_module
from logging import error, warning
from sys import exit as sys_exit
from platform import system
from pathlib import Path
from enum import Enum

from colorama import Fore, Style
from llvmlite import ir


BYTE_DIR = Path(__file__).parent
STDLIB_PATH = BYTE_DIR / 'stdlib'
VERSION = '0.0.1'
NODE_KWARGS = {'slots': True}

class Target(Enum):
    WINDOWS = 'Windows'
    LINUX = 'Linux'
    MACOS = 'Darwin'
    
    @staticmethod
    def current():
        return Target(system())
    
    @property
    def exe_extension(self):
        return '.exe' if self == Target.WINDOWS else ''

@dataclass
class Position:
    line: int = 0
    column: int = 0

    def comptime_error(self, file: 'File', message: str):
        lines = file.src.splitlines()
        if len(lines) >= self.line:
            print(file.src.splitlines()[self.line - 1])
            print(' ' * self.column + '^')
        
        print(f'{Style.BRIGHT}{Fore.RED}error (in {file.path.name}): {message}{Style.RESET_ALL}')
        error(message)
        sys_exit(1)
    
    def comptime_warning(self, file: 'File', message: str):
        print(file.src.splitlines()[self.line - 1])
        print(' ' * self.column + '^')
        print(f'{Style.BRIGHT}{Fore.YELLOW}warning (in {file.path.name}): {message}{Style.RESET_ALL}')
        warning(message)

@dataclass(kw_only=True, slots=True)
class SymbolFlags:
    mutable: bool = False
    public: bool = True
    forward_decl: bool = False

@dataclass
class Symbol:
    name: str
    type: 'Type'
    value: Any
    flags: SymbolFlags = field(default_factory=SymbolFlags)

@dataclass
class SymbolTable:
    parent: Union['SymbolTable', None] = None
    symbols: dict[str, Symbol] = field(default_factory=dict)
    
    def get(self, name: str):
        if self.parent is not None and self.parent.has(name):
            return self.parent.get(name)
        
        return self.symbols[name]

    def tryget(self, name: str):
        if self.parent is not None and self.parent.has(name):
            return self.parent.tryget(name)
        
        return self.symbols.get(name)
                 
    def add(self, symbol: Symbol):
        self.symbols[symbol.name] = symbol
    
    def has(self, name: str):
        if self.parent is not None and self.parent.has(name):
            return True
        
        return name in self.symbols
                 
    def remove(self, name: str):
        if self.parent is not None and self.parent.has(name):
            return self.parent.remove(name)
        elif name in self.symbols:
            del self.symbols[name]
            return True
        
        return False
    
    def merge(self, other: 'SymbolTable', merge_private: bool = False):
        if merge_private:
            self.symbols.update(other.symbols)
        else:
            non_static_symbols = {k: v for k, v in other.symbols.items() if v.flags.public}
            self.symbols.update(non_static_symbols)
                 
@dataclass
class TypeMap:
    types: dict[str, 'Type'] = field(default_factory=dict)
    
    def get(self, name: str):
        return self.types[name]
                 
    def tryget(self, name: str):
        return self.types.get(name)
                 
    def add(self, name: str, typ: Union['Type', None] = None):
        self.types[name] = typ or Type(name)
        return self.types[name]
    
    def has(self, name: str):
        return name in self.types
                 
    def remove(self, name: str):
        if self.has(name):
            del self.types[name]
    
    def clone(self):
        return TypeMap(self.types.copy())
    
    def merge(self, other: 'TypeMap'):
        self.types.update(other.types)

@dataclass
class ScopePassData:
    codegen_while_merge_block: ir.Block | None = None
    codegen_while_test_block: ir.Block | None = None
    end_of_scope_nodes: list['Node'] = field(default_factory=list)
    prepend_nodes: list['Node'] = field(default_factory=list)
    
    def clone(self):
        return ScopePassData(self.codegen_while_merge_block, self.codegen_while_test_block)

@dataclass
class Scope:
    parent: Union['Scope', None] = None
    symbol_table: SymbolTable = field(default_factory=SymbolTable)
    in_loop: bool = False
    data: ScopePassData = field(default_factory=ScopePassData)
    
    def clone(self):
        return Scope(self, SymbolTable(self.symbol_table), self.in_loop, self.data.clone())

@dataclass(slots=True)
class CompileOptions:
    debug: bool = False
    optimise: bool = False
    emit_llvm: bool = False

@dataclass
class File:
    path: Path
    scope: Scope = field(default_factory=Scope)
    type_map: TypeMap = field(default_factory=TypeMap)
    dependencies: list[Path] = field(default_factory=list)
    options: CompileOptions = field(default_factory=CompileOptions)
    target: Target = field(default_factory=Target.current)
    
    @property
    def unique_name(self):
        self._unique_name_idx += 1
        return f'_{self._unique_name_idx}'

    @property
    def src(self):
        return self.path.read_text()

    @property
    def global_scope(self):
        global_scope = self.scope
        while global_scope.parent is not None:
            global_scope = global_scope.parent

        return global_scope
    
    def __post_init__(self):
        self._unique_name_idx = -1
        
        self.type_map.add('int')
        self.type_map.add('float')
        self.type_map.add('bool')
        self.type_map.add('nil')
        
        self.type_map.add('string')
        self.type_map.add('Math')
        self.type_map.add('System')
        self.type_map.add('IOFile')
        
        self.type_map.add('any')
        self.type_map.add('pointer')
        self.type_map.add('function')
    
    @contextmanager
    def child_scope(self):
        outer_scope = self.scope
        self.scope = self.scope.clone()
        yield
        self.scope = outer_scope


@dataclass(**NODE_KWARGS)
class Node(ABC):
    pos: Position = field(repr=False, compare=False)
    type: 'Type'
    
    @property
    def children(self):
        children = []
        for f in fields(self):
            value = getattr(self, f.name)
            if isinstance(value, Node):
                children.append(value)
            elif isinstance(value, list):
                children.extend(elem for elem in value if isinstance(elem, Node))
        
        return children
    
    def to_arg(self):
        return Arg(self.pos, self.type, self)
    
    @abstractmethod
    def __str__(self) -> str:
        ...

@dataclass(**NODE_KWARGS)
class TypelessNode(Node, ABC):
    type: 'Type' = field(default_factory=lambda: Type('any'), init=False, repr=False, compare=False)

@dataclass(**NODE_KWARGS)
class Type(Node):
    pos: Position = field(default_factory=Position, init=False, compare=False)
    type: str #type: ignore
    
    @property
    def basic_type(self):
        if self.is_reference():
            return self.type
        
        return self
    
    @staticmethod
    def from_llvm(file: File, ir_type: ir.Type):
        if isinstance(ir_type, ir.IntType):
            if ir_type.width == 1:
                return file.type_map.get('bool')
            elif ir_type.width == 32 or ir_type.width == 8:
                return file.type_map.get('int')
        elif isinstance(ir_type, ir.FloatType):
            return file.type_map.get('float')
        elif isinstance(ir_type, ir.VoidType):
            return file.type_map.get('nil')
        elif isinstance(ir_type, ir.IdentifiedStructType):
            return file.type_map.get(ir_type.name)
        elif isinstance(ir_type, ir.PointerType):
            return file.type_map.get('pointer')
        elif isinstance(ir_type, ir.LiteralStructType):
            return file.type_map.get('any')
        
        raise NotImplementedError
    
    def reference(self):
        return ReferenceType(self)
    
    def is_reference(self):
        return isinstance(self, ReferenceType)
    
    def __str__(self) -> str:
        return self.type

@dataclass(**NODE_KWARGS)
class ReferenceType(Type):
    type: Type # type: ignore
    
    def __eq__(self, other: object):
        if not isinstance(other, Type):
            return False
        
        return self.type == other
    
    def __ne__(self, other: object):
        if not isinstance(other, Type):
            return False
        
        return self.type != other
    
    def __str__(self) -> str:
        return f'{self.type}&'

@dataclass(**NODE_KWARGS)
class ClassType(Type):
    fields: list[Type] = field(default_factory=list, compare=False)
    
    @property
    def name(self):
        return self.type

    # def __str__(self) -> str:
    #     fields_str = ', '.join(map(str, self.fields))
    #     return f'{self.type}[{fields_str}]'

@dataclass(**NODE_KWARGS)
class ArrayType(Type):
    type: Type # type: ignore
    size: int | None = None

    def __str__(self) -> str:
        size = str(self.size) if self.size is not None else ''
        return f'{self.type}[{size}]'

@dataclass(**NODE_KWARGS)
class Program(TypelessNode):
    nodes: list[Node] = field(default_factory=list)
    
    def __str__(self) -> str:
        return '\n'.join(map(str, self.nodes))

@dataclass(**NODE_KWARGS)
class Comment(TypelessNode):
    text: str
    
    def __str__(self) -> str:
        return f'// {self.text}'

@dataclass(**NODE_KWARGS)
class Arg(Node):
    value: Any
    
    def __str__(self) -> str:
        return str(self.value)

@dataclass(kw_only=True, slots=True)
class ParamFlags:
    mutable: bool = False
    copy: bool = False

    def __str__(self) -> str:
        code = ''
        if self.copy:
            code += 'copy '

        if self.mutable:
            code += 'mut '

        return code

@dataclass(**NODE_KWARGS)
class Param(Node):
    name: str
    flags: ParamFlags = field(default_factory=ParamFlags)
    
    def to_symbol(self):
        return Symbol(self.name, self.type, self, SymbolFlags(mutable=self.flags.mutable))
    
    def __str__(self) -> str:
        return f'{self.flags}{self.type} {self.name}'

@dataclass(**NODE_KWARGS)
class Body(Node):
    nodes: list[Node] = field(default_factory=list)
    
    def __str__(self) -> str:
        return '\n'.join(map(str, self.nodes))

@dataclass(**NODE_KWARGS)
class Return(Node):
    value: Node | None = None
    
    def __str__(self) -> str:
        if self.value is None:
            return 'return'
        
        return f'return {self.value}'

@dataclass(**NODE_KWARGS)
class Property(Node):
    name: str
    getter_body: Body
    
    def __str__(self) -> str:
        return f"""{self.type} {self.name} => {{
{self.getter_body}
}}"""

@dataclass(**NODE_KWARGS)
class Field(Node):
    name: str

    def __str__(self) -> str:
        return f'{self.type} {self.name}'

@dataclass(**NODE_KWARGS)
class Class(TypelessNode):
    name: str
    members: list[Union['Function', 'Property', 'Field']] = field(default_factory=list)

    @property
    def fields(self):
        return [member for member in self.members if isinstance(member, Field)]
    
    def __str__(self) -> str:
        members_str = '\n'.join(map(str, self.members))
        return f"""class {self.name} {{
{members_str}
}}"""

@dataclass(kw_only=True, slots=True)
class FunctionFlags:
    static: bool = False
    property: bool = False
    method: bool = False
    returns_reference: bool = False
    
    def __str__(self):
        code = ''
        if self.static:
            code += 'static '
        
        if self.property:
            code += 'property '
        
        if self.method:
            code += 'method '

        if self.returns_reference:
            code += 'ret_ref '
        
        return code

@dataclass(**NODE_KWARGS)
class Function(Node):
    name: str
    params: list[Param] = field(default_factory=list)
    body: Body | Callable | None = None
    flags: FunctionFlags = field(default_factory=FunctionFlags)
    extend_type: Type | None = None
    generic_params: list[str] = field(default_factory=list)
    overloads: list['Function'] = field(default_factory=list)
    
    @property
    def ret_type(self):
        return self.type
    
    @property
    def is_generic(self):
        return len(self.generic_params) > 0
    
    @property
    def signature(self):
        params_str = ', '.join(map(str, self.params))
        extend_type = f'{self.extend_type}.' if self.extend_type is not None else ''
        generic_params = ('<' + ', '.join(self.generic_params) + '>') if self.is_generic else ''
        return f'{self.flags}fn {extend_type}{self.name}{generic_params}({params_str}) -> {self.ret_type}'

    @property
    def symbol_name(self):
        extend_type = f'{self.extend_type}.' if self.extend_type is not None else ''
        return f'{extend_type}{self.name}'
    
    def __str__(self) -> str:
        signature = self.signature
        if self.body is None:
            return signature

        body = str(self.body)
        if callable(self.body):
            signature = 'virtual ' + signature
            body = f'// a python interop function is called here (name = {self.body.__name__})'
        
        return f"""{signature} {{
{body}
}}"""

@dataclass(**NODE_KWARGS)
class Variable(Node):
    name: str
    value: Node
    is_mutable: bool = False
    op: str | None = None
    
    def to_id(self):
        return Id(self.pos, self.type, self.name)
    
    def __str__(self) -> str:
        mut = 'mut ' if self.is_mutable else ''
        return f'{mut}{self.type} {self.name} = {self.value}'

@dataclass(**NODE_KWARGS)
class Assignment(Node):
    name: str
    value: Node
    op: str | None = None
    attr: str | None = None
    
    def __str__(self) -> str:
        op = self.op or ''
        attr = f'.{self.attr}' if self.attr is not None else ''
        return f'{self.name}{attr} {op}= {self.value}'

@dataclass(**NODE_KWARGS)
class Elseif(TypelessNode):
    cond: Node
    body: Body
    
    def __str__(self) -> str:
        return f"""else if {self.cond} {{
{self.body}
}}"""

@dataclass(**NODE_KWARGS)
class If(TypelessNode):
    cond: Node
    body: Body
    else_body: Body | None = field(default=None)
    elseifs: list[Elseif] = field(default_factory=list)
    
    def __str__(self) -> str:
        else_body = f""" else {{
{self.else_body}
}}""" if self.else_body is not None else ''
        elseifs = '\n'.join(map(str, self.elseifs))
        return f"""if {self.cond} {{
{self.body}
}}{elseifs}{else_body}"""

@dataclass(**NODE_KWARGS)
class While(TypelessNode):
    cond: Node
    body: Body
    
    def __str__(self) -> str:
        return f"""while {self.cond} {{
{self.body}
}}"""

@dataclass(**NODE_KWARGS)
class ForRange(TypelessNode):
    iter_name: str
    start: Node
    end: Node
    body: Body
    step: Node | None = None
    
    def __str__(self) -> str:
        step = f'..{self.step}' if self.step is not None else ''
        return f"""for {self.iter_name} in {self.start}..{self.end}{step} {{
{self.body}
}}"""

@dataclass(**NODE_KWARGS)
class Foreach(TypelessNode):
    iter_name: str
    value: Node
    body: Body

    def __str__(self) -> str:
        return f"""foreach {self.iter_name} in {self.value} {{
{self.body}
}}"""

@dataclass(**NODE_KWARGS)
class Break(TypelessNode):
    def __str__(self) -> str:
        return 'break'

@dataclass(**NODE_KWARGS)
class Continue(TypelessNode):
    def __str__(self) -> str:
        return 'continue'

@dataclass(**NODE_KWARGS)
class Use(TypelessNode):
    path: str

    def use_byte_file(self, file: File, running_file: File, path: Path, current_pass_type: type):
        from byte.pipeline import Pipeline

        if file.path.stem == running_file.path.stem:
            return

        file.path = path
        pipeline = Pipeline()
        pipeline.end_at_pass(current_pass_type).run_passes(file)

        running_file.scope.symbol_table.merge(file.scope.symbol_table)
        running_file.type_map.merge(file.type_map)

    def use_py_file(self, file: File, running_file: File, path: Path):
        if path.parent.name != 'stdlib':
            module = import_module(f'byte.stdlib.{path.stem}.{path.stem}')
        else:
            module = import_module(f'byte.stdlib.{path.stem}')
        
        cls = getattr(module, path.stem)
        instance = cls(file)
        instance.init()
        for k, v in instance.intrinsics.items():
            ast_func = v.ast_func
            file.scope.symbol_table.add(Symbol(k, file.type_map.get('function'), ast_func))

        running_file.scope.symbol_table.merge(file.scope.symbol_table)
        running_file.type_map.merge(file.type_map)
    
    def __str__(self) -> str:
        return f'use "{self.path}"'

@dataclass(**NODE_KWARGS)
class Int(Node):
    value: int
    
    def __str__(self) -> str:
        return f'{self.value}'

@dataclass(**NODE_KWARGS)
class Float(Node):
    value: float
    
    def __str__(self) -> str:
        return f'{self.value}'

@dataclass(**NODE_KWARGS)
class String(Node):
    value: str
    
    def __str__(self) -> str:
        return f'"{self.value}"'

@dataclass(**NODE_KWARGS)
class StringPointer(Node):
    value: str
    
    def __str__(self) -> str:
        return f'p"{self.value}"'

@dataclass(**NODE_KWARGS)
class Bool(Node):
    value: bool
    
    def __str__(self) -> str:
        return f'{self.value}'.lower()

@dataclass(**NODE_KWARGS)
class Id(Node):
    name: str
    
    def to_ref(self):
        return Ref(self.pos, self.type.reference(), self.name)
    
    def __str__(self) -> str:
        return self.name

@dataclass(**NODE_KWARGS)
class Call(Node):
    callee: str
    args: list[Arg] = field(default_factory=list)
    
    def __str__(self) -> str:
        args_str = ', '.join(map(str, self.args))
        return f'{self.callee}({args_str})'

@dataclass(**NODE_KWARGS)
class Operation(Node):
    op: str
    left: Node
    right: Node
    
    def __str__(self) -> str:
        return f'{self.left} {self.op} {self.right}'

@dataclass(**NODE_KWARGS)
class UnaryOperation(Node):
    op: str
    value: Node
    
    def __str__(self) -> str:
        return f'{self.op}{self.value}'

@dataclass(**NODE_KWARGS)
class Ternary(Node):
    cond: Node
    true: Node
    false: Node
    
    def __str__(self) -> str:
        return f'{self.true} if {self.cond} else {self.false}'

@dataclass(**NODE_KWARGS)
class Bracketed(Node):
    value: Node
    
    def __str__(self) -> str:
        return f'({self.value})'

@dataclass(**NODE_KWARGS)
class Attribute(Node):
    value: Node
    attr: str
    args: list[Arg] | None = None
    
    def __str__(self) -> str:
        args_str = ', '.join(map(str, self.args or []))
        return f'{self.value}.{self.attr}({args_str})'

@dataclass(**NODE_KWARGS)
class New(Node):
    new_type: Type
    args: list[Arg] = field(default_factory=list)
    
    def __str__(self) -> str:
        args_str = ', '.join(map(str, self.args))
        return f'new {self.new_type}({args_str})'

@dataclass(**NODE_KWARGS)
class NewArray(Node):
    elem_type: Type
    size: int | None = None

    def __str__(self) -> str:
        size = str(self.size) if self.size is not None else ''
        return f'new {self.elem_type}[{size}]'

@dataclass(**NODE_KWARGS)
class Ref(Node):
    name: str
    
    def __str__(self) -> str:
        return f'&{self.name}'

@dataclass(**NODE_KWARGS)
class Deref(Node):
    name: str

    def __str__(self) -> str:
        return f'*{self.name}'


@dataclass(**NODE_KWARGS)
class StructLiteral(Node):
    name: str
    args: list[Node] = field(default_factory=list)
    
    def __str__(self) -> str:
        args_str = ', '.join(map(str, self.args))
        return f'struct<{self.name}>({args_str})'

@dataclass(**NODE_KWARGS)
class Null(Node):
    def __str__(self) -> str:
        return 'null'
