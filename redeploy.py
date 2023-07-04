#!/usr/bin/env python3

import requests
import datetime
from os import environ
from sys import argv

RANCHER_URL = environ.get('RANCHER_URL')
RANCHER_CLUSTER = environ.get('RANCHER_CLUSTER')
RANCHER_NAMESPACE = environ.get('RANCHER_NAMESPACE')
RANCHER_ACCESS_KEY = environ.get('RANCHER_ACCESS_KEY')
RANCHER_SECRET_KEY = environ.get('RANCHER_SECRET_KEY')
RANCHER_DEPLOYMENT_NAME = argv[1]

current_deployment = requests.get(
    f"{RANCHER_URL}/k8s/clusters/{RANCHER_CLUSTER}/v1/apps.deployments/{RANCHER_NAMESPACE}/{RANCHER_DEPLOYMENT_NAME}",
    auth=(RANCHER_ACCESS_KEY, RANCHER_SECRET_KEY),
    headers={
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache'
    }
)

current_deployment_json = current_deployment.json()
next_timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
current_deployment_json['spec']['template']['metadata']['annotations']['cattle.io/timestamp'] = next_timestamp

next_deployment = requests.put(
    f"{RANCHER_URL}/k8s/clusters/{RANCHER_CLUSTER}/v1/apps.deployments/{RANCHER_NAMESPACE}/{RANCHER_DEPLOYMENT_NAME}",
    auth=(RANCHER_ACCESS_KEY, RANCHER_SECRET_KEY),
    headers={
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    },
    json=current_deployment_json
)

next_deployment.raise_for_status()