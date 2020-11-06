#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2020 xaj

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import requests, os

auth_head = {'API-Key': os.getenv("VULTR_KEY")}
api_url = "https://api.vultr.com/v1"
snapshot_list_url = api_url + '/snapshot/list'
server_create_url = api_url + '/server/create'

server_list_url = api_url + '/server/list'
server_list = requests.get(server_list_url, headers=auth_head)

if server_list.json():
    for k,v in server_list.json().items():
        if v['label'] == 'auto_deployed_server':
            exit(-1)

snapshots = requests.get(snapshot_list_url, headers=auth_head)

server_create_data={'DCID':25, 'VPSPLANID':201, 'OSUD':164, 'label':'auto_deployed_server'}

if snapshots.json():
    for k,v in snapshots.json().items():
        if v['description'] == 'auto_created_snapshot':
            server_create_data['SNAPSHOTID']=k
            break

if 'SNAPSHOTID' not in server_create_data:
    exit(-1)

res = requests.post(server_create_url, headers=auth_head, data=server_create_data)

if res.status_code != 200:
    exit(-1)
