#!/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np
# from cycler import cycler

plt.rcParams['font.family'] = 'NewComputerModern08'
plt.rcParams['font.size'] = 23
# plt.rcParams['axes.prop_cycle'] = cycler('color', plt.get_cmap('Set2').colors)

BAR_WIDTH = 0.2
OUTSIDE_LEGEND_PARAMS = {
    'bbox_to_anchor': (-0.15, 1, 1, 0.2), # x0, y0, width, height
    'frameon': False,
    'loc': 'lower left',
    'ncol': 3,
    'handlelength': 1,
    'columnspacing': 0.8,
    'handletextpad': 0.4,
}

# ============================================================ Web Servers
# 
# Latency in ms

# --------------------------- With 100 connections
data_100 = {
    'Lighttpd': {
        'Our solution': { 'latency-p99': 1.06,  'latency-p90': 0.71,  'latency-p50': 0.54,  'throughput': 175210 },
        'gVisor':       { 'latency-p99': 3.41,  'latency-p90': 2.30,  'latency-p50': 1.83,  'throughput': 54100 },
        'Kata':         { 'latency-p99': 6.15,  'latency-p90': 5.28,  'latency-p50': 3.46,  'throughput': 34650 },
    },
    'Nginx': {
        'Our solution': { 'latency-p99': 1.18,  'latency-p90': 0.73,  'latency-p50': 0.47,  'throughput': 179750 },
        'gVisor':       { 'latency-p99': 13.29, 'latency-p90': 5.92,  'latency-p50': 2.64,  'throughput': 33390 },
        'Kata':         { 'latency-p99': 40.18, 'latency-p90': 36.32, 'latency-p50': 31.93, 'throughput': 3160 },
    },
}
# --------------------------- With 10 connections
data = {
    'Lighttpd': {
        'Our solution': { 'latency-p99': 0.109, 'latency-p90': 0.082, 'latency-p50': 0.070, 'throughput': 139510 },
        'gVisor':       { 'latency-p99': 0.586, 'latency-p90': 0.345, 'latency-p50': 0.214, 'throughput': 41070 },
        'Kata':         { 'latency-p99': 0.512, 'latency-p90': 0.358, 'latency-p50': 0.276, 'throughput': 38010 },
    },
    'Nginx': {
        'Our solution': { 'latency-p99': 0.235, 'latency-p90': 0.100, 'latency-p50': 0.064, 'throughput': 136260 },
        'gVisor':       { 'latency-p99': 2.56,  'latency-p90': 0.797, 'latency-p50': 0.304, 'throughput': 27730 },
        'Kata':         { 'latency-p99': 4.16,  'latency-p90': 3.67,  'latency-p50': 3.21,  'throughput': 3120 },
    },
}

groups = data.keys()
xs = np.arange(len(groups))
latencies = {}
throughputs = {}

for method in ['Our solution', 'gVisor', 'Kata']:
    for perc in ['p99', 'p90', 'p50']:
        latencies[method] = [data[g][method][f'latency-{perc}'] for g in groups]
        plt.figure()
        m = 0
        for label, values in latencies.items():
            offset = BAR_WIDTH * m
            plt.bar(xs + offset, values, width=BAR_WIDTH, label=label)
            m += 1

        plt.xticks(xs + BAR_WIDTH, groups)
        plt.ylabel('Latency [ms]')
        plt.ylim(0, 4.3)
        plt.legend(**OUTSIDE_LEGEND_PARAMS)
        plt.savefig(f'web-servers-latency-{perc}.pdf', bbox_inches='tight')
        plt.close()

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
        'Our solution': {
            'read-p99':  419,
            'write-p99': 429,
            'throughput': 2645.50,
        },
        'gVisor':  {
            'read-p99':  554,
            'write-p99': 500,
            'throughput': 2183.41,
        },
        'Kata':    {
            'read-p99':  536,
            'write-p99': 448,
            'throughput': 2398.08,
        },
    },
    'Redis': {
        'Our solution': {
            'read-p99':  111,
            'write-p99': 98,
            'throughput': 16949.15,
        },
        'gVisor':  {
            'read-p99':  198,
            'write-p99': 189,
            'throughput': 8547.01,
        },
        'Kata':    {
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
for method in ['Our solution', 'gVisor', 'Kata']:
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
        'Our solution': {
            'latency-p99':  16.12,
            'throughput': 2270.57,
        },
        'gVisor':  {
            'latency-p99':  21.11,
            'throughput': 1661.38,
        },
        'Kata':    {
            'latency-p99':  21.50,
            'throughput': 1493.13,
        },
    },
    'PostgreSQL': {
        'Our solution': {
            'latency-p99':  4.33,
            'throughput': 6991.39,
        },
        'gVisor':  {
            'latency-p99':  9.22,
            'throughput': 3321.93,
        },
        'Kata':    {
            'latency-p99':  5.57,
            'throughput': 5006.76,
        },
    },
}

groups = data.keys()
xs = np.arange(len(groups))
latencies = {}
throughputs = {}
for method in ['Our solution', 'gVisor', 'Kata']:
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
