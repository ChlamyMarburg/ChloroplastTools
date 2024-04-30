import json
import pandas as pd 

from config import config
from absorbance import AbsorbanceConstructor
from echo import EchoConstructor
from luminescence import LuminescenceBuilder


'''
ABSORBANCE_SHEET = "raw_data/Absorbance_HSM_Plate_1_Light.xlsx"
ECHO_SHEET = "raw_data/EchoScript_HSM_Plate_1_Light.csv"
NLUC_SHEETS = [
    "raw_data/Nluc_HSM_Light_1_1.xlsx",
    "raw_data/Nluc_HSM_Light_1_2.xlsx",
    "raw_data/Nluc_HSM_Light_1_3.xlsx"
]
MEDIUM = "HSM"
CONDITION = "Light"
PLATE_ID = 1
'''



def main():
    echo = EchoConstructor(config.ECHO_SHEET)
    absorbance = AbsorbanceConstructor(config.ABSORBANCE_SHEET)
    luminescence = LuminescenceBuilder(config.NLUC_SHEETS)
    with open(config.MAPPING) as file:
        mapping = json.load(file)

    search_plate = lambda x: next(item for item in mapping if item["plate_id"] == x)
    search_construct = lambda x,y: next(item for item in x["constructs"] if item["column"] == y)
    od_normal = lambda x,y: x*(y/10_000)     

    result_data = []
    for step in echo.echo_steps:
        buffer = search_plate(config.PLATE_ID)
        #breakpoint()
        try:
            constr = search_construct(buffer, int(step.source_well[1:]))
        except:
            breakpoint()
        lumi = luminescence.measurements[step.dest_plate]
        #breakpoint()
        #try:
        result_buffer = {
            "alias": constr["alias"],
            "start_time_luminescence": lumi.start_time,
            "start_time_absorbance": absorbance.start_time,
            "end_time_luminescence": lumi.end_time,
            "end_time_absorbance": absorbance.end_time,
            "plate_id_agar": config.PLATE_ID,
            "plate_id_echo": step.dest_plate,
            "medium": config.MEDIUM,
            "condition": config.CONDITION,
            "well_echo": step.source_well,
            "well_agar": step.dest_well,
            "construct_name": constr["name"],
            "absorbance": absorbance.data[step.source_well],
            "transfer_vol": step.transfer_vol,
            "final_od": od_normal(absorbance.data[step.source_well], step.transfer_vol),
            "luminescence_raw": luminescence.measurements[step.dest_plate].data[step.dest_well],
            "luminescence_normalized": "",
            "protein_yield": ""
            }
        #except KeyError:
        #    breakpoint()
        result_data.append(result_buffer)

    
    df = pd.DataFrame.from_dict(result_data)
    df.to_csv("test_result_2_A2.csv", index=False)


if __name__ == "__main__":
    main()