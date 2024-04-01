from .addition_operation import AdditionOperation
from .and_operation import AndOperation
from .divide_operation import DivideOperation
from .equality_operation import EqualityOperation
from .greater_equal_operation import GreaterEqualOperation
from .greater_operation import GreaterOperation
from .modulo_operation import ModuloOperation
from .multiplying_operation import MultiplyingOperation
from .not_equal_operation import NotEqualOperation
from .or_operation import OrOperation
from .power_operation import PowerOperation
from .smaller_equal_operation import SmallerEqualOperation
from .smaller_operation import SmallerOperation
from .subtraction_operation import SubtractionOperation
from .xor_operation import XorOperation

ORDERED_PAIR_VALUES_OPERATIONS = [
    PowerOperation(),
    MultiplyingOperation(),
    DivideOperation(),
    ModuloOperation(),
    AdditionOperation(),
    SubtractionOperation(),
    EqualityOperation(),
    GreaterEqualOperation(),
    GreaterOperation(),
    SmallerEqualOperation(),
    SmallerOperation(),
    NotEqualOperation(),
    AndOperation(),
    OrOperation(),
    XorOperation()
]
