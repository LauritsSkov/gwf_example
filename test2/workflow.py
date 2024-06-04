from gwf import Workflow, AnonymousTarget

gwf = Workflow()


def simulate(samples, sequence_length, mutation_rate, output):
    inputs = []
    outputs = [output]
    options = {}
    spec = f'''
    mkdir -p $(dirname {output})
    python simulate.py -samples={samples} -seq_len={sequence_length} -mutrate={mutation_rate} -out={output}
    '''
    return AnonymousTarget(inputs=inputs, outputs=outputs, options=options, spec=spec)


for samples in range(1,4):
    for sequence_length in [1000, 2000, 5000]:
        for mutation_rate in [0.01, 0.02, 0.05]:
            output = f'simdata/{samples}_{sequence_length}_{mutation_rate}.txt'
            jobname = f'simulate_{samples}_{sequence_length}_{mutation_rate}'
            gwf.target_from_template(jobname, simulate(samples, sequence_length, mutation_rate, output))