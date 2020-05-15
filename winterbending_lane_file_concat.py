'''
This file concatenates the winter bending files into one for each of 
the 4 lanes,

Note: this was created to solve a problem we had using bash scripts
with this particular data set.  It is a little more "safe"
than just the typical concat * >> concat.fastq as it gives
size outputs and what it's reading, but it is not faster.  The
speed difference, however, is pretty negligible as this ran quickly
on hundreds of 4+gb files.  It is mostly hampered
by the screen output, which, again, is the point of it.

Thomas Horn
2020
Tsai Labs (UGA)
'''

import sys
import os

base_dir = os.getcwd() # Testing Site: "/scratch/twh58439/winterbend_2018/fastq/R1"
letters = ["O", "S", "T"]
dir_contents = os.listdir(base_dir)

# Check for R1 vs (optional) R2 paired end flags.
if len(sys.argv) > 2:
    print("Incorrect argument number.  Use R2 to signify R2 reads")
    sys.exit(1)

flag = "R1"
if len(sys.argv) == 2 and sys.argv[1].upper() == "R2":
    flag = "R2"

# Only 3 letter choices
for letter in letters: #letters:
    # First number goes from 2 to 4
    for i in range(2, 5):

        # First number ranges from 1 to 6 and is used to create the new file.
        # The new file does not need the innermost number as that would defeat
        # the point of this.
        for j in range(1, 7):
            # SX# only needs to go up to 4.  Skip iterations if needed
            if letter == "S" and j > 4:
                continue

            name = f"{letter}X{i}_{j}_concat_{flag}.fastq.gz"
            file_size = []
            
            # Check for existing file as ab will just append onto it
            if os.path.exists(name):
                input = ("Removing existing file? y/n")
                if input.upper == "Y":
                    os.remove(name)


            # Last number ranges from 1 to 4
            for k in range(1, 5):
                fname = f"{letter}X{i}_{j}_L00{k}_{flag}.fastq.gz"
                print("reading " + fname)
                
                # Get file size and append it to be later summed
                file_size.append(os.stat(fname).st_size)

                # Append lines to the concatenated file
                with open(os.path.join(fname), 'rb') as infile,\
                     open(os.path.join(name), 'ab+') as outfile:
                    lines = infile.readlines()  
                    for line in lines:
                        outfile.write(line)

            # Check File Size Comparison
            file_sum = sum(file_size)
            new_sum = os.stat(name).st_size

            print(f"L00 Sizes: {file_sum}")
            print(f"New Size:  {new_sum}")

            if not file_sum == new_sum:
                print("Mismatched files.  Are you sure you're not appending\
                        onto an existing file accidentially?")
                sys.exit(1)
            else:
                print("Concatenation successful")
