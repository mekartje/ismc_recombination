#script to iterate over .bed file, keeping only autosomes
##1st argument -- bed file path

import sys

autosomes=['chr1', 'chr2', 'chr3', 'chr4', 'chr5', 'chr6', 'chr7', 'chr8', 'chr9', 'chr10', 'chr11', 'chr12', 'chr13', 'chr14', 'chr15', 'chr16', 'chr17', 'chr18', 'chr19']

with open(sys.argv[1]) as inf, open(sys.argv[1][:-4] + '_autosomes.bed', 'w') as outf:
    for line in inf:
        chr = line.rstrip().split('\t')[0]
        if chr in autosomes:
            outf.writelines(line)
        else:
            continue
