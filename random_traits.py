import csv
import os
import json

def series(i):
    if i < 10:
        return("Creator")
    if i < 100:
        return("OG")
    if i < 1000:
        return("Alpha")
    return("Founder")

def generate_random_traits():
    # This function will generate the 10k random traits
    # so it can be used by the vrf smart contract

    randomtraits = []
    issued_traits = {}

    # load random traits
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
            randomtraits.append(trait)
            issued_traits[trait["name"]] = 0



    # create weighted card pool
    # OGs have 3x the chance to get picked
    # Alphas have 2x the chance
    # Founders have 1x the chance
    weighted_pool = []
    for i in range(10000):
        if series(i) == "OG":
            weighted_pool.append(i)
            weighted_pool.append(i)
            weighted_pool.append(i)
        if series(i) == "Alpha":
            weighted_pool.append(i)
            weighted_pool.append(i)
        if series(i) == "Founder":
            weighted_pool.append(i)


    # assign traits
    trait_array = []
    for i in range(10000):
        trait_array.append({"traits":[], "trait_types":[], "series":series(i)})


    for trait in randomtraits:
        # What series are eligible for the trait?
        # Some traits (for example Alpha upgrade) can only be applied on Founder cards
        eligibles = trait["card_type"].split(",")
        if eligibles[0] == "all":
            eligibles = ["og","alpha","founder"]
        for i in range(trait["max_issuance"]):

            winner = False
            while not winner:
                # pick a card. Any card.
                p = int.from_bytes(os.urandom(3),"little") % (len(weighted_pool) -1 )
                c = weighted_pool[p]       

                eligible = True
                
                ser = series(c).lower()
                if not (ser in eligibles):
                    #wrong series
                    eligible = False

                if trait["name"] in trait_array[c]["traits"]:
                    #Already has trait
                    eligible = False
            
                if trait["trait_type"] in trait_array[c]["trait_types"]:
                    #Already has trait type
                    eligible = False

                if eligible:
                    r = int.from_bytes(os.urandom(3),"little") % 10000
                    if r < trait["max_issuance"]:
                        winner = True

                        trait_array[c]["traits"].append(trait["name"])
                        if trait["trait_type"] != "":
                            trait_array[c]["trait_types"].append(trait["trait_type"])
                        issued_traits[trait["name"]] += 1

    # Issue rerolls
    for i in range(len(trait_array)):
        if trait_array[i]["series"] == "OG":
            if len(trait_array[i]["traits"]) == 0:
                trait_array[i]["traits"].append("Reroll")
            if len(trait_array[i]["traits"]) == 1:
                trait_array[i]["traits"].append("Reroll")
        if trait_array[i]["series"] == "Alpha":
            if len(trait_array[i]["traits"]) == 0:
                trait_array[i]["traits"].append("Reroll")

    # OG Traits
    og_traits = []
    alpha_traits = []
    founder_traits = []
    for i in range(len(trait_array)):
        x = trait_array[i]
        if x["series"] == "OG":
            og_traits.append(x)
        if x["series"] == "Alpha":
            alpha_traits.append(x)
        if x["series"] == "Founder":
            founder_traits.append(x)

    with open("./random_traits.json", "w") as write_file:
        json.dump(trait_array, write_file, indent=4)
    
    with open("./random_traits_og.json", "w") as write_file:
        json.dump(og_traits, write_file, indent=4)
    
    with open("./random_traits_alpha.json", "w") as write_file:
        json.dump(alpha_traits, write_file, indent=4)
    
    with open("./random_traits_founder.json", "w") as write_file:
        json.dump(founder_traits, write_file, indent=4)
        
    with open("./random_traits_issuance.json", "w") as write_file:
        json.dump(issued_traits, write_file, indent=4)


    # basic stats
    # traits on OGs
    ts = {}
    ts["Creator"] = {
            "count":0,
            "notraits":0
            }

    ts["OG"] = {
            "count":0,
            "notraits":0
            }

    ts["Alpha"] = {
            "count":0,
            "notraits":0
            }

    ts["Founder"] = {
            "count":0,
            "notraits":0
            }

    for i in range(len(trait_array)):
        x = trait_array[i]
        ts[x["series"]]["count"] += len(x["traits"])

        if len(x["traits"]) == 0:
            ts[x["series"]]["notraits"] += 1

    print(ts,"\n")
    print("OG Trait avg:", ts["OG"]["count"] / 90)
    print("\n")
    print("Alpha Trait avg:", ts["Alpha"]["count"] / 900)
    print("\n")
    print("Founder Trait avg:", ts["Founder"]["count"] / 9000)



generate_random_traits()
