#!/usr/bin/env python
import requests

params = [('custom', '1'), ('cmd', 2001)]
params.append(('str', '1'))

r = requests.get("http://192.168.1.254/", params=params)
print(r)
