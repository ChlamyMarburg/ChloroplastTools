import attr
import logging
import pandas as pd

import config
import calc



@attr.s
class Plate():
    source_list = []
    total_wells: pd.DataFrame = attr.ib(init=False)
    target_wells: list["Well"] = attr.ib(init=False)
    plate_id: str = attr.ib(converter=str, kw_only=True)
    source_file: str = attr.ib(converter=str, kw_only=True)

    def __attrs_post_init__(self):
        self.target_wells = []
        df = pd.read_excel(self.source_file)
        
        # calculate offsets
        header_offset = df[df.iloc[:,0]=="<>"].index[0]+1
        total_size = df.shape[0]
        footer_offset = total_size - df[df.iloc[:,0]=="O"].index[0]-1
        
        # load the correct od matrix
        self.total_wells = pd.read_excel(self.source_file,
                        header = header_offset,
                        skipfooter = footer_offset,
                        usecols = range(1,25))

        Plate.source_list.append(self)
        logging.info(f"Successfully loaded source plate {self.plate_id}")

        return self
        

    def process(self) -> None:
        logging.info(f"Starting to process source plate {self.plate_id}")
        for col in self.total_wells:
            # take top biological replicates w/ highest OD
            top_bio = self.total_wells[col].nlargest(config.bio_repl)
            
            if min(top_bio) < 0.1:
                logging.warning(f"WARNING, minimum OD {min(top_bio)} for column {col} is lower than the defined threshold")

            for index, value in top_bio.items():
                target_well = Well(od=value, position=calc.pos2well(col, index), plate_id=self.plate_id)
                self.target_wells.append(target_well)
            
        logging.info(f"Finished processing source plate {self.plate_id}")


@attr.s
class Well():
    source_well_list = []
    #start_volume: int = attr.ib(converter=int)
    od: float = attr.ib(converter=float)
    position: str = attr.ib(converter=str)
    plate_id: str = attr.ib(converter=str)

    def __attrs_post_init__(self):
        Well.source_well_list.append(self)
        return self


@attr.s
class Water():
    water_wells = []
    plate_id:str = attr.ib(converter=str)
    position:str = attr.ib(converter=str)
    current_vol:int = attr.ib(converter=int, default=config.echo_work_vol)

    def __attrs_post_init__(self):
        Water.water_wells.append(self)
        logging.info(f"Generated new water well on position {self.position}")