import os


def infile_type(parser, f):
    if os.path.isfile(f):
        return f
    else:
        parser.error('The input file `{}` does not exist'.format(f))
