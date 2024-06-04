"""This is an example workflow for read-mapping using bwa and samtools."""
from gwf import Workflow, AnonymousTarget

gwf = Workflow()

def bwa_index(ref_genome):
    """Template for indexing a genome with `bwa index`."""
    inputs = ['{}.fa'.format(ref_genome)]
    outputs = ['{}.amb'.format(ref_genome),
               '{}.ann'.format(ref_genome),
               '{}.pac'.format(ref_genome),
               '{}.bwt'.format(ref_genome),
               '{}.sa'.format(ref_genome),
               ]
    options = {
        'cores': 1,
        'memory': '1g',
        'walltime': '00:45:00',
        'queue': 'savio3_htc',
        'account': 'co_moorjani',
    }

    spec = f"""
    module load bwa

    bwa index -p {ref_genome} -a bwtsw {ref_genome}.fa
    """

    return AnonymousTarget(inputs=inputs, outputs=outputs, options=options, spec=spec)

def bwa_map(ref_genome, r1, r2, bamfile):
    """Template for mapping reads to a reference genome with `bwa` and `samtools`."""
    inputs = [r1, r2,
              '{}.amb'.format(ref_genome),
              '{}.ann'.format(ref_genome),
              '{}.pac'.format(ref_genome),
             ]
    outputs = [bamfile]
    options = {
        'cores': 1,
        'memory': '1g',
        'walltime': '00:45:00',
        'queue': 'savio3_htc',
        'account': 'co_moorjani',
    }

    spec = f'''
    module load bwa
    module load samtools

    bwa mem -t 1 {ref_genome} {r1} {r2} | samtools sort | samtools rmdup -s - {bamfile}
    '''

    return AnonymousTarget(inputs=inputs, outputs=outputs, options=options, spec=spec)


def merge_bamfiles(inbamfiles, mergedbam):
    """Template for indexing a genome with `bwa index`."""
    inputs = inbamfiles
    space_separated = ' '.join(inbamfiles)

    outputs = [mergedbam]
    options = {
        'cores': 1,
        'memory': '1g',
        'walltime': '00:45:00',
        'queue': 'savio3_htc',
        'account': 'co_moorjani',
    }

    spec = f"""
    module load samtools
    samtools merge -f {mergedbam} {space_separated}
    """

    return AnonymousTarget(inputs=inputs, outputs=outputs, options=options, spec=spec)





# Index refgenome
gwf.target_from_template(name='IndexGenome',template=bwa_index(ref_genome='ponAbe2'))


# Map reads to reference genome

ref_genome = 'ponAbe2'
outbamfiles = []

for index in range(15):

    jobname = f'map_pairs_{index}'
    out_bamfile = f'bamfiles/Masala_{index}.bam'
    outbamfiles.append(out_bamfile)

    r1 = f'fastqfiles/Masala_R1.{index}.fastq'
    r2 = f'fastqfiles/Masala_R2.{index}.fastq'

    gwf.target_from_template(jobname,template=bwa_map(ref_genome, r1, r2, out_bamfile))


# Merge bamfiles
mergedbam = 'bamfiles/Masala.bam'
gwf.target_from_template('merge',template=merge_bamfiles(outbamfiles, mergedbam))