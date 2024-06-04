import msprime 
import argparse

parser = argparse.ArgumentParser(description='Simulate something')
parser.add_argument('-samples', default = 2, type=int)
parser.add_argument('-seq_len', default = 1000, type=int)
parser.add_argument('-mutrate', default = 0.01, type=float)
parser.add_argument('-out', default = 'output.txt', type=str)

args = parser.parse_args()

ts = msprime.sim_ancestry(args.samples, sequence_length=args.seq_len)
mts = msprime.sim_mutations(ts, rate=args.mutrate)

with open(args.out, 'w') as out:
    for var in mts.variants():
        print(var.site.position, var.alleles, var.genotypes, sep="\t", file = out)