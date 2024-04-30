from dataclasses import dataclass


# Replace with a json file ? 
@dataclass
class config:
    ABSORBANCE_SHEET = "3UTR_measurement/raw_data/Absorbance_Plate_2_A2.xlsx"
    ECHO_SHEET = "3UTR_measurement/raw_data/EchoScript_Plate_2_A2.csv"
    NLUC_SHEETS = [
        "3UTR_measurement/raw_data/Plate_2_1_A2_Nanoluc.xlsx",
        "3UTR_measurement/raw_data/Plate_2_2_A2_Nanoluc.xlsx",
        #"3UTR_measurement/raw_data/Plate_1_3_A2_Nanoluc.xlsx",
    ]
    MEDIUM = "TAP"
    CONDITION = "Light"
    PLATE_ID = 4
    MAPPING = "3UTR_measurement/mapping_3UTR.json"