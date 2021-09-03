##Parameter file format:
#recom_bedgraph =    //bedgraph with rho estimates output from ismc_mapper. none if using breaks and r options
#Tcol = //colonization time (integer)
#out_pre = //outfile prefix

##1st argument -- parameter file

#msprime simulation outline (forward in time)
#1 -- ancestral population N = 175,000
#2 -- population split into A & B at colonization time Tcol
    #A -- constant N = 175000 until present ('initial size' = 175000 with no growth)
    #B -- (1) N reduced to 350 at split time with growth rate of 1.001 for ('initial size' = 18,500, set growth rate so that size at split is 350 1250 generation in the past)
    #            -- lasts 1250 generations
    #      (2) From Tcol + 1250 = T2 until present, population is constant at 18,500

import msprime, sys

with open(sys.argv[1]) as params:
    for line in params:
        if line.startswith('recom_bedgraph'):
            recom_bedgraph = line.rstrip().split('=')[1].strip()
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
        elif line.startswith('Tcol'):
            Tcol = int(line.rstrip().split('=')[1].strip())
        elif line.startswith('out_pre'):
            out_pre = line.rstrip().split('=')[1].strip()

print('Using recombination landscape specified in ' + recom_bedgraph + '\n')

demography = msprime.Demography()
demography.add_population(name = 'gough', initial_size = 18_500, growth_rate = 0.003174)
demography.add_population(name = 'germany', initial_size = 175_000)
demography.add_population(name = 'anc', initial_size = 175_000)
demography.add_population_split(time = Tcol, derived = ['gough', 'germany'], ancestral = 'anc')
if Tcol > 1250:
    demograhy.add_population_parameters_change(time = Tcol - 1250, initial_size = 18_500, population = 'gough')
demography.sort_events()

print(demography)

rate_map = msprime.RateMap(position = breaks, rate = r)

num_replicates = 50

replicates = msprime.sim_ancestry(samples = {'gough':4, 'germany':4}, num_replicates = num_replicates, recombination_rate = rate_map, demography = demography)
for replicate_index, ts in enumerate(replicates):
    mts = msprime.sim_mutations(ts, model = 'JC69', rate = 2.31625e-09)
    with open(out_pre + str(replicate_index) + '.vcf', 'w') as outf:
        mts.write_vcf(outf)
