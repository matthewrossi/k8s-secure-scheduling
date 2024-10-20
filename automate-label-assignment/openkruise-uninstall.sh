#!/bin/bash

set -e

echo -e '[*] Uninstall OpenKruise'
helm uninstall kruise
