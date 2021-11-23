import os

def extract_cpk(cpk):
    '''
    Receives the cpk, then use an external app CPKMAKERC to extract them
    into a temp folder where we extract our files
    '''
    cur_dir = os.path.abspath(".")
    if cpk !='':
        output_folder = cpk.split('/')[-1].split('.')[0]
        os.system(CPKMAKERC + ' \"'  + cpk +'\" -extract=\"' + cur_dir + '/input/' + output_folder + '\" -noerrorstop')

def compress_cpk(folder):
    '''
    Receives a folder, then use an external app CPKMAKERC to compress 
    the files inside into a cpk file 
    '''
    if folder != '':
        cpkname = folder.split('/')[-1]
        # cpkmakec.exe "../input/MTEXT" "./MTEXT.cpk" -align=512 -mode=ID -forcecompress -noerrorstop
        os.system(CPKMAKERC + ' \"'  + folder +'\" \"' + cpkname + '.cpk\" -align=512 -mode=ID -forcecompress -noerrorstop')

CPKMAKERC = r'utils\cpkmakec.exe'