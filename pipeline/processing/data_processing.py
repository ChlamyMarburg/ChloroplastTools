import json
import pandas as pd 

#from config import config
from absorbance import AbsorbanceConstructor
from echo import EchoConstructor
from luminescence import LuminescenceBuilder



def main():

    for medium in ["HSM", "TAP"]:
        for condition in ["Light", "Dark"]:
            for plate_id in [1,2,3]:

                echo = EchoConstructor(f"raw_data/EchoScript_{medium}_Plate_{plate_id}_{condition}.csv")
                absorbance = AbsorbanceConstructor(f"raw_data/Absorbance_{medium}_Plate_{plate_id}_{condition}.xlsx")
                NLUC_SHEETS = [
                    f"raw_data/Nluc_{medium}_{condition}_{plate_id}_1.xlsx",
                    f"raw_data/Nluc_{medium}_{condition}_{plate_id}_2.xlsx",
                    f"raw_data/Nluc_{medium}_{condition}_{plate_id}_3.xlsx"
                ]
                luminescence = LuminescenceBuilder(NLUC_SHEETS)
                with open("mapping.json") as file:
                    mapping = json.load(file)

                search_plate = lambda x: next(item for item in mapping if item["plate_id"] == x)
                search_construct = lambda x,y: next(item for item in x["constructs"] if item["column"] == y)
                od_normal = lambda x,y: x*(y/10_000)     

                result_data = []
                for step in echo.echo_steps:
                    buffer = search_plate(plate_id)
                    constr = search_construct(buffer, int(step.source_well[1:]))
                    lumi = luminescence.measurements[step.dest_plate]

                    result_buffer = {
                        "alias": constr["alias"],
                        "start_time_luminescence": lumi.start_time,
                        "start_time_absorbance": absorbance.start_time,
                        "end_time_luminescence": lumi.end_time,
                        "end_time_absorbance": absorbance.end_time,
                        "plate_id_agar": plate_id,
                        "plate_id_echo": step.dest_plate,
                        "medium": medium,
                        "condition": condition,
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
                    result_data.append(result_buffer)

                
                df = pd.DataFrame.from_dict(result_data)
                df.to_csv(f"result/{medium}_{condition}_{plate_id}.csv", index=False)


if __name__ == "__main__":
    main()