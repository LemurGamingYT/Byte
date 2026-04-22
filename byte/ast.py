from dataclasses import dataclass, field
from contextlib import contextmanager
from abc import ABC, abstractmethod
from sys import exit as sys_exit
from logging import info, error
from typing import Union, Any
from pathlib import Path

from colorama import Fore, Style
from llvmlite import ir


STDLIB_PATH = Path(__file__).parent / 'stdlib'

@dataclass
class Position:
    line: int = 0
    column: int = 0

    def comptime_error(self, file: 'File', message: str):
        print(file.src.splitlines()[self.line - 1])
        print(' ' * self.column + '^')
        print(f'{Style.BRIGHT}{Fore.RED}error: {message}{Style.RESET_ALL}')
        error(message)
        sys_exit(1)

@dataclass
class Symbol:
    name: str
    type: 'Type'
    value: Any
    is_mutable: bool = False
    public: bool = True

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
            non_static_symbols = {k: v for k, v in other.symbols.items() if v.public}
            self.symbols.update(non_static_symbols)
                 
@dataclass
class TypeMap:
    types: dict[str, 'Type'] = field(default_factory=dict)
    
    def get(self, name: str):
        return self.types[name]
                 
    def tryget(self, name: str):
        return self.types.get(name)
                 
    def add(self, typ: str):
        self.types[typ] = Type(typ)
    
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

@dataclass
class File:
    path: Path
    scope: Scope = field(default_factory=Scope)
    type_map: TypeMap = field(default_factory=TypeMap)
    dependencies: list[Path] = field(default_factory=list)
    
    @property
    def unique_name(self):
        self._unique_name_idx += 1
        return f'_{self._unique_name_idx}'
    
    def __post_init__(self):
        self._unique_name_idx = -1
        self.src = self.path.read_text()
        
        self.type_map.add('int')
        self.type_map.add('float')
        self.type_map.add('bool')
        self.type_map.add('nil')
        
        self.type_map.add('string')
        self.type_map.add('Math')
        
        self.type_map.add('any')
        self.type_map.add('pointer')
        self.type_map.add('function')
    
    @contextmanager
    def child_scope(self):
        outer_scope = self.scope
        self.scope = self.scope.clone()
        info('entering child scope')
        yield
        self.scope = outer_scope


@dataclass
class Node(ABC):
    pos: Position
    type: 'Type'
    
    def to_arg(self):
        return Arg(self.pos, self.type, self)
    
    @abstractmethod
    def __str__(self) -> str:
        ...

@dataclass
class TypelessNode(Node, ABC):
    type: 'Type' = field(default_factory=lambda: Type('any'), init=False, repr=False, compare=False)

@dataclass
class Type(Node):
    pos: Position = field(default_factory=Position, init=False, compare=False)
    type: str #type: ignore
    
    @staticmethod
    def from_llvm(file: File, ir_type: ir.Type):
        if isinstance(ir_type, ir.IntType):
            if ir_type.width == 1:
                return file.type_map.get('bool')
            elif ir_type.width == 32:
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
    
    def __str__(self) -> str:
        return self.type

@dataclass
class Program(TypelessNode):
    nodes: list[Node] = field(default_factory=list)
    
    def __str__(self) -> str:
        return '\n'.join(map(str, self.nodes))

@dataclass
class Comment(TypelessNode):
    text: str
    
    def __str__(self) -> str:
        return f'// {self.text}'

@dataclass
class Arg(Node):
    value: Node
    
    def __str__(self) -> str:
        return str(self.value)

@dataclass
class Param(Node):
    name: str
    is_mutable: bool = False
    
    def to_symbol(self):
        return Symbol(self.name, self.type, self, self.is_mutable)
    
    def __str__(self) -> str:
        return f'{self.type} {self.name}'

@dataclass
class Body(Node):
    nodes: list[Node] = field(default_factory=list)
    
    def __str__(self) -> str:
        return '\n'.join(map(str, self.nodes))

@dataclass
class Return(Node):
    value: Node | None = None
    
    def __str__(self) -> str:
        if self.value is None:
            return 'return'
        
        return f'return {self.value}'

@dataclass(kw_only=True)
class FunctionFlags:
    static: bool = False
    property: bool = False
    method: bool = False
    
    def __str__(self):
        code = ''
        if self.static:
            code += 'static '
        
        if self.property:
            code += 'property '
        
        if self.method:
            code += 'method '
        
        return code

@dataclass
class Function(Node):
    name: str
    params: list[Param] = field(default_factory=list)
    body: Body | None = None
    flags: FunctionFlags = field(default_factory=FunctionFlags)
    extend_type: Type | None = None
    overloads: list['Function'] = field(default_factory=list)
    
    @property
    def ret_type(self):
        return self.type
    
    def __str__(self) -> str:
        params_str = ', '.join(map(str, self.params))
        extend_type = f'{self.extend_type}.' if self.extend_type is not None else ''
        signature = f'{self.flags}fn {extend_type}{self.name}({params_str}) -> {self.ret_type}'
        if self.body is None:
            return signature
        
        return f"""{signature} {{
{self.body}
}}"""

@dataclass
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

@dataclass
class Assignment(Node):
    name: str
    value: Node
    op: str | None = None
    
    def __str__(self) -> str:
        op = self.op or ''
        return f'{self.name} {op}= {self.value}'

@dataclass
class Elseif(TypelessNode):
    cond: Node
    body: Body
    
    def __str__(self) -> str:
        return f"""else if {self.cond} {{
{self.body}
}}"""

@dataclass
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

@dataclass
class While(TypelessNode):
    cond: Node
    body: Body
    
    def __str__(self) -> str:
        return f"""while {self.cond} {{
{self.body}
}}"""

@dataclass
class Break(TypelessNode):
    def __str__(self) -> str:
        return 'break'

@dataclass
class Continue(TypelessNode):
    def __str__(self) -> str:
        return 'continue'

@dataclass
class Use(TypelessNode):
    path: str
    
    def __str__(self) -> str:
        return f'use "{self.path}"'

@dataclass
class Defer(TypelessNode):
    expr: Node
    
    def __str__(self) -> str:
        return f'defer {self.expr}'

@dataclass
class Int(Node):
    value: int
    
    def __str__(self) -> str:
        return f'{self.value}'

@dataclass
class Float(Node):
    value: float
    
    def __str__(self) -> str:
        return f'{self.value}'

@dataclass
class String(Node):
    value: str
    
    def __str__(self) -> str:
        return f'"{self.value}"'

@dataclass
class StringPointer(Node):
    value: str
    
    def __str__(self) -> str:
        return f'p"{self.value}"'

@dataclass
class Bool(Node):
    value: bool
    
    def __str__(self) -> str:
        return f'{self.value}'.lower()

@dataclass
class Id(Node):
    name: str
    
    def __str__(self) -> str:
        return self.name

@dataclass
class Call(Node):
    callee: str
    args: list[Arg] = field(default_factory=list)
    
    def __str__(self) -> str:
        args_str = ', '.join(map(str, self.args))
        return f'{self.callee}({args_str})'

@dataclass
class Operation(Node):
    op: str
    left: Node
    right: Node
    
    def __str__(self) -> str:
        return f'{self.left} {self.op} {self.right}'

@dataclass
class UnaryOperation(Node):
    op: str
    value: Node
    
    def __str__(self) -> str:
        return f'{self.op}{self.value}'

@dataclass
class Ternary(Node):
    cond: Node
    true: Node
    false: Node
    
    def __str__(self) -> str:
        return f'{self.true} if {self.cond} else {self.false}'

@dataclass
class Bracketed(Node):
    value: Node
    
    def __str__(self) -> str:
        return f'({self.value})'

@dataclass
class Attribute(Node):
    value: Node
    attr: str
    args: list[Arg] | None = None
    
    def __str__(self) -> str:
        args_str = ', '.join(map(str, self.args or []))
        return f'{self.value}.{self.attr}({args_str})'

@dataclass
class New(Node):
    new_type: Type
    args: list[Arg] = field(default_factory=list)
    
    def __str__(self) -> str:
        args_str = ', '.join(map(str, self.args))
        return f'new {self.new_type}({args_str})'
