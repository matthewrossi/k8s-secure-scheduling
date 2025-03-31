#!/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.family'] = 'NewComputerModern08'
plt.rcParams['font.size'] = 18

# Copied by hand, latency in ms
# Throughput is average req/s
data = {
    # 'Apache': {
    #     'containerd': {
    #         'latency': {'P50': 1.04, 'P90': 3.32, 'P99': 8.56},
    #         'throughput': 72290,
    #     },
    #     'gVisor':  {
    #         'latency': {'P50': 3.28, 'P90': 9.14, 'P99': 18.08},
    #         'throughput': 22370,
    #     },
    #     'QEMU':    {
    #         'latency': {'P50': 24.33, 'P90': 73.32, 'P99': 173.11},
    #         'throughput': 3390,
    #     },
    # },
    'Lighttpd': {
        'containerd': {
            'latency': {'P50': 0.541, 'P90': 0.708, 'P99': 1.06},
            'throughput': 175210,
        },
        'gVisor':  {
            'latency': {'P50': 1.83, 'P90': 2.30, 'P99': 3.41},
            'throughput': 54100,
        },
        'QEMU':    {
            'latency': {'P50': 3.46, 'P90': 5.28, 'P99': 6.15},
            'throughput': 34650,
        },
    },
    'Nginx': {
        'containerd': {
            'latency': {'P50': 0.474, 'P90': 0.727, 'P99': 1.18},
            'throughput': 179750,
        },
        'gVisor':  {
            'latency': {'P50': 2.64, 'P90': 5.92, 'P99': 13.29},
            'throughput': 33390,
        },
        'QEMU':    {
            'latency': {'P50': 31.93, 'P90': 36.32, 'P99': 40.18},
            'throughput': 3160,
        },
    },
}


width = 0.25    # bar width
groups = data.keys()
xs = np.arange(len(groups))
latencies = {}
throughputs = {}

OUTSIDE_LEGEND_PARAMS = {
    'bbox_to_anchor': (-0.06, 1, 1, 0.2), # x0, y0, width, height
    'frameon': False,
    'loc': 'lower left',
    'ncol': 3,
    'handlelength': 1,
}

for method in ['containerd', 'gVisor', 'QEMU']:
    # ------------------------------------ Latency

    latencies[method] = [data[g][method]['latency']['P99'] for g in groups]

    plt.figure()
    m = 0
    for label, values in latencies.items():
        offset = width * m
        plt.bar(xs + offset, values, width=width, label=label)
        m += 1

    plt.xticks(xs + width, groups)
    plt.ylabel('Latency [ms]')
    plt.legend(**OUTSIDE_LEGEND_PARAMS)
    plt.savefig('latency.pdf', bbox_inches='tight')

    # ------------------------------------ Throughput

    throughputs[method] = [data[g][method]['throughput'] / 1000 for g in groups]

    plt.figure()
    m = 0
    for label, values in throughputs.items():
        offset = width * m
        plt.bar(xs + offset, values, width=width, label=label)
        m += 1

    plt.xticks(xs + width, groups)
    yticks = range(0, 200, 40)
    plt.yticks(ticks=yticks, labels=[f'{k}K' if k != 0 else '0' for k in yticks])
    plt.ylabel('Throughput [req/s]')
    plt.legend(**OUTSIDE_LEGEND_PARAMS)
    plt.savefig('throughput.pdf', bbox_inches='tight')
