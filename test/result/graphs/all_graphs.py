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


def grouped_bars(use_case, files, types, labels, value_transformers, bar_width=0.25, xticks_offset=0.25, ylabel='', ylim=None, output=''):
    data = {}
    for key, _ in value_transformers:
        data[key] = {}

    for path in (FOLDER / use_case).glob(files):
        test_type = get_type(path, types)
        with open(path) as f:
            values = json.load(f)

        for key, f in value_transformers:
            data[key][test_type] = f(values)

    x = np.arange(len(types))

    plt.figure()
    for i, (attribute, measurements) in enumerate(data.items()):
        offset = bar_width * i
        values = [measurements[t] for t in types]
        plt.bar(x + offset, values, bar_width, label=attribute)

    plt.ylabel(ylabel)
    plt.xticks(x + xticks_offset, [labels[t] for t in types])
    plt.legend(**OUTSIDE_LEGEND_PARAMS)
    plt.ylim(ylim)
    plt.savefig(f'out/{output}.pdf', bbox_inches='tight')


def scheduling_throughput(use_case, types, labels):
    grouped_bars(use_case,
                 files='SchedulingThroughputPrometheus*.json',
                 types=types,
                 labels=labels,
                 value_transformers=[
                     ('Average', lambda x: x['avg']),
                     ('Maximum', lambda x: x['max']),
                 ],
                 xticks_offset=0.125,
                 ylabel='Throughput [qps]',
                 ylim=(0, 75),
                 output=f'{use_case}-scheduling-throughput.pdf')


def scheduling_latency(use_case, types, labels):
    grouped_bars(use_case,
                 files='SchedulingMetrics*.json',
                 types=types,
                 labels=labels,
                 value_transformers=[
                     ('P50', lambda x: x['schedulingLatency']['Perc50'] / 1e6),
                     ('P90', lambda x: x['schedulingLatency']['Perc90'] / 1e6),
                     ('P99', lambda x: x['schedulingLatency']['Perc99'] / 1e6),
                 ],
                 ylabel='Latency [ms]',
                 ylim=(0, 3.7),
                 output=f'{use_case}-scheduling-latency.pdf')


def prometheus_mutation_duration(use_case, types, labels):
    grouped_bars(use_case,
                 files='GenericPrometheusQuery GatekeeperMutationRequestDuration*.json',
                 types=types,
                 labels=labels,
                 value_transformers=[
                     ('P50', lambda x: x['dataItems'][0]['data']['Perc50'] * 1000),
                     ('P90', lambda x: x['dataItems'][0]['data']['Perc90'] * 1000),
                     ('P99', lambda x: x['dataItems'][0]['data']['Perc99'] * 1000),
                 ],
                 ylabel='Duration [ms]',
                 ylim=(0, 1.3),
                 output=f'{use_case}-prometheus-mutation-duration.pdf')

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
