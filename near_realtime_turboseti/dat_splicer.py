#This notebook is a prototype for a script that will splice individual
#UFUDs into UFSD files. 

#Ellie White, 26 Jan 2021

import numpy as np
import pylab as plt
import sys
import pandas as pd
from astropy.io import ascii

np.set_printoptions(threshold= sys.maxsize)
pd.set_option('display.max_rows', None)

#first, read in the .dat files for the first scan in the cadence:
#Need to figure out how to make the filenames more general or at least 
#how to make them work for running on the GBO machine

nodes_list = ['00', '01']

filenames_list = []

for node in nodes_list:
    filename = '/home/ellie/research/seti/dat_files/'\
               'blc{0}_guppi_59046_80036_DIAG_VOYAGER-1_0011.rawspec.0000.dat'.format(node)
    filenames_list.append(filename)

#########################################
# THIS IS THE MAIN PART OF THE CODE
#########################################

########################################
# Read the info from all the files to 
# create the spliced DataFrame
########################################

fname_idx = 0
file_ids = []

for fname in filenames_list:

    #replace \t with space character 
    #so ascii can use space as a delimiter
    f1 = open(fname, 'r')
    content = f1.read()
    f1.close()

    content = content.replace('\t',' ')

    f2 = open(fname+'.mod', 'w')
    f2.write(content)
    f2.close()

    #now read in the table
    ufud = ascii.read(fname+'.mod', format='commented_header', header_start=7, delimiter=' ')
    ufud = ufud.to_pandas()
    ufud = ufud.apply(pd.to_numeric)

    #create the spliced dataframe
    if fname_idx == 0:
        ufsd = ufud
    else:
        ufsd = ufsd.append(ufud)

    #create list of filenames to go in the header    
    file_ids.append('.'.join(fname.split('/')[-1].split('.')[:-1])+'.h5')
    
    #increment the filename index
    fname_idx += 1
    
#############################################        
# Get info for spliced .dat header
#############################################

f = open(filenames_list[0], 'r')
header_lines = f.readlines()[:9]
f.close()

file_id_line = header_lines[1].split(':')[0]+': '+', '.join(file_ids)+'\n'
header_lines[1] = file_id_line
spliced_header = ''.join(header_lines)

###############################################
# Sort the rows of the spliced .dat DataFrame 
# so they are in order of freq., descending
###############################################

num_rows = ufsd['Uncorrected_Frequency'].size
ufsd.sort_values(by='Uncorrected_Frequency', ascending=False, inplace=True)
ufsd.set_index(np.arange(0, num_rows, 1), inplace=True)
    
#################################################################
# Replace Total_Hit_# values so they are unique for each
# row and are natural numbers, matching the turboSETI convention
#################################################################

total_hit_nums = np.arange(1, num_rows+1, 1).tolist()
ufsd['Top_Hit_#'] = total_hit_nums

################################################
# Fix issue with coarse channel numbers
################################################

sorted_coarse_chans = []
chan_num = 0

for c in range(num_rows):
    if c == 0:
        sorted_coarse_chans.append(chan_num)
    
    #if there are multiple rows for one coarse channel, the coarse
    #channel number needs to stay the same for all of those rows:
    elif ufsd.iloc[c, 10] == ufsd.iloc[(c-1), 10]: #sorted_dat_info[c,10] == sorted_dat_info[(c-1),10]:
        sorted_coarse_chans.append(chan_num)
        
    #if your coarse channel is different from the last one, it needs to be incremented:
    else:
        chan_num += 1
        sorted_coarse_chans.append(chan_num)

ufsd['Coarse_Channel_Number'] = sorted_coarse_chans

######################################################
# Print the spliced dat rows to the new file
######################################################

outfile_name = 'datspliced_'+'_'.join(filenames_list[0].split('_')[3:])
outfile = open(outfile_name, 'w')
outfile.write(spliced_header)

#indices
top_hit_idx = 0
drift_idx = 1
snr_idx = 2
ufreq_idx = 3
cfreq_idx = 4
index_idx = 5
fstart_idx = 6
fend_idx = 7
sefd_idx = 8
sefd_freq_idx = 9
cchan_idx = 10
full_hits_idx = 11

for r in range(num_rows):
    
    info_str = '%03d\t  '%(int(ufsd.iloc[r, top_hit_idx]))  #Top Hit number
    info_str += '%f\t'%(float(ufsd.iloc[r, drift_idx]))  #Drift Rate
    info_str += '%f\t  '%(float(ufsd.iloc[r, snr_idx]))  #SNR
    info_str += '%f\t  '%(float(ufsd.iloc[r, ufreq_idx])) #Uncorrected Frequency:
    info_str += '%f\t'%(float(ufsd.iloc[r, cfreq_idx])) #Corrected Frequency:
    info_str += '%d\t  '%(int(ufsd.iloc[r, index_idx])) #Index:
    info_str += '%f\t  '%(float(ufsd.iloc[r, fstart_idx])) #freq_start:
    info_str += '%f\t'%(float(ufsd.iloc[r, fend_idx])) #freq_end:
    info_str += '%f      \t'%(float(ufsd.iloc[r, sefd_idx])) #SEFD:
    info_str += '%f\t'%(float(ufsd.iloc[r, sefd_freq_idx])) #SEFD_mid_freq:
    info_str += '%i\t'%(int(ufsd.iloc[r, cchan_idx])) #course channel number
    info_str += '%i\t'%(int(ufsd.iloc[r, full_hits_idx])) #
    info_str +='\n'
    
    outfile.write(info_str)
    
outfile.close()

'''#check that coarse channel assignments match for spliced vs. unspliced

#read in ufud:

#now read in the table
ufud = ascii.read(filenames_list[0]+'.mod', format='commented_header', header_start=7, delimiter=' ')
ufud = ufud.to_pandas()
ufud = ufud.apply(pd.to_numeric)
ufud.sort_values(by='Uncorrected_Frequency', ascending=False, inplace=True)

ufud_coarse_chans = list(ufud['Full_number_of_hits'])
ufsd_coarse_chans = list(ufsd['Full_number_of_hits'])[:len(ufud_coarse_chans)]

print(ufud_coarse_chans == ufsd_coarse_chans)'''
