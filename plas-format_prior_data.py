"""                                                                                                                          
Thomas Horn                                                                                                                  
Tsai Lab                                                                                                                     
PLAS Project                                                                                                                 
                                                                                                                             
This is a very simple script used to format proteomes and transcriptome .fa files.                                           
                                                                                                                             
Reference sequence proteomes and transcriptomes come in the format:                                                          
>ATCG00500.1 pacid=37375748 transcript=ATCG00500.1 locus=ATCG00500 ID=ATCG00500.1.Araport11.447 annot-version=Araport11      
[sequence]                                                                                                                   
                                                                                                                             
In order to match the gene of interest format in GeneOfInterest.txt the excess information                                   
must be eliminated.  Additionally, to eliminate any redundency, anything after the primary                                   
sequence (the line after .) is removed.                                                                                      
                                                                                                                             
This works for both proteomes and transcriptomes.                                                                            
                                                                                                                             
Usage: simply run the script with an input file and type of file (protoeome or transcriptome) as arguments.                  
  python3 format_prior_data.py file filetype                                                                                 
                                                                                                                             
Output: proteome.fa or transcriptome.fa                                                                                      
"""                                                                                                                          
                                                                                                                             
import sys                                                                                                                   
import os                                                                                                                    
                                                                                                                             
# Verify command line arguments                                                                                              
if len(sys.argv) != 3:                                                                                                       
    print("Error: enter the correct number of arguments.")                                                                   
    sys.exit(1)                                                                                                              
                                                                                                                             
if sys.argv[2] not in ["transcriptome", "proteome"]:                                                                         
    print("Please enter a valid file type.")                                                                                 
    sys.exit(1)                                                                                                              
                                                                                                                             
# Assign filenames for context manager                                                                                       
inputFile = sys.argv[1]                                                                                                      
outputFile = sys.argv[2] + ".fa"                                                                                             
                                                                                                                             
with open(inputFile, 'r') as infile, open(outputFile, 'w+') as outfile:                                                      
    lines = infile.readlines()                                                                                               
                                                                                                                             
    # We only need to edit lines that begin with '>' and remove anything after the first '.'                                 
    for line in lines:                                                                                                       
        if line[0] == '>':                                                                                                   
            # Split the line on '.' and only grab the first chunk containing the gene sequence                               
            new_line = line.split('.')                                                                                       
            outfile.write(new_line[0] + os.linesep)  # need to give this a line separator                                    
        else:                                                                                                                
            outfile.write(line)                                                                                              
