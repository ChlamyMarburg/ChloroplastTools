from dataclasses import dataclass, field
import pandas as pd 



@dataclass
class EchoStep:
    source_well: str
    dest_plate: int
    dest_well: str
    transfer_vol: int


@dataclass
class EchoConstructor:
    file_path: str
    df: pd.DataFrame = field(init=False)
    echo_steps: list[EchoStep] = field(init=False)

    def __post_init__(self) -> None:
        self.load()
        self.process()

    def load(self) -> None:
        ECHO_HEADER = ["Source Plate Name","Source Plate Type","Source Well","Destination Plate Name","Destination Well","Transfer Volume","Comment"]
        self.df = pd.read_csv(self.file_path, header=None, skiprows=1)
        self.df.columns = ECHO_HEADER

    def process(self) -> None:
        data = []
        for _, row in self.df[self.df["Source Plate Name"]==1].iterrows():
            buffer = EchoStep(
                source_well = row["Source Well"],
                dest_plate = row["Destination Plate Name"],
                dest_well = row["Destination Well"],
                transfer_vol = row["Transfer Volume"]
            )
            data.append(buffer)
        self.echo_steps = data