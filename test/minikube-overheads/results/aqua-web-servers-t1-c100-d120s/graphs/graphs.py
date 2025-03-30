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
            'latency': {'P50': 1.03, 'P90': 3.36, 'P99': 9.31},
            'throughput': 72570,
        },
        'gVisor':  {
            'latency': {'P50': 3.16, 'P90': 9.06, 'P99': 19.02},
            'throughput': 23160,
        },
        'QEMU':    {
            'latency': {'P50': 24.45, 'P90': 71.29, 'P99': 170.39},
            'throughput': 3420,
        },
    },
    'Lighttpd': {
        'containerd': {
            'latency': {'P50': 0.544, 'P90': 0.586, 'P99': 1.06},
            'throughput': 175400,
        },
        'gVisor':  {
            'latency': {'P50': 1.87, 'P90': 2.31, 'P99': 3.32},
            'throughput': 53550,
        },
        'QEMU':    {
            'latency': {'P50': 2.90, 'P90': 3.43, 'P99': 5.37},
            'throughput': 37830,
        },
    },
    'Nginx': {
        'containerd': {
            'latency': {'P50': 0.453, 'P90': 0.694, 'P99': 1.15},
            'throughput': 181060,
        },
        'gVisor':  {
            'latency': {'P50': 2.66, 'P90': 6.14, 'P99': 14.10},
            'throughput': 33210,
        },
        'QEMU':    {
            'latency': {'P50': 29.92, 'P90': 35.44, 'P99': 42.07},
            'throughput': 3280,
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
