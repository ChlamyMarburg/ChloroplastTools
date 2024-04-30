import logging
from datetime import datetime

import config
import calc
import destination
import source




logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
    datefmt='%d-%m %H:%M:%S',
    filename='report.log')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logging.getLogger('').addHandler(console)

def main() -> None:
    source.Water(
        plate_id=len(config.od_measurements)+1, 
        position=calc.num2well(config.water_counter)) # initialize first water well

    dest = destination.Plate(plate_id=config.dest_plate_cnt)
    for idx, filename in enumerate(config.od_measurements):
        s = source.Plate(plate_id=idx+1, source_file=filename)
        s.process()

        for sw in s.target_wells:
            for tr in range(config.tech_repl):
                if not dest.available():
                    logging.info(f"Current destination plate {dest.plate_id} is full")
                    config.dest_plate_cnt += 1
                    dest = destination.Plate(plate_id=config.dest_plate_cnt)
                    breakpoint

                dest.fill_well(sw)

    logging.info("Beginning to generate echo script")
    header = "Source Plate Name,Source Plate Type,Source Well,Destination Plate Name,Destination Well,Transfer Volume\n"
    now = datetime.now().strftime('%Y%m%d_%H%M%S')
    echo_filename = f"EchoScript_{now}.csv"
    with open(echo_filename, "w") as file:
        logging.info(f"Created new echo script {echo_filename}")
        file.write(header)
        for dest in destination.Plate.destination_list:
            for well in dest.wells:
                cs, ws = well.repr()
                file.write(cs)
                file.write(ws)
    logging.info("Finished writing the echo script")



if __name__ == "__main__":
    logging.info("Started logging")
    config.load()
    main()