#!/usr/bin/env python

import json
import matplotlib.pyplot as plt
import numpy as np
from cycler import cycler
from pathlib import Path

# For LaTeX-like fonts, comment if it errors out
plt.rcParams['font.family'] = 'NewComputerModern08'
plt.rcParams['font.size'] = 18
plt.rcParams['axes.prop_cycle'] = cycler('color', ['orchid', 'teal', 'purple'])

BAR_WIDTH = 0.25
OUTSIDE_LEGEND_PARAMS = {
    'bbox_to_anchor': (-0.15, 1.02, 1, 0.2), # x0, y0, width, height
    'frameon': False,
    'handlelength': 1,
    'loc': 'lower left',
    'ncol': 3,
    'columnspacing': 0.8,
    'handletextpad': 0.4,
}

# baseline taken from ../aqua-baseline-3cn-1000n-30kpods-uniform, from vanilla tests
# other data taken from ../aqua-3cn-1000n-30kpods-uniform
#
# Scheduling Latency in ms (if more values of p99, then the max)
# Throughput is qps (max value, if given more values then the minimum of the maximums)

data = {
    'Data\nSovereignty': {
        'scheduling-latency-p99': {
            'Baseline': 1.700,
            'Unconstrained': 1.803,
            'Constrained': 4.300,
        },
        'scheduling-latency-p90': {
            'Baseline': 0.922,
            'Unconstrained': 0.929,
            'Constrained': 1.396,
        },
        'scheduling-latency-p50': {
            'Baseline': 0.513,
            'Unconstrained': 0.516,
            'Constrained': 0.581,
        },
        'scheduling-throughput': {
            'Baseline': 146,
            'Unconstrained': 140,
            'Constrained': 137,
        },
    },
    'Multiple\nTenants': {
        'scheduling-latency-p99': {
            'Baseline': 1.684,
            'Unconstrained': 1.823,
            'Constrained': 3.689,
        },
        'scheduling-latency-p90': {
            'Baseline': 0.922,
            'Unconstrained': 0.927,
            'Constrained': 0.984,
        },
        'scheduling-latency-p50': {
            'Baseline': 0.512,
            'Unconstrained': 0.515,
            'Constrained': 0.547,
        },
        'scheduling-throughput': {
            'Baseline': 143,
            'Unconstrained': 140,
            'Constrained': 58.6,
        },
    },
    'Incompatible\nSecurity Levels': {
        'scheduling-latency-p99': {
            'Baseline': 1.748,
            'Unconstrained': 1.875,
            'Constrained': 3.512,
        },
        'scheduling-latency-p90': {
            'Baseline': 0.923,
            'Unconstrained': 0.931,
            'Constrained': 0.981,
        },
        'scheduling-latency-p50': {
            'Baseline': 0.513,
            'Unconstrained': 0.517,
            'Constrained': 0.545,
        },
        'scheduling-throughput': {
            'Baseline': 179,
            'Unconstrained': 143,
            'Constrained': 143,
        },
    },
}

groups = data.keys()
xs = np.arange(len(groups))
latencies = {}
throughputs = {}

for method in ['Baseline', 'Unconstrained', 'Constrained']:
    latencies[method] = [data[g]['scheduling-latency-p99'][method] for g in groups]
    plt.figure()
    _, ax = plt.subplots()
    m = 0
    for label, values in latencies.items():
        offset = BAR_WIDTH * m
        plt.bar(xs + offset, values, width=BAR_WIDTH, label=label)
        m += 1

    plt.xticks(xs + BAR_WIDTH, groups)
    plt.ylabel('Latency [ms]')
    plt.legend(**OUTSIDE_LEGEND_PARAMS)
    plt.savefig('scheduling-latency.pdf', bbox_inches='tight')

    throughputs[method] = [data[g]['scheduling-throughput'][method] for g in groups]
    plt.figure()
    m = 0
    for label, values in throughputs.items():
        offset = BAR_WIDTH * m
        plt.bar(xs + offset, values, width=BAR_WIDTH, label=label)
        m += 1

    plt.xticks(xs + BAR_WIDTH, groups)
    # yticks = range(0, 200, 40)
    # plt.yticks(ticks=yticks, labels=[f'{k}K' if k != 0 else '0' for k in yticks])
    plt.ylabel('Throughput [qps]')
    plt.legend(**OUTSIDE_LEGEND_PARAMS)
    plt.savefig('scheduling-throughput.pdf', bbox_inches='tight')

for use_case, values in data.items():
    print(use_case)
    for measure, results in values.items():
        print(f'  {measure}')
        print(f"    Unconstrained: {round((results['Unconstrained'] / results['Baseline'] - 1) * 100, 2)}%")
        print(f"    Constrained:   {round((results['Constrained'] / results['Baseline'] - 1) * 100, 2)}%")
