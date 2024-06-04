from gwf import Workflow, AnonymousTarget

gwf = Workflow()


def make_text(value, output):
    inputs = []
    outputs = [output]
    options = {}
    spec = f'''
    echo {value} > {output}
    '''
    return AnonymousTarget(inputs=inputs, outputs=outputs, options=options, spec=spec)


def merge_text(infiles, output):
    inputs = infiles
    infiles_string = ' '.join(infiles)

    outputs = [output]
    options = {}
    spec = f'''
    cat {infiles_string} > {output}
    '''
    return AnonymousTarget(inputs=inputs, outputs=outputs, options=options, spec=spec)


# Make some input files
list_output_files = []
for value in 'xy':
    output = f'{value}.txt'
    list_output_files.append(output)
    gwf.target_from_template(f'make_{value}', make_text(value, output))



# merge them in the output
final_output = 'final_out.txt'
gwf.target_from_template(f'merge', merge_text(list_output_files, final_output))



