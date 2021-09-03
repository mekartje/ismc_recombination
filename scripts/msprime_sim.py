##Parameter file format:
#breaks = 	//comma-separated list of break positions. none if using recom_bedgraph option
#r = 	//comma-separated list of recombination rates (NOT population-scaled). none if using recom_bedgraph option
#recom_bedgraph =    //bedgraph with rho estimates output from ismc_mapper. none if using breaks and r options
#demo_model = 

##1st argument -- parameter file
##2nd argument -- outfile prefix

import msprime, sys
from IPython.display import SVG, display

with open(sys.argv[1]) as params:
    #read off header line(s)
    for line in params:
        if not line.startswith('breaks'):
            continue
        else:
            #get recombination window breakpoints
            breaks = line.split('=')[1].strip()
            breaks = [int(i.strip()) for i in breaks.split(',')]
            #get recombination landscape, parse comma-separated value into list
            r = params.readline().split('=')[1].strip()
            r = [float(i.strip()) for i in r.split(',')]
            #get recombinnation bedgraph path
            recom_bedgraph = params.readline().split('=')[1].strip()
            #get demographic model ('gough' or 'germany')
            demo_model = params.readline().split('=')[1].strip()
            break

#if given, parse bedgraph to get recombination landscape (replace breaks and r if so)
if recom_bedgraph != 'none':
    breaks = []
    r = []
    with open(recom_bedgraph) as recomf:
        #read off header line
        header = recomf.readline().rstrip().split('\t')
        r_pos = header.index('sample_mean')
        for line in recomf:
            line = line.rstrip().split('\t')
            breaks.append(int(line[1]))
            r.append(float(line[r_pos]))
        #append last position to breaks
        breaks.append(int(line[2]))
        #shift breaks so first position is zero (this is requried by msprime)
        correction = breaks[0]
        breaks = [(i - correction) for i in breaks]	

print('Simulating a population with a ' + demo_model + '-like demographic history.\n')

demography = msprime.Demography()
demography.add_population(initial_size = 175000)

if demo_model == 'gough':
    print('GOUGH')
    #pop size at colonization
    demography.add_population_parameters_change(time = 1250, initial_size = 350)
    #current pop size (instantaneous-ish bottleneck)
    demography.add_population_parameters_change(time = 1249, initial_size = 18500)
    #sort demographic events (most recent first)
    demography.sort_events()

elif demo_model == 'germany':
    print('GERMANY')

#rate map for 10Mb region in 1Mb windows
#rate_map = msprime.RateMap(position = [0, 1000000, 2000000, 3000000, 4000000, 5000000, 6000000, 7000000, 8000000, 9000000, 10000000],
#                           rate = [8.1414160871523e-09, 8.301303586214627e-09, 9.291919258522762e-09, 8.0960257636222e-09, 8.562263986862933e-09, 7.334352877992885e-09, 7.970534809877985e-09, 9.368170436697772e-09, 8.598866846424917e-09, 8.587776714560249e-09])
rate_map = msprime.RateMap(position = breaks, rate = r)

#number of independent replicates
num_replicates = 20
replicates = msprime.sim_ancestry(4, num_replicates = num_replicates, recombination_rate=rate_map, demography = demography)
for replicate_index, ts in enumerate(replicates):
    mts = msprime.sim_mutations(ts, model = 'JC69', rate = 2.31625e-09)
    with open(sys.argv[2] + str(replicate_index) + '.vcf', 'w') as outf:
        mts.write_vcf(outf)
