from dataclasses import dataclass, field
from abc import ABC
from datetime import datetime

import pandas as pd 



@dataclass
class PlateReaderData(ABC):
    file_path: str
    row_cutoff: str #i.e. "O"
    start_time: datetime = field(init=False)
    end_time: datetime = field(init=False)
    data: dict[str, float] = field(init=False)


    def __post_init__(self) -> None:
        df = self.load()
        df_trimmed = self.trimm(df=df, row_str=self.row_cutoff)

        self.start_time = self.get_time(df=df, time_str="Start Time")
        self.end_time = self.get_time(df=df, time_str="End Time")
        self.process(df_trimmed)
        #breakpoint()


    def load(self) -> pd.DataFrame:
        df = pd.read_excel(self.file_path)
        return df

    
    def process(self, df:pd.DataFrame) -> None:
        di = {}
        for row in df.index:
            for col in df.columns:
                di[f"{row}{col}"] = df.loc[row, col]

        self.data = di


    def trimm(self, df:pd.DataFrame, row_str:str) -> pd.DataFrame:
        header_offset = df[df.iloc[:,0]=="<>"].index[0]+1
        total_size = df.shape[0]
        try:
            footer_offset = total_size - df[df.iloc[:,0]==row_str].index[0]-1
        
            df_trimmed = pd.read_excel(self.file_path,
                        header = header_offset,
                        skipfooter = footer_offset,
                        usecols = range(0,25),
                        index_col=0)
        except Exception:
            breakpoint()
        u = df_trimmed.shape
        cop = df_trimmed.copy()
        df_trimmed = df_trimmed.dropna(axis="columns", thresh=1)
        #if df_trimmed.shape != u:
        #    breakpoint()
        return df_trimmed


    def get_time(self, df: pd.DataFrame, time_str:str) -> datetime:
        df_result = df.loc[df.iloc[:,0].str.contains(time_str, na=False)]
        time = df_result.iloc[:,1].values[0]

        return datetime.strptime(time, "%d.%m.%Y %H:%M:%S")