import json
import os

# creating folder structure for the VRF script

def create_folders():
    # Load json
    with open('random_traits.json') as json_file:
        traits = json.load(json_file)

    # create root folder if needed
    rootfolder = "random_drop_1"

    if not os.path.exists(rootfolder):
        os.makedirs(rootfolder)

    # create json files
    for i, trait in enumerate(traits):

        subfolder = os.path.join(rootfolder,(str(i % 100)))
        if not os.path.exists(subfolder):
            os.makedirs(subfolder)
    
        jsonname = str(i)+".json"
        filename = os.path.join(subfolder,jsonname)
   

        print("creating json:" + filename)
        with open(filename, "w") as write_file:
            json.dump(trait, write_file, indent=4)

create_folders()
