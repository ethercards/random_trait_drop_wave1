from web3.auto import w3  
import json
import os
import requests

test = True
results_folder = "results"
test_new_traits_folder = "random_drop_1"


def load_new_traits(i):
    # get appropriate number from rando
    if test:
        subfolder = os.path.join(test_new_traits_folder,(str(i % 100)))
        filename = os.path.join(subfolder,(str(i)+".json")) 
        with open(filename) as json_file:
            new_traits = json.load(json_file)
    else:
        new_traits_url = rando.functions.tokenURI(i).call()
        new_traits = json.loads(requests.get(new_traits_url).text)

    return(new_traits)

def allocate_drop():
    # load sales abi
    with open('sales_abi.json') as json_file:
        sales_abi = json.load(json_file)
           
    # load rando abi
    with open('rando_abi.json') as json_file:
        rando_abi = json.load(json_file)
           
    #print(abi)
    
    # making sure we are connected
    print(w3.isConnected())
    
    # initialize contract
    
    ec = w3.eth.contract(address='0x97CA7FE0b0288f5EB85F386FeD876618FB9b8Ab8', abi=sales_abi)
    rando = w3.eth.contract(address='0xdc21eB6f0dacFba4dE360f3C6548A9c4B708c123', abi=rando_abi)
    
    
    # create records folder if necessary
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
        new_traits = load_new_traits(i)
        print(new_traits)
        print("")
        
        # merge
    
        # save merged metadata
        print("==================================")
        
allocate_drop()


