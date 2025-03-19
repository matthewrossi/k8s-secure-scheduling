#!/usr/bin/env python

import json
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

FOLDER = Path('../anthem-kind-3-control-1000-fake-worker-nodes-30k-pods')

def get_type(path, types=[]):
    for t in types:
        if t in path.as_posix():
            return t
    return None


def scheduling_throughput(use_case, types, labels):
    data = {
        'Average': {},
        'Maximum': {},
    }

    for path in (FOLDER / use_case).glob('SchedulingThroughputPrometheus_direct-scheduler*.json'):
        test_type = get_type(path, types)
        with open(path) as f:
            values = json.load(f)
        data['Average'][test_type] = values['avg']
        data['Maximum'][test_type] = values['max']

    x = np.arange(len(types)) # label locations

    plt.figure()
    fig, ax = plt.subplots(layout='constrained')

    width = 0.25
    for i, (attribute, measurements) in enumerate(data.items()):
        offset = width * i
        values = [measurements[t] for t in types]
        rects = ax.bar(x + offset, values, width, label=attribute)

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Throughput [qps]')
    ax.set_xticks(x + width / 2, [labels[t] for t in types])
    ax.legend(loc='upper left')
    ax.set_ylim(0, 75)

    plt.savefig(f'out/{use_case}-scheduling-throughput.pdf', bbox_inches='tight')


def scheduling_latency(use_case, types, labels):
    data = {
        '50th percentile': {},
        '90th percentile': {},
        '99th percentile': {},
    }

    for path in (FOLDER / use_case).glob('SchedulingMetrics*.json'):
        test_type = get_type(path, types)
        with open(path) as f:
            values = json.load(f)

        data['50th percentile'][test_type] = values['schedulingLatency']['Perc50'] / 1000
        data['90th percentile'][test_type] = values['schedulingLatency']['Perc90'] / 1000
        data['99th percentile'][test_type] = values['schedulingLatency']['Perc99'] / 1000

    x = np.arange(len(types)) # label locations

    plt.figure()
    fig, ax = plt.subplots(layout='constrained')

    width = 0.25
    for i, (attribute, measurements) in enumerate(data.items()):
        offset = width * i
        values = [measurements[t] for t in types]
        rects = ax.bar(x + offset, values, width, label=attribute)

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Scheduling Latency [ms]')
    ax.set_xticks(x + width, [labels[t] for t in types])
    ax.legend(loc='upper left')
    ax.set_ylim(0, 3700)

    plt.savefig(f'out/{use_case}-scheduling-latency.pdf', bbox_inches='tight')

# ================================================ Multi tenancy

# ------------------------- Scheduling Throughput

TYPES = ['vanilla', 'uc1', 'uc2']
LABELS = {'uc1': 'Tenant A', 'uc2': 'Tenant B', 'vanilla': 'Unconstrained'}

scheduling_throughput(use_case='multi-tenancy-test', types=TYPES, labels=LABELS)
scheduling_latency(use_case='multi-tenancy-test', types=TYPES, labels=LABELS)
 
# ================================================ Data Sovereignty

# ------------------------- Scheduling Throughput

TYPES = ['vanilla', 'eu-region', 'us-region']
LABELS = {'eu-region': 'European Economic Area', 'us-region': 'United States', 'vanilla': 'Unconstrained'}

scheduling_throughput(use_case='data-sovereignty-test', types=TYPES, labels=LABELS)
scheduling_latency(use_case='data-sovereignty-test', types=TYPES, labels=LABELS)

# ================================================ Workload Security Rings

# ------------------------- Scheduling Throughput

TYPES = ['vanilla', 'unhandened', 'sensitive'] # yes, there's a typo in the file names
LABELS = {'unhandened': 'Unhardened', 'sensitive': 'Sensitive', 'vanilla': 'Unconstrained'}

scheduling_throughput(use_case='workload-security-rings-test', types=TYPES, labels=LABELS)
scheduling_latency(use_case='workload-security-rings-test', types=TYPES, labels=LABELS)
