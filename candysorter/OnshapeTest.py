fixed_url = '/api/partstudios/d/did/w/wid/e/eid/massproperties'

# https://cad.onshape.com/documents/263517311c2ad139d4eb57ca/w/b45057ae06777e0c28bca6c5/e/d316bcbc694c9dbb6555f340
did = '263517311c2ad139d4eb57ca'
wid = 'b45057ae06777e0c28bca6c5'
eid = 'd316bcbc694c9dbb6555f340'

method = 'GET'

params = {}
payload = {}
headers = {'Accept': 'application/vnd.onshape.v1+json; charset=UTF-8;qs=0.1',
           'Content-Type': 'application/json'}

fixed_url = fixed_url.replace('did', did)
fixed_url = fixed_url.replace('wid', wid)
fixed_url = fixed_url.replace('eid', eid)

response = client.api_client.request(method, url=base + fixed_url, query_params=params, headers=headers, body=payload)

parsed = json.loads(response.data)
# The command below prints the entire JSON response from Onshape
print(json.dumps(parsed, indent=4, sort_keys=True))