from .absolute_operation import AbsoluteOperation
from .average_operation import AverageOperation
from .concat_operation import ConcatOperation
from .count_operation import CountOperation
from .countif_operation import CountIfOperation
from .if_operation import IfOperation
from .length_operation import LengthOperation
from .ln_operation import LnOperation
from .log_operation import LogOperation
from .lookup_operation import LookupOperation
from .max_opeartion import MaxOperation
from .median_operation import MedianOperation
from .min_operation import MinOperation
from .round_operation import RoundOperation
from .sqrt_operation import SqrtOperation
from .summary_operation import SummaryOperation
from .truncate_operation import TruncateOperation

REDUCE_OPERATIONS = [
    AverageOperation(),
    MaxOperation(),
    MinOperation(),
    MedianOperation(),
    RoundOperation(),
    SqrtOperation(),
    SummaryOperation(),
    LogOperation(),
    LnOperation(),
    LookupOperation(),
    CountIfOperation(),
    LengthOperation(),
    CountOperation(),
    IfOperation(),
    AbsoluteOperation(),
    ConcatOperation(),
    TruncateOperation()
]
