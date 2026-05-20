from byte.stdlib.builtins.classes.StringBuilder import StringBuilder
from byte.stdlib.builtins.operations import operations
from byte.stdlib.builtins.intrinsics import intrinsics
from byte.stdlib.builtins.classes.string import string
from byte.stdlib.builtins.classes.System import System
from byte.stdlib.builtins.classes.float import float
from byte.stdlib.builtins.registry import registry
from byte.stdlib.builtins.classes.bool import bool
from byte.stdlib.builtins.classes.Math import Math
from byte.stdlib.builtins.classes.int import int
from byte.intrinsics import IntrinsicLib


class builtins(IntrinsicLib):
    def init(self):
        self.add(registry)
        self.add(operations)
        self.add(intrinsics)
        self.add(int)
        self.add(float)
        self.add(string)
        self.add(bool)
        self.add(Math)
        self.add(System)
        self.add(StringBuilder)
