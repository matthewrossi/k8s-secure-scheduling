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
        },
        'gVisor':  {
            'read':  {'P90': 435, 'P99': 554},
            'write': {'P90': 408, 'P99': 500},
        },
        'QEMU':    {
            'read':  {'P90': 401, 'P99': 536},
            'write': {'P90': 371, 'P99': 448},
        },
    },
    'Redis': {
        'containerd': {
            'read':  {'P90':  68, 'P99': 111},
            'write': {'P90':  75, 'P99':  98},
        },
        'gVisor':  {
            'read':  {'P90': 140, 'P99': 198},
            'write': {'P90': 150, 'P99': 189},
        },
        'QEMU':    {
            'read':  {'P90': 100, 'P99': 124},
            'write': {'P90': 109, 'P99': 147},
        },
    },
}

# ------------------------------------ Latency graphs

def mean(*args):
    return sum(args) / len(args)

for dbms in data.keys():
    width = 0.25   # bar width

    groups = list(data[dbms].keys())
    percentiles = {}
    for perc in ['P90', 'P99']:
        percentiles[perc] = [mean(data[dbms][g]['read'][perc], data[dbms][g]['write'][perc]) for g in groups]
        
    plt.figure()

    x = np.arange(len(groups))
    m = 0
    for attribute, measurement in percentiles.items():
        offset = width * m
        plt.bar(x + offset, measurement, width, label=attribute)
        m += 1

    plt.xticks(x + width / 2, groups)
    plt.ylabel('Latency [μs]')
    plt.legend(loc='upper left')
    plt.ylim(0, 565)

    plt.savefig(f'{dbms}-latency.pdf', bbox_inches='tight')

    print('For DBMS', dbms)
    for p in ['P90', 'P99']:
        print(f'  {p}')
        for g in ['gVisor', 'QEMU']:
            inc = mean(data[dbms][g]['read'][p], data[dbms][g]['write'][p]) / mean(data[dbms]['containerd']['read'][perc], data[dbms]['containerd']['write'][p]) - 1
            print(f'    {g}:', inc * 100)
