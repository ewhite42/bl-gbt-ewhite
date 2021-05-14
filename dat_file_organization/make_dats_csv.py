#this program uses pandas to create a table of dat files
# Ellie White 13 May 2021

import pandas as pd
import blimpy as bp
import glob 

#note you can add rows to an existing csv file by 
#specifying the existing file as the startfile

# Also note that to run this, you need access to the h5 or filterbank files,
# but not the dat files.

def create_waterfalls(fil_paths):

    #create waterfall objects so you can extract the header info from the h5 and fil files
    waterfalls = []
    for filname in fil_paths:
        fil = bp.Waterfall(filname)
        waterfalls.append(fil)

    return waterfalls

def write_dat_summary(startfile, dat_paths, h5_fil_paths, proj_name, contact_people, storage_loc, outfile_name = 'dat_summary.csv'):

    starting_df = pd.read_csv(startfile)

    num_rows = len(dat_paths)

    dat_names = []
    for dat in dat_paths:
        dat_names.append(dat.split('/')[-1])

    waterfalls = create_waterfalls(h5_fil_paths)

    rx_list = []
    for r in range(num_rows):
        rx_list.append(waterfalls[r].header['fch1'])

    mjd_list = []
    for m in range(num_rows):
        mjd_list.append(waterfalls[m].header['tstart'])

    target_list = []
    for t in range(num_rows):
        target_list.append(waterfalls[t].header['source_name'])

    table_data = []
    for i in range(num_rows):
        row = [dat_names[i], proj_name, contact_people, rx_list[i], mjd_list[i], target_list[i], storage_loc, h5_fil_paths[i]]
        table_data.append(row)

    new_dat_summary_df = pd.DataFrame(table_data, columns=starting_df.columns)
    dat_summary_df = starting_df.append(new_dat_summary_df)

    dat_summary_df.to_csv(outfile_name, index=False)
    return dat_summary_df

def get_file_paths(file_paths_lst):
    paths_file = open(file_paths_lst, 'r')
    lines = paths_file.readlines()

    file_paths = []
    for line in lines:
        file_paths.append(line.strip())

    return file_paths

def main():

    starting_table_fname = 'dat_summary_1.csv'
    new_table_fname = 'dat_summary_etz_and_gcp.csv'

    dats_list_file = 'karen_dat_paths.lst' #insert filepath here
    dat_filepaths = get_file_paths(dats_list_file)

    list_h5_fil_file = 'karen_fil_paths.lst'
    h5_fil_paths = get_file_paths(list_h5_fil_file)

    project = 'Galactic Center Survey'
    contact_person = 'Karen Perez'
    stored = 'blpc0'

    # starting_table = pd.DataFrame([[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']], columns=['.dat File Name', 'Project Name', 'Contact Person(s)', 'Max. Freq', 'MJD', 'Target', \
    #                                                                                   'Storage Location', 'Path to .h5 / .fil'])
    #starting_table.to_csv(starting_table_fname, index=False)
    # print(starting_table)

    dat_summary = write_dat_summary(starting_table_fname, dat_filepaths, h5_fil_paths, project, contact_person, stored, new_table_fname)
    print(dat_summary)

if __name__ == '__main__':
    main()
