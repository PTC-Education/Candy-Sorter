from onshape_client.client import Client
import json
base = 'https://cad.onshape.com' # change this if you're using a document in an enterprise (i.e. "https://ptc.onshape.com")
exec(open('~/Documents/colabkeys.py').read())
client = Client(configuration={"base_url": base,
                               "access_key": access,
                               "secret_key": secret})
print('client configured')