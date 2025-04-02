#!/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np
# from cycler import cycler

plt.rcParams['font.family'] = 'NewComputerModern08'
plt.rcParams['font.size'] = 18
# plt.rcParams['axes.prop_cycle'] = cycler('color', plt.get_cmap('Set2').colors)

BAR_WIDTH = 0.2
OUTSIDE_LEGEND_PARAMS = {
    'bbox_to_anchor': (-0.06, 1, 1, 0.2), # x0, y0, width, height
    'frameon': False,
    'loc': 'lower left',
    'ncol': 3,
    'handlelength': 1,
}

# ============================================================ Web Servers
# 
# Latency in ms

# --------------------------- With 100 connections
data_100 = {
    'Lighttpd': {
        'containerd': { 'latency-p99': 1.06, 'throughput': 175210 },
        'gVisor':  { 'latency-p99': 3.41, 'throughput': 54100 },
        'QEMU':    { 'latency-p99': 6.15, 'throughput': 34650 },
    },
    'Nginx': {
        'containerd': { 'latency-p99': 1.18, 'throughput': 179750 },
        'gVisor':  { 'latency-p99': 13.29, 'throughput': 33390 },
        'QEMU':    { 'latency-p99': 40.18, 'throughput': 3160 },
    },
}
# --------------------------- With 10 connections
data = {
    'Lighttpd': {
        'containerd': { 'latency-p99': 0.109, 'throughput': 139510 },
        'gVisor':     { 'latency-p99': 0.586, 'throughput': 41070 },
        'QEMU':       { 'latency-p99': 0.512, 'throughput': 38010 },
    },
    'Nginx': {
        'containerd': { 'latency-p99': 0.235, 'throughput': 136260 },
        'gVisor':     { 'latency-p99': 2.56, 'throughput': 27730 },
        'QEMU':       { 'latency-p99': 4.16, 'throughput': 3120 },
    },
}

groups = data.keys()
xs = np.arange(len(groups))
latencies = {}
throughputs = {}

for method in ['containerd', 'gVisor', 'QEMU']:
    latencies[method] = [data[g][method]['latency-p99'] for g in groups]
    plt.figure()
    m = 0
    for label, values in latencies.items():
        offset = BAR_WIDTH * m
        plt.bar(xs + offset, values, width=BAR_WIDTH, label=label)
        m += 1

    plt.xticks(xs + BAR_WIDTH, groups)
    plt.ylabel('Latency [ms]')
    plt.legend(**OUTSIDE_LEGEND_PARAMS)
    plt.savefig('web-servers-latency.pdf', bbox_inches='tight')

    throughputs[method] = [data[g][method]['throughput'] / 1000 for g in groups]
    plt.figure()
    m = 0
    for label, values in throughputs.items():
        offset = BAR_WIDTH * m
        plt.bar(xs + offset, values, width=BAR_WIDTH, label=label)
        m += 1

    plt.xticks(xs + BAR_WIDTH, groups)
    yticks = range(0, 200, 40)
    plt.yticks(ticks=yticks, labels=[f'{k}K' if k != 0 else '0' for k in yticks])
    plt.ylabel('Throughput [req/s]')
    plt.legend(**OUTSIDE_LEGEND_PARAMS)
    plt.savefig('web-servers-throughput.pdf', bbox_inches='tight')


# ============================================================ NoSQL

# Latency in us
data = {
    'MongoDB': {
        'containerd': {
            'read-p99':  419,
            'write-p99': 429,
            'throughput': 2645.50,
        },
        'gVisor':  {
            'read-p99':  554,
            'write-p99': 500,
            'throughput': 2183.41,
        },
        'QEMU':    {
            'read-p99':  536,
            'write-p99': 448,
            'throughput': 2398.08,
        },
    },
    'Redis': {
        'containerd': {
            'read-p99':  111,
            'write-p99': 98,
            'throughput': 16949.15,
        },
        'gVisor':  {
            'read-p99':  198,
            'write-p99': 189,
            'throughput': 8547.01,
        },
        'QEMU':    {
            'read-p99':  124,
            'write-p99': 147,
            'throughput': 10989.01,
        },
    },
}

groups = data.keys()
xs = np.arange(len(groups))
latencies = {}
throughputs = {}
for method in ['containerd', 'gVisor', 'QEMU']:
    latencies[method] = [max(data[g][method]['read-p99'], data[g][method]['write-p99']) / 1000 for g in groups]
    plt.figure()
    m = 0
    for label, values in latencies.items():
        offset = BAR_WIDTH * m
        plt.bar(xs + offset, values, width=BAR_WIDTH, label=label)
        m += 1

    plt.xticks(xs + BAR_WIDTH, groups)
    plt.ylabel('Latency [ms]')
    plt.legend(**OUTSIDE_LEGEND_PARAMS)
    plt.savefig('nosql-latency.pdf', bbox_inches='tight')

    throughputs[method] = [data[g][method]['throughput'] / 1000 for g in groups]
    plt.figure()
    m = 0
    for label, values in throughputs.items():
        offset = BAR_WIDTH * m
        plt.bar(xs + offset, values, width=BAR_WIDTH, label=label)
        m += 1

    plt.xticks(xs + BAR_WIDTH, groups)
    yticks = range(0, 21, 5)
    plt.yticks(ticks=yticks, labels=[f'{k}K' if k != 0 else '0' for k in yticks])
    plt.ylabel('Throughput [q/s]')
    plt.ylim(0, 21)
    plt.legend(**OUTSIDE_LEGEND_PARAMS)
    plt.savefig('nosql-throughput.pdf', bbox_inches='tight')



# ============================================================ SQL (Sysbench)

# Latency in ms
data = {
    'MySQL': {
        'containerd': {
            'latency-p99':  16.12,
            'throughput': 2270.57,
        },
        'gVisor':  {
            'latency-p99':  21.11,
            'throughput': 1661.38,
        },
        'QEMU':    {
            'latency-p99':  21.50,
            'throughput': 1493.13,
        },
    },
    'PostgreSQL': {
        'containerd': {
            'latency-p99':  4.33,
            'throughput': 6991.39,
        },
        'gVisor':  {
            'latency-p99':  9.22,
            'throughput': 3321.93,
        },
        'QEMU':    {
            'latency-p99':  5.57,
            'throughput': 5006.76,
        },
    },
}

groups = data.keys()
xs = np.arange(len(groups))
latencies = {}
throughputs = {}
for method in ['containerd', 'gVisor', 'QEMU']:
    latencies[method] = [data[g][method]['latency-p99'] for g in groups]
    plt.figure()
    m = 0
    for label, values in latencies.items():
        offset = BAR_WIDTH * m
        plt.bar(xs + offset, values, width=BAR_WIDTH, label=label)
        m += 1

    plt.xticks(xs + BAR_WIDTH, groups)
    plt.ylabel('Latency [ms]')
    plt.legend(**OUTSIDE_LEGEND_PARAMS)
    plt.savefig('sysbench-latency.pdf', bbox_inches='tight')

    throughputs[method] = [data[g][method]['throughput'] / 1000 for g in groups]
    plt.figure()
    m = 0
    for label, values in throughputs.items():
        offset = BAR_WIDTH * m
        plt.bar(xs + offset, values, width=BAR_WIDTH, label=label)
        m += 1

    plt.xticks(xs + BAR_WIDTH, groups)
    yticks = range(0, 8)
    plt.yticks(ticks=yticks, labels=[f'{k}K' if k != 0 else '0' for k in yticks])
    plt.ylabel('Throughput [q/s]')
    plt.legend(**OUTSIDE_LEGEND_PARAMS)
    plt.savefig('sysbench-throughput.pdf', bbox_inches='tight')
