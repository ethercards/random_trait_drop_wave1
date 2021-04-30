from web3.auto import w3  
import json
import os
import requests

# load abi
with open('sales_abi.json') as json_file:
    abi = json.load(json_file)
       
#print(abi)

# making sure we are connected
print(w3.isConnected())

# initialize contract

ec = w3.eth.contract(address='0x97CA7FE0b0288f5EB85F386FeD876618FB9b8Ab8', abi=abi)


# create records folder if necessary
results_folder = "results"
if not os.path.exists(results_folder):
    os.makedirs(results_folder)


# loop through the 10k tokens
# and merge the new traits with the metadata

for i in range(10000):
    print("card",i)
    print("")
    # create subfolder if needed
    subfolder = os.path.join(results_folder,(str(i % 100)))
    if not os.path.exists(subfolder):
        os.makedirs(subfolder)

    # load existing metadata
    metadata_url = ec.functions.tokenURI(i).call()
    metadata = json.loads(requests.get(metadata_url).text)
    print("metadata:")
    print(metadata)
    print("")
    
    # load new traits
    print("new traits:")
    print(new_trait)
    print("")
    # merge
    # save merged metadata
