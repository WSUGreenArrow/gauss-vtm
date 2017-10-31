import os
import socket


def infile_type(parser, f):
    if os.path.isfile(f):
        return f
    else:
        parser.error('The input file `{}` does not exist'.format(f))


def get_primary_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 8000))
        ip = s.getsockname()[0]
    except:
        ip = None
    finally:
        s.close()

    return ip
