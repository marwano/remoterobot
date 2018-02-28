#!/usr/bin/env python3

import time
from statistics import mean
from argparse import ArgumentParser
from http.client import HTTPConnection


def parse_args():
    parser = ArgumentParser(description='measure network latency')
    parser.add_argument('--host', default='localhost', help='server hostname')
    parser.add_argument('--port', default=8000, help='server port number')
    parser.add_argument('--count', default=10, type=int, help='sample count')
    return parser.parse_args()


def main():
    args = parse_args()
    conn = HTTPConnection(args.host, args.port)
    stats = []
    for i in range(1, args.count + 1):
        start = time.perf_counter()
        conn.request('POST', '/', '{"action": "__str__", "kwargs": {}}')
        response = conn.getresponse().read().decode()
        duration = (time.perf_counter() - start) * 1000
        if i != 1:
            stats.append(duration)
        msg = '(excluded from stats)' if i == 1 else ''
        print('seq: {i:>2}  time: {duration:.2f} ms {msg}'.format(**vars()))
        assert 'SwiftAPI object' in response, 'invalid response received'
    print('-------- SUMMARY --------')
    print('  max: {:.2f} ms'.format(max(stats)))
    print('  avg: {:.2f} ms'.format(mean(stats)))
    print('  min: {:.2f} ms'.format(min(stats)))


if __name__ == '__main__':
    main()
