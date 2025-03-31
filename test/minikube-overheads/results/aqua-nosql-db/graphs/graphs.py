#!/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.family'] = 'NewComputerModern08'
plt.rcParams['font.size'] = 18

# Copied by hand, latency in us
data = {
    'MongoDB': {
        'containerd': {
            'read':  {'P90': 331, 'P99': 419},
            'write': {'P90': 314, 'P99': 429},
            'throughput': 2645.50,
        },
        'gVisor':  {
            'read':  {'P90': 435, 'P99': 554},
            'write': {'P90': 408, 'P99': 500},
            'throughput': 2183.41,
        },
        'QEMU':    {
            'read':  {'P90': 401, 'P99': 536},
            'write': {'P90': 371, 'P99': 448},
            'throughput': 2398.08,
        },
    },
    'Redis': {
        'containerd': {
            'read':  {'P90':  68, 'P99': 111},
            'write': {'P90':  75, 'P99':  98},
            'throughput': 16949.15,
        },
        'gVisor':  {
            'read':  {'P90': 140, 'P99': 198},
            'write': {'P90': 150, 'P99': 189},
            'throughput': 8547.01,
        },
        'QEMU':    {
            'read':  {'P90': 100, 'P99': 124},
            'write': {'P90': 109, 'P99': 147},
            'throughput': 10989.01,
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

    latencies[method] = [max(data[g][method]['read']['P99'], data[g][method]['write']['P99']) for g in groups]

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
    yticks = range(0, 21, 5)
    plt.yticks(ticks=yticks, labels=[f'{k}K' if k != 0 else '0' for k in yticks])
    plt.ylabel('Throughput [req/s]')
    plt.ylim(0, 21)
    plt.legend(**OUTSIDE_LEGEND_PARAMS)
    plt.savefig('throughput.pdf', bbox_inches='tight')
