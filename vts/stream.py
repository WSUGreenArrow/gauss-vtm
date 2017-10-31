#!/usr/bin/env python
import argparse
import os
import signal
import subprocess
import sys
import tempfile
import time
import threading

from http.server import HTTPServer, SimpleHTTPRequestHandler
from utils import infile_type, get_primary_ip


g_server = None
g_tempdir = tempfile.TemporaryDirectory(prefix='gauss_')
g_threads = []
g_stop = threading.Event()


def stream(source, name, host, port, vstream=0, astream=None, realtime=True):
    print('Streaming `{}` on rtp://{}:{}'.format(name, host, port))
    sdp_filename = os.path.join(g_tempdir.name, name + '.sdp')

    # Start FFmpeg
    cmd = ['ffmpeg']
    if realtime:
        cmd.append('-re')
    cmd.extend([
        '-f', 'mjpeg',
        '-i', source,
        '-c', 'copy',       # copy existing codec
        '-f', 'rtp',        # stream over RTP
        '-map', '0:v:{}'.format(vstream),
    ])
    if astream is not None:
        cmd.extend(['-map', '0:a:{}'.format(astream)])
    cmd.append('rtp://{}:{}'.format(host, port))

    p = subprocess.Popen(cmd, stderr=subprocess.DEVNULL, stdout=subprocess.PIPE,
                         universal_newlines=True, bufsize=1)

    # Save SDP to temporary directory for HTTP server
    line = p.stdout.readline()
    while line.strip() != 'SDP:':
        line = p.stdout.readline()
    with open(sdp_filename, 'w') as sdp:
        line = p.stdout.readline()
        while line.strip():
            sdp.write(line)
            line = p.stdout.readline()

    # Wait for streaming to stop
    while p.poll() is None:
        if g_stop.is_set():
            p.send_signal(signal.SIGTERM)
        time.sleep(0.5)

    if not g_stop.is_set():
        print('Stream `{}` completed.'.format(name))
        os.unlink(sdp_filename)

    # If this is the last stream thread, kill the server
    if not os.listdir(g_tempdir.name):
        g_server.shutdown()


def terminate(signum, frame):
    if not g_stop.is_set():
        print('Stopping server...')
        g_stop.set()
        g_server.shutdown()


def main():
    global g_server

    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--left', required=True,
                        type=lambda f: infile_type(parser, f),
                        help='left channel input')
    parser.add_argument('-r', '--right', required=True,
                        type=lambda f: infile_type(parser, f),
                        help='right channel input')
    parser.add_argument('--audio', choices=['l', 'r'],
                        help='audio source (left / right)')
    parser.add_argument('--host', help='address to bind to')
    parser.add_argument('--hport', default=8080, type=int,
                        help='HTTP server port number')
    parser.add_argument('--lport', default=8482, type=int,
                        help='left video port number')
    parser.add_argument('--rport', default=8483, type=int,
                        help='right video port number')
    args = parser.parse_args()

    # Check for default host
    host = args.host
    if host is None:
        host = get_primary_ip()
        if host is None:
            print('Could not detect primary IP address!')
            return 1

    # Parse arguments
    left = os.path.abspath(os.path.realpath(args.left))
    right = os.path.abspath(os.path.realpath(args.right))
    audio = args.audio
    hport, lport, rport = args.hport, args.lport, args.rport

    # Start HTTP server
    os.chdir(g_tempdir.name)
    g_server = HTTPServer((host, hport), SimpleHTTPRequestHandler)

    server_thread = threading.Thread(target=g_server.serve_forever)
    g_threads.append(server_thread)
    server_thread.start()
    print('Serving files from `{}` on {}:{}'.format(g_tempdir.name, host, hport))

    # Start video streams
    left_thread = threading.Thread(target=stream, name='left',
                                   args=(left, 'left', host, lport),
                                   kwargs={'realtime': True,
                                           'astream': 0 if audio == 'l' else None})
    right_thread = threading.Thread(target=stream, name='right',
                                    args=(right, 'right', host, rport),
                                    kwargs={'realtime': True,
                                            'astream': 0 if audio == 'r' else None})
    g_threads.append(left_thread)
    g_threads.append(right_thread)
    left_thread.start()
    right_thread.start()

    # Register signal handlers
    signal.signal(signal.SIGTERM, terminate)
    signal.signal(signal.SIGINT, terminate)

    print('Press Ctrl+C to quit.')
    for thread in g_threads:
        thread.join()
    g_tempdir.cleanup()

    return 0


if __name__ == '__main__':
    sys.exit(main())
