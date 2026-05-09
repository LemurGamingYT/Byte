from byte.intrinsics import IntrinsicLib
from byte.classes import init_class
from byte import ast


class fstream(IntrinsicLib):
    def init(self):
        string_type = self.file.type_map.get('string')
        
        class_members = init_class(ast.Position(), self.file, 'File', [
            ast.Property(ast.Position(), string_type, 'filename')
        ])

        for member in class_members:
            self.file.scope.symbol_table.add(ast.Symbol(member.name, self.file.type_map.get('function'), member))
