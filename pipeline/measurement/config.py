import os 
import logging



def load():
    global pre_vol
    global total_vol
    global target_od
    global tech_repl
    global bio_repl
    global echo_work_vol
    global od_measurements
    global water_counter
    global dest_plate_cnt 

    pre_vol = 8_000
    total_vol = 10_000
    target_od = 0.01
    tech_repl = 3
    bio_repl  = 7 
    echo_work_vol = 35_000 # total_vol - dead_vol
    water_counter = 0
    dest_plate_cnt = 1
    od_measurements = ["ODs/Plate_2_A2_absorbance.xlsx"] 

    for file in od_measurements:
        assert os.path.isfile(file), logging.error(f"Can't find the file {file}")
    
    logging.info("Successfully loaded all config parameters")