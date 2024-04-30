from dataclasses import dataclass, field
from datetime import datetime

import pandas as pd 

from platereader import PlateReaderData


@dataclass
class AbsorbanceConstructor(PlateReaderData):
    row_cutoff: str = "O"
