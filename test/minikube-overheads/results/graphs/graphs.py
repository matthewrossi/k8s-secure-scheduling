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

# The legend as a separate image

fig = plt.figure()
ax = fig.add_subplot(111)

legend = plt.figure()
line1, = ax.bar(0, 100)
line2, = ax.bar(0, 100)
line3, = ax.bar(0, 100)

legend.legend([line1, line2, line3], ['Our solution', 'gVisor', 'Kata'], loc='center', ncol=3, handlelength=1, columnspacing=0.8, frameon=False)
legend.savefig('legend.pdf', bbox_inches='tight')

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

software = data.keys()
percentiles = [50, 90, 99]
xs = np.arange(len(percentiles))
methods = ['Our solution', 'gVisor', 'Kata']
latencies = {}
throughputs = {}

# Latencies

for soft in software:
    for method in methods:
        latencies[method] = [data[soft][method][f'latency-p{p}'] for p in percentiles]

    plt.figure()
    m = 0
    for label, values in latencies.items():
        offset = BAR_WIDTH * m
        plt.bar(xs + offset, values, width=BAR_WIDTH, label=label)
        m += 1

    plt.xticks(xs + BAR_WIDTH, [f'P{p}' for p in percentiles])
    plt.ylabel('Latency [ms]')
    # plt.legend(**OUTSIDE_LEGEND_PARAMS)
    plt.savefig(f'{soft.lower()}-latency.pdf', bbox_inches='tight')
    plt.close()

# Throughputs

with plt.rc_context({'xtick.color': 'white'}):
    for soft in software:
        for method in methods:
            throughputs[method] = [data[soft][method]['throughput'] / 1000]

        plt.figure(figsize=(3, 5.5))
        m = 0
        for label, values in throughputs.items():
            offset = BAR_WIDTH * m
            plt.bar(offset, values, width=BAR_WIDTH, label=label)
            m += 1

        plt.xlim(-0.4, 0.9)
        plt.xticks([0])
        yticks = range(0, 200, 50)
        plt.yticks(ticks=yticks, labels=[f'{k}K' if k != 0 else '0' for k in yticks])
        plt.ylabel('Throughput [req/s]')
        # plt.legend(**OUTSIDE_LEGEND_PARAMS)
        plt.savefig(f'{soft.lower()}-throughput.pdf', bbox_inches='tight')
        plt.close()


# ============================================================ NoSQL

# Latency in us
data = {
    'MongoDB': {
        'Our solution': {
            'read-p99':  413, 'read-p90':  266, 'read-p50':  155,
            'write-p99': 357, 'write-p90': 246, 'write-p50': 156,
            'throughput': 2801.12,
        },
        'gVisor':  {
            'read-p99':  461, 'read-p90':  371, 'read-p50':  253,
            'write-p99': 549, 'write-p90': 365, 'write-p50': 258,
            'throughput': 2222.22,
        },
        'Kata':    {
            'read-p99':  801,  'read-p90':  333, 'read-p50':  198,
            'write-p99': 2341, 'write-p90': 347, 'write-p50': 219,
            'throughput': 2262.44,
        },
    },
    'Redis': {
        'Our solution': {
            'read-p99':  110, 'read-p90':  48, 'read-p50':  33,
            'write-p99': 101, 'write-p90': 53, 'write-p50': 37,
            'throughput': 15873.02,
        },
        'gVisor':  {
            'read-p99':  194, 'read-p90':  112, 'read-p50':  83,
            'write-p99': 184, 'write-p90': 124, 'write-p50': 86,
            'throughput': 8928.57,
        },
        'Kata':    {
            'read-p99':  106, 'read-p90':  82, 'read-p50':  65,
            'write-p99': 129, 'write-p90': 82, 'write-p50': 66,
            'throughput': 11111.11,
        },
    },
}

software = data.keys()
percentiles = [50, 90, 99]
xs = np.arange(len(percentiles))
methods = ['Our solution', 'gVisor', 'Kata']
latencies = {}
throughputs = {}

# Latencies

for soft in software:
    for method in methods:
        latencies[method] = [max(data[soft][method][f'read-p{p}'], data[soft][method][f'write-p{p}']) / 1000 for p in percentiles]

    plt.figure()
    m = 0
    for label, values in latencies.items():
        offset = BAR_WIDTH * m
        plt.bar(xs + offset, values, width=BAR_WIDTH, label=label)
        m += 1

    plt.xticks(xs + BAR_WIDTH, [f'P{p}' for p in percentiles])
    plt.ylabel('Latency [ms]')
    # plt.legend(**OUTSIDE_LEGEND_PARAMS)
    plt.savefig(f'{soft.lower()}-latency.pdf', bbox_inches='tight')
    plt.close()

# Throughputs

ticks = {
    'MongoDB': range(0, 4),
    'Redis': range(0, 21, 5),
}

with plt.rc_context({'xtick.color': 'white'}):
    for soft in software:
        for method in methods:
            throughputs[method] = [data[soft][method]['throughput'] / 1000]

        plt.figure(figsize=(3, 5.5))
        m = 0
        for label, values in throughputs.items():
            offset = BAR_WIDTH * m
            plt.bar(offset, values, width=BAR_WIDTH, label=label)
            m += 1

        plt.xticks([0])
        plt.xlim(-0.4, 0.9)
        yticks = ticks[soft]
        plt.yticks(ticks=yticks, labels=[f'{k}K' if k != 0 else '0' for k in yticks])
        plt.ylabel('Throughput [q/s]')
        # plt.legend(**OUTSIDE_LEGEND_PARAMS)
        plt.savefig(f'{soft.lower()}-throughput.pdf', bbox_inches='tight')
        plt.close()


# ============================================================ SQL (Sysbench)

# Latency in ms
# throughput is the best among all three
data = {
    'MySQL': {
        'Our solution': {
            'latency-p99':  26.68, 'latency-p90': 20.74, 'latency-p50': 11.45,
            'throughput': 1485.43,
        },
        'gVisor':  {
            'latency-p99':  26.20, 'latency-p90': 21.89, 'latency-p50': 16.41,
            'throughput': 1168.28,
        },
        'Kata':    {
            'latency-p99':  33.12, 'latency-p90': 22.28, 'latency-p50': 13.22,
            'throughput': 1318.14,
        },
    },
    'PostgreSQL': {
        'Our solution': {
            'latency-p99':  5.28, 'latency-p90': 3.13, 'latency-p50': 2.86,
            'throughput': 6782.39,
        },
        'gVisor':  {
            'latency-p99':  10.65, 'latency-p90': 9.56, 'latency-p50': 8.58,
            'throughput': 3234.48,
        },
        'Kata':    {
            'latency-p99':  9.06, 'latency-p90': 5.88, 'latency-p50': 5.37,
            'throughput': 3690.98,
        },
    },
}

software = data.keys()
percentiles = [50, 90, 99]
xs = np.arange(len(percentiles))
methods = ['Our solution', 'gVisor', 'Kata']
latencies = {}
throughputs = {}

# Latencies

for soft in software:
    for method in methods:
        latencies[method] = [data[soft][method][f'latency-p{p}'] for p in percentiles]

    plt.figure()
    m = 0
    for label, values in latencies.items():
        offset = BAR_WIDTH * m
        plt.bar(xs + offset, values, width=BAR_WIDTH, label=label)
        m += 1

    plt.xticks(xs + BAR_WIDTH, [f'P{p}' for p in percentiles])
    plt.ylabel('Latency [ms]')
    # plt.legend(**OUTSIDE_LEGEND_PARAMS)
    plt.savefig(f'{soft.lower()}-latency.pdf', bbox_inches='tight')
    plt.close()

# Throughputs

ticks = {
    'MySQL': range(0, 2),
    'PostgreSQL': range(0, 8),
}

with plt.rc_context({'xtick.color': 'white'}):
    for soft in software:
        for method in methods:
            throughputs[method] = [data[soft][method]['throughput'] / 1000]

        plt.figure(figsize=(3, 5.5))
        m = 0
        for label, values in throughputs.items():
            offset = BAR_WIDTH * m
            plt.bar(offset, values, width=BAR_WIDTH, label=label)
            m += 1

        plt.xlim(-0.4, 0.9)
        plt.xticks([0])
        yticks = ticks[soft]
        plt.yticks(ticks=yticks, labels=[f'{k}K' if k != 0 else '0' for k in yticks])
        plt.ylabel('Throughput [q/s]')
        # plt.legend(**OUTSIDE_LEGEND_PARAMS)
        plt.savefig(f'{soft.lower()}-throughput.pdf', bbox_inches='tight')
        plt.close()
