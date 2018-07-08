"""
This script automatically processes any MTA turnstile files added to the data/ folder
"""

from os import listdir
from os.path import join, isfile
from make_Benson_csv import make_Benson_csv

datafolder = 'data'
for filename in [f for f in listdir(datafolder) if (isfile(join(datafolder, f)) and f[-4:] == ".txt")]:
    input_filepath = join(datafolder, filename)
    output_filepath = join('BensonData', filename[-10:-4] + ".csv")

    print(input_filepath)
    print(output_filepath)

    if (isfile(output_filepath)):
        print("{} already exists! Skipping...".format(output_filepath))
        continue

    make_Benson_csv(input_filepath, output_filepath)