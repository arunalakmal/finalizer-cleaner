#/usr/bin/python3
import atexit
import json
import requests
import subprocess
import sys

namespace = sys.argv[1]
application = sys.argv[2]

d = json.dumps({'metadata': {'finalizers': None}})

subprocess.run(["kubectl", "-n",namespace, "patch", "app", application, "-p", d, "--type", "merge"])

proxy_process = subprocess.Popen(['kubectl', 'proxy'])
atexit.register(proxy_process.kill)
p = subprocess.Popen(['kubectl', 'get', 'namespace', namespace, '-o', 'json'], stdout=subprocess.PIPE)
p.wait()
data = json.load(p.stdout)
data['spec']['finalizers'] = []
requests.put('http://127.0.0.1:8001/api/v1/namespaces/{}/finalize'.format(namespace), json=data).raise_for_status()
