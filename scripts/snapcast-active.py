#!/usr/bin/python3

# deps: avahi-utils

from functools import wraps
import telnetlib


def incrementing_id(func):
    id = 1
    @wraps(func)
    def wrapper(*args, **kwds):
        nonlocal id
        result = func(id, *args, **kwds)
        id += 1
        return result
    return wrapper

@incrementing_id
def doRequest(requestId, client, method, params=None):
    from json import dumps, loads
    request = {'method': method, 'jsonrpc': '2.0', 'id': requestId}
    if params:
        request.update({'params': params})
    # print("send: " + dumps(request))
    client.write((dumps(request) + "\r\n").encode('ascii'))
    while (True):
        response = client.read_until("\r\n".encode('ascii'), 2)
        jResponse = loads(response.decode())
        if 'id' in jResponse:
            if jResponse['id'] == requestId:
                if 'result' in jResponse:
                    return jResponse['result']
                elif 'error' in jResponse:
                    raise Exception(jResponse['error'])
    return

def avahi_entries():
    from subprocess import run
    try:
        ret = run(["avahi-browse", "-trp", "_snapcast-jsonrpc._tcp"], capture_output=True, check=True, text=True).stdout
    except TypeError:
        from subprocess import check_output
        ret = check_output(["avahi-browse", "-trp", "_snapcast-jsonrpc._tcp"], universal_newlines=True)
    return list((r[7], int(r[8])) for r in (r.split(';') for r in ret.split("\n")) if r[0] == '=')

def has_active_streams(client):
    res = doRequest(client, 'Server.GetStatus')
    groups = res['server']['groups']
    return any(not g['muted'] for g in groups)

if __name__ == '__main__':
    active = False
    for server, port in avahi_entries():
        try:
            # print(server, port)
            telnet = telnetlib.Telnet(server, port)
            active = active or has_active_streams(telnet)
        except OSError:
            telnet = None
        finally:
            if telnet:
                telnet.close()
    from sys import exit
    if not active:
        exit(1)
    exit(0)
