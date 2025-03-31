#!/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.family'] = 'NewComputerModern08'
plt.rcParams['font.size'] = 18

# Copied by hand, latency in ms
# Throughput is average req/s
data = {
    'Apache': {
        'containerd': {
            'latency': {'P50': 1.04, 'P90': 3.32, 'P99': 8.56},
            'throughput': 72290,
        },
        'gVisor':  {
            'latency': {'P50': 3.28, 'P90': 9.14, 'P99': 18.08},
            'throughput': 22370,
        },
        'QEMU':    {
            'latency': {'P50': 24.33, 'P90': 73.32, 'P99': 173.11},
            'throughput': 3390,
        },
    },
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

# ------------------------------------ Latency graphs

for server in data.keys():
    width = 0.25   # bar width

    groups = list(data[server].keys())
    percentiles = {}
    for perc in ['P50', 'P90', 'P99']:
        percentiles[perc] = [data[server][g]['latency'][perc] for g in groups]
        
    plt.figure()

    x = np.arange(len(groups))
    m = 0
    for attribute, measurement in percentiles.items():
        offset = width * m
        plt.bar(x + offset, measurement, width, label=attribute)
        m += 1

    plt.xticks(x + width, groups)
    # plt.xlabel('Method')
    plt.ylabel('Latency [ms]')
    # plt.yscale('log')
    plt.legend()

    plt.savefig(f'{server}-latency.pdf', bbox_inches='tight')

# ------------------------------------ Throughput

OUTSIDE_LEGEND_PARAMS = {
    'bbox_to_anchor': (-0.06, 1, 1, 0.2), # x0, y0, width, height
    'frameon': False,
    'loc': 'lower left',
    'ncol': 3,
    'handlelength': 1,
}

width = 0.25   # bar width

groups = data.keys()
methods = {}
for method in ['containerd', 'gVisor', 'QEMU']:
    methods[method] = [data[g][method]['throughput'] / 1000 for g in groups]
    
fig = plt.figure()

x = np.arange(len(groups))
m = 0
for attribute, measurement in methods.items():
    offset = width * m
    plt.bar(x + offset, measurement, width, label=attribute)
    m += 1

plt.xticks(x + width, groups)
yticks = range(0, 200, 40)
plt.yticks(ticks=yticks, labels=[f'{k}K' if k != 0 else '0' for k in yticks])
# plt.xlabel('Method')
plt.ylabel('Throughput [req/s]')
# plt.yscale('log')
plt.legend(**OUTSIDE_LEGEND_PARAMS)

plt.savefig(f'throughput.pdf', bbox_inches='tight')
