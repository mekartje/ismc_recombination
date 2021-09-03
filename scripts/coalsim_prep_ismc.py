#Script to generate ismc inputs from a list of input vcf's

##1st argument -- file containing newline-delimited vcf paths

import sys

#get list of vcfs
with open(sys.argv[1]) as inf:
    vcfs = [i.rstrip() for i in inf]

for vcf in vcfs:
    with open(vcf) as inf, open(vcf[:-4] + '.tab', 'w') as tabf, open(vcf[:-4] + '_ismc.bpp', 'w') as bpp:
        #read off header lines
        for line in inf:
            if line.startswith('#'):
                pass
            else:
                break
        #get first position
        start = line.rstrip().split('\t')[1]
        #get last position
        for line in inf:
            pass
        end = line.rstrip().split('\t')[1]
        tab_line = [str(1), start, end, str(0), str(int(end) - int(start)), start, end]
        tab_line = '\t'.join(tab_line)
        tabf.writelines(tab_line + '\n')
        bpp.writelines('#iSMC parameter file generated using coalsim_prep_ismc.py\n')
        bpp.writelines('dataset_label = ' + vcf[:-4] + '\n')
        bpp.writelines('input_file_type = VCF\n')
        bpp.writelines('sequence_file_path = ' + vcf + '\n')
        bpp.writelines('mask_file_path =   \n')
        bpp.writelines('mask_file_type =   \n')
        bpp.writelines('seq_compression_type =   \n')
        bpp.writelines('mask_compression_type =   \n')
        bpp.writelines('tab_file_path = ' + vcf[:-4] + '.tab\n')
        bpp.writelines('diploid_indices = (0,1)\n')
        bpp.writelines('optimize = true\n')
        bpp.writelines('decode = true\n')
        bpp.writelines('number_threads = 4\n')
        bpp.writelines('decode_breakpoints_parallel = false\n')
        bpp.writelines('number_rho_categories = 5\n')
        bpp.writelines('number_intervals =   \n')
        bpp.writelines('function_tolerance = 1e-4\n')
        bpp.writelines('fragment_size = 3000000\n')
