from dataclasses import dataclass, field

from platereader import PlateReaderData



@dataclass 
class LuminescenceConstructor(PlateReaderData):
    plate_id: int = None
    row_cutoff: str = "M"


@dataclass 
class LuminescenceBuilder:
    nluc_sheets: list[str] 
    measurements: dict[int, LuminescenceConstructor] = field(init=False)

    def __post_init__(self) -> None:
        self.build()

    def build(self) -> None:
        di = {}
        for idx, file_path in enumerate(self.nluc_sheets):
                di[idx+1] = LuminescenceConstructor(
                        file_path = file_path,
                        plate_id = idx+1
                    )
        self.measurements = di