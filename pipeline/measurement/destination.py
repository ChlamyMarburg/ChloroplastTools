import attr
import logging

import calc
import config
import source



@attr.s 
class Plate():
    destination_list = []
    plate_id: str = attr.ib(converter=str)
    wells: list["Well"] = attr.ib(init=False)
    full: bool = attr.ib(init=False)
    allowed_wells: list[int] = attr.ib(init=False)
    

    def __attrs_post_init__(self):
        allowed_wells = []
        for i in range(12):
            for x in range(0,16,2):
                num = x+32*i
                if not ((num % (14+32*i) == 0) and num!=0):
                    allowed_wells.append(num)
        self.allowed_wells = allowed_wells            
        self.full = False
        self.wells = []
        Plate.destination_list.append(self)
        logging.info(f"Successfully generated destination plate {self.plate_id}")
        return self

    def available(self) -> bool:
        if not len(self.allowed_wells)>0:
            self.full = True
            return False
        return True

    def fill_well(self, source:source.Well) -> None:
        current_well = self.allowed_wells.pop(0)
        cell_vol_exact = calc.od_volume(source.od)
        cell_vol = calc.round_volume(cell_vol_exact)
        position = calc.num2well(current_well)
        well = Well(cell_vol=cell_vol, position=position, source_well=source, plate_id=self.plate_id)
        self.wells.append(well)


@attr.s
class Well():
    cell_vol: int = attr.ib(converter=int)
    water_fillup: int = attr.ib(converter=int, init=False)
    position: str = attr.ib(converter=str)
    source_well: source.Well = attr.ib()
    water_well: source.Water = attr.ib(init=False)
    plate_id: str = attr.ib(converter=str)
    water_prefill:int = attr.ib(default=config.pre_vol)

    def __attrs_post_init__(self):
        self.water_fillup = calc.h2o_topup(self.cell_vol)
        if source.Water.water_wells[-1].current_vol < self.water_fillup:
            config.water_counter += 1
            source.Water(plate_id=len(config.od_measurements)+1, 
                            position=calc.num2well(config.water_counter))

        self.water_well = source.Water.water_wells[-1]
        self.water_well.current_vol -= self.water_fillup

        return self

    # string representation to write to echo
    def repr(self) -> tuple[str, str]:
        #"Source Plate Name,Source Plate Type,Source Well,Destination Plate Name,Destination Well,Transfer Volume\n"
        step1 = f"{self.source_well.plate_id},384PP_Plus_AQ_SP,{self.source_well.position},{self.plate_id},{self.position},{self.cell_vol},Cells\n"
        step2 = f"{self.water_well.plate_id},384PP_Plus_AQ_SP,{self.water_well.position},{self.plate_id},{self.position},{self.water_fillup},Water\n"

        return step1, step2