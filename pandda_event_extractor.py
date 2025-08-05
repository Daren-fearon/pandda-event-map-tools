import sys
import subprocess
import glob
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(message)s'
)

def split_cif(cif):
    cif_new = os.path.splitext(os.path.basename(cif))[0]

    ref_data_block = None
    ori_data_block = None
    pandda_event_block = None

    # Detect data block names
    with open(cif, 'r') as f:
        for line in f:
            if line.startswith('data_'):
                if 'Bsf' in line and not pandda_event_block:
                    pandda_event_block = line.strip()
                elif 'Asf' in line and not ori_data_block:
                    ori_data_block = line.strip()
                elif 'sf' in line and not ref_data_block:
                    ref_data_block = line.strip()

    if not (ref_data_block and ori_data_block and pandda_event_block):
        logging.error(f"Could not detect all required data blocks in {cif}")
        return None

    block = 'data'
    with open(cif_new + '_data.cif', 'w') as b1, open(cif_new + '_pandda_event.cif', 'w') as b2, open(cif, 'r') as f1:
        for line in f1:
            if line.startswith('data_'):
                if line.strip() in [ref_data_block, ori_data_block]:
                    block = 'data'
                elif line.strip() == pandda_event_block:
                    block = 'pandda'
                else:
                    block = 'other'
            if block == 'data':
                b1.write(line)
            elif block == 'pandda':
                b2.write(line)

    logging.info(f"Split completed for {cif}")
    return cif_new

def convert_to_mtz(cif_new, space_group=None):
    try:
        cmd1 = ['phenix.cif_as_mtz', f'{cif_new}_data.cif', '--extend_flags']
        cmd2 = ['phenix.cif_as_mtz', f'{cif_new}_pandda_event.cif', '--extend_flags']
        if space_group:
            cmd2 += [f'space_group={space_group}']

        result1 = subprocess.run(cmd1, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        logging.info(result1.stdout)
        if result1.stderr:
            logging.warning(result1.stderr)

        result2 = subprocess.run(cmd2, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        logging.info(result2.stdout)
        if result2.stderr:
            logging.warning(result2.stderr)

        logging.info(f"Conversion to MTZ completed for {cif_new}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error during conversion for {cif_new}: {e.stderr}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        logging.error("Usage: python /dls/science/groups/i04-1/software/scripts/event_map_extractor/pandda_event_extractor.py <*sf.mmcif> [space_group=XXX]")
        sys.exit(1)

    space_group = None
    cif_files = []

    for arg in sys.argv[1:]:
        if arg.startswith("space_group="):
            space_group = arg.split("=")[1]
        else:
            cif_files.extend(glob.glob(arg))

    if not cif_files:
        logging.error("No CIF files provided.")
        sys.exit(1)

    for cif in cif_files:
        cif_new = split_cif(cif)
        if cif_new:
            convert_to_mtz(cif_new, space_group)
