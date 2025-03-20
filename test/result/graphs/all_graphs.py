#!/usr/bin/env python

import json
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# For LaTeX-like fonts, comment if it errors out
plt.rcParams['font.family'] = 'NewComputerModern08'
plt.rcParams['font.size'] = 15

OUTSIDE_LEGEND_PARAMS = {
    'bbox_to_anchor': (0, 1.02, 1, 0.2), # x0, y0, width, height
    'frameon': False,
    'loc': 'lower left',
    'ncol': 3,
}

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

    width = 0.25
    for i, (attribute, measurements) in enumerate(data.items()):
        offset = width * i
        values = [measurements[t] for t in types]
        rects = plt.bar(x + offset, values, width, label=attribute)

    # Add some text for labels, title and custom x-axis tick labels, etc.
    plt.ylabel('Throughput [qps]')
    plt.xticks(x + width / 2, [labels[t] for t in types])
    plt.legend(**OUTSIDE_LEGEND_PARAMS)
    plt.ylim(0, 75)

    plt.savefig(f'out/{use_case}-scheduling-throughput.pdf', bbox_inches='tight')


def scheduling_latency(use_case, types, labels):
    data = {
        'P50': {},
        'P90': {},
        'P99': {},
    }

    for path in (FOLDER / use_case).glob('SchedulingMetrics*.json'):
        test_type = get_type(path, types)
        with open(path) as f:
            values = json.load(f)

        data['P50'][test_type] = values['schedulingLatency']['Perc50'] / 1e6
        data['P90'][test_type] = values['schedulingLatency']['Perc90'] / 1e6
        data['P99'][test_type] = values['schedulingLatency']['Perc99'] / 1e6

    x = np.arange(len(types)) # label locations

    plt.figure()

    width = 0.25
    for i, (attribute, measurements) in enumerate(data.items()):
        offset = width * i
        values = [measurements[t] for t in types]
        rects = plt.bar(x + offset, values, width, label=attribute)

    # Add some text for labels, title and custom x-axis tick labels, etc.
    plt.ylabel('Scheduling Latency [ms]')
    plt.xticks(x + width, [labels[t] for t in types])
    plt.legend(**OUTSIDE_LEGEND_PARAMS)
    plt.ylim(0, 3.7)

    plt.savefig(f'out/{use_case}-scheduling-latency.pdf', bbox_inches='tight')


def prometheus_mutation_duration(use_case, types, labels):
    data = {
        'P50': {},
        'P90': {},
        'P99': {},
    }

    for path in (FOLDER / use_case).glob('GenericPrometheusQuery GatekeeperMutationRequestDuration*.json'):
        test_type = get_type(path, types)
        with open(path) as f:
            values = json.load(f)

        data['P50'][test_type] = values['dataItems'][0]['data']['Perc50'] * 1000
        data['P90'][test_type] = values['dataItems'][0]['data']['Perc90'] * 1000
        data['P99'][test_type] = values['dataItems'][0]['data']['Perc99'] * 1000

    x = np.arange(len(types)) # label locations

    plt.figure()
    # fig, ax = plt.subplots(layout='constrained')

    width = 0.25
    for i, (attribute, measurements) in enumerate(data.items()):
        offset = width * i
        values = [measurements[t] for t in types]
        rects = plt.bar(x + offset, values, width, label=attribute)

    # Add some text for labels, title and custom x-axis tick labels, etc.
    plt.ylabel('Duration [ms]')
    plt.xticks(x + width, [labels[t] for t in types])
    # ax.legend(loc='upper left')
    # outside_legend(plt)
    plt.legend(**OUTSIDE_LEGEND_PARAMS)
    plt.ylim(0, 1.3)

    plt.savefig(f'out/{use_case}-prometheus-mutation-duration.pdf', bbox_inches='tight')

# ================================================ Multi tenancy

# ------------------------- Scheduling Throughput

TYPES = ['vanilla', 'uc1', 'uc2']
LABELS = {'uc1': 'Tenant A', 'uc2': 'Tenant B', 'vanilla': 'Unconstrained'}

scheduling_throughput(use_case='multi-tenancy-test', types=TYPES, labels=LABELS)
scheduling_latency(use_case='multi-tenancy-test', types=TYPES, labels=LABELS)
prometheus_mutation_duration(use_case='multi-tenancy-test', types=TYPES, labels=LABELS)
 
# ================================================ Data Sovereignty

# ------------------------- Scheduling Throughput

TYPES = ['vanilla', 'eu-region', 'us-region']
LABELS = {'eu-region': 'EEA', 'us-region': 'US', 'vanilla': 'Unconstrained'}

scheduling_throughput(use_case='data-sovereignty-test', types=TYPES, labels=LABELS)
scheduling_latency(use_case='data-sovereignty-test', types=TYPES, labels=LABELS)
prometheus_mutation_duration(use_case='data-sovereignty-test', types=TYPES, labels=LABELS)

# ================================================ Workload Security Rings

# ------------------------- Scheduling Throughput

TYPES = ['vanilla', 'unhandened', 'sensitive'] # yes, there's a typo in the file names
LABELS = {'unhandened': 'Unhardened', 'sensitive': 'Sensitive', 'vanilla': 'Unconstrained'}

scheduling_throughput(use_case='workload-security-rings-test', types=TYPES, labels=LABELS)
scheduling_latency(use_case='workload-security-rings-test', types=TYPES, labels=LABELS)
prometheus_mutation_duration(use_case='workload-security-rings-test', types=TYPES, labels=LABELS)
