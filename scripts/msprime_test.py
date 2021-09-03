import msprime
from IPython.display import SVG, display

ts = msprime.sim_ancestry(samples=3, recombination_rate=1e-8,sequence_length=5_000,population_size=10_000,random_seed=123456)

SVG(ts.draw_svg())
