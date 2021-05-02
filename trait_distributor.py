from web3.auto import w3  
import json
import os
import requests
import csv

# important variables
test_new_traits_folder = "random_drop_1"     # this is where the calculated new random traits sit
results_folder         = "results"           # the new metadata goes here
traitsi_file           = "random_traits.csv" # document with trait names and descriptions

rando = ""

def load_traits():
    traits = {}
    with open('random_traits.csv', newline='') as f:
        reader = csv.reader(f)
        raw_traits = list(reader)
        raw_traits.pop(0)

        for t in raw_traits:
            trait={}
            trait["name"]               = t[0]
            trait["card_type"]          = t[1]
            trait["trait_type"]         = t[2]
            trait["max_issuance"]       = int(t[3])
            trait["description"]        = t[4]
            traits[trait["name"]] = trait

    return traits


def load_new_traits(i):
    # get appropriate number from rando
    new_traits_url = rando.functions.tokenURI(i).call()
    new_traits = json.loads(requests.get(new_traits_url).text)
    return(new_traits)

def allocate_drop():
    global rando

    # load traits
    traits = load_traits()

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
        nt = load_new_traits(i)
        new_traits = nt["traits"]
       
        # loop through new traits and find descriptions
        for t in new_traits:
            print(traits[t])
        # merge
    
        # save merged metadata
        print("==================================")
        
allocate_drop()


