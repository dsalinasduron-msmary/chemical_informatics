import json
import requests
import pandas as pd
import logging

# TARGETS

def get_disease_query(disease_id, num_targets=100):
    # Build query string to get target information as well as count
    query_string = """
query AssociatedTargets {{
  disease(efoId: "{disease_id}") {{
    id
    name
    associatedTargets(page: {{ size: {num_targets}, index: 0 }}) {{
      count
      rows {{
        target {{
          id
          approvedName
          approvedSymbol
        }}
        score
      }}
    }}
  }}
}}
    """.format(disease_id=disease_id,num_targets=num_targets)
    return query_string


def get_targets_json_from_api(disease_id, num_targets):
    query_string = get_disease_query(disease_id,num_targets)
    # Set variables object of arguments to be passed to endpoint
    variables = {"efoId": disease_id}

    # Set base URL of GraphQL API endpoint
    base_url = "https://api.platform.opentargets.org/api/v4/graphql"

    # Perform POST request and check status code of response
    r = requests.post(base_url, json={"query": query_string, "variables": variables})

    # Report error if code not OK
    if(r.status_code != 200) :
        logging.warning("Did not receive OK status code (200) when requesting " + str(disease_id) + "from OpenTargets.")
        logging.warning("Received status code  " + str(r.status_code))
        return None

    #Transform API response from JSON into Python dictionary and print in console
    return json.loads(r.text)

def get_num_targets(disease_id):
    response_dict = get_targets_json_from_api(disease_id, num_targets = 1)
    count = response_dict['data']['disease']['associatedTargets']['count']
    return count

def get_targets(disease_id, num_targets):
    return get_target_dataframe(get_targets_json_from_api(disease_id,num_targets))

def get_all_targets(disease_id):
    num_targets = get_num_targets(disease_id)
    return get_targets(disease_id, num_targets)

def make_dataframe_row(disease_efo,disease_name,row):
    return(disease_efo,disease_name,row["target"]["approvedName"],row["score"],row["target"]["id"])

def get_target_dataframe(target_json):
    fields = ["disease_efo","disease_name","target_short_name","target_score","target_ensg"]
    target_list = target_json["data"]["disease"]["associatedTargets"]["rows"]
    disease_efo = target_json["data"]["disease"]["id"]
    disease_name = target_json["data"]["disease"]["name"]
    return pd.DataFrame([ make_dataframe_row(disease_efo,disease_name,row) for row in target_list ],columns=fields)

# ASSAYS and COMPOUNDS
def get_assay_json_from_target(target_id):
    r = requests.get('https://pubchem.ncbi.nlm.nih.gov/rest/pug/gene/synonym/Ensemble:' + target_id + '/aids/json')
    
    # Report error if code not OK 
    if(r.status_code != 200) :
        logging.warning("Did not receive OK status code (200) when requesting " + str(target_id) + "from PubChem.")
        logging.warning("Received status code  " + str(r.status_code))
        return None
    return r.json()

def get_assay_list(target_id,target_json):
    # unpack assay_ids into a list containing just the AIDs from the dictionary
    try:
        aids = target_json['InformationList']['Information'][0]['AID']
        return aids
    except:
        logging.info("Target " + str(target_id) + "has no assays on PubChem.")
        return None
    
def get_compounds_and_assays(target_list):
    # Create dataframe assigning assays to to each target, and assigning compounds to each assay using PUG REST
    # df = pd.DataFrame()
    tca = []
    for target in target_list :
        # about  4 targets/second
        target_json = get_assay_json_from_target(target)
        if target_json != None :
            assay_ids = get_assay_list(target,target_json)
            if assay_ids != None :
                for aid in assay_ids:
                    assay_pubchem = get_assay_pubchem(aid)
                    if assay_pubchem != None :
                        compounds = get_compound_data(aid, assay_pubchem)
                        if compounds != None :
                            return compounds
    return tca

def get_assay_pubchem(assay_id):
    # Get raw assay data, including CIDs and Activity data, from PubChem.
    r = requests.get('https://pubchem.ncbi.nlm.nih.gov/assay/pcget.cgi?query=download&record_type=datatable&actvty=active&response_type=display&aid={}'.format(assay_id))
    if (r.status_code != 200):
        logging.info("Could not retrieve assay {} from PubChem".format(assay_id))
        return None
    return r.text

def get_compound_data(assay_id,assay_pubchem):
    # Get the index of the information you want, to grab from those columns later
    listed_data = assay_pubchem.split(',')
    # Gets index of CID location, and passes to next assay if CID column is not found
    try:   
        cid_index = listed_data.index("PUBCHEM_CID")
        IC50_index = listed_data.index("IC50")
        standard_score_index = listed_data.index("PubChem Standard Value")
        return 1
    except:
        logging.warning("Missing on or more of: active compound IDs or IC50 standard score in assay {} ".format(assay_id))
        return None
"""
fhand = io.StringIO(loose_data)
"""

def assay():
    pass
    """
    for target_id in target_list:
        #target_id = target_id[0]
        # get raw AIDs (Assay IDs) for each Ensemble ID in JSON format using PUG REST
        r = requests.get('https://pubchem.ncbi.nlm.nih.gov/rest/pug/gene/synonym/Ensemble:' + target_id + '/aids/json')
        # convert JSON to Python Dictionary
        raw_aids = r.json()
        # isolate raw_aids into a list containing just the AIDs from the dictionary
        try:
            aids = raw_aids['InformationList']['Information'][0]['AID']
        except:
            pass
        # assign each Ensemble Target ID to dictionary entry with associated Assay IDs
        # target_id_assay_dict[id] =  aids
            
        # create sub-dictionary for compounds within each assay
        target_id_assay_dict[target_id] =  {}
        for aid in aids:
            aid = str(aid)
            #print(aid)
            # Get raw assay data, including CIDs and Activity data, from PubChem.
            r = requests.get('https://pubchem.ncbi.nlm.nih.gov/assay/pcget.cgi?query=download&record_type=datatable&actvty=active&response_type=display&aid=' + aid)
            
            # Convert data to string
            loose_data = r.text

            
            # Get the index of the information you want, to grab from those columns later
            listed_data = loose_data.split(',')
            # Gets index of CID location, and passes to next assay if CID column is not found
            try:   
                cid_index = listed_data.index("PUBCHEM_CID")
                #print(cid_index)
                #print(type(cid_index))
            except:
                #print("no CIDs found")
                continue
            # Gets index of IC50 column (essentially looks to see of "IC50" is anywhere), and passes if IC50 is not used
            try:
                IC50_index = listed_data.index("IC50")
                #print(IC50_index)
                #print(type(IC50_index))
            except:
                #print("no IC50 found")
                continue
            # Gets index of Pubchem Standard Value (standard unit conversion from IC0, EC50, etc.) and passes to next assay if not found
            try:
                standard_score_index = listed_data.index("PubChem Standard Value")
            except:
                #print("no standard value found")
                continue
            
            fhand = io.StringIO(loose_data)

            cids_with_activities = []
            # Split each line into a list, and use found indicies to get desired data
            for line in fhand:
                line = line.split(',')
                #print(line)
                try:
                    int(line[0])
                    int(line[cid_index])
                    #float(line[IC50_index])
                    float(line[standard_score_index])
                except:
                    line = ""
                    continue
                cid_with_activity = (line[cid_index], line[standard_score_index])
                cids_with_activities.append(cid_with_activity)
            #isolate raw_cids into a list containing just the CIDs from the dictionary
            if len(cids_with_activities) > 0:
                #assign CIDs to associated AID dictionary entry
                target_id_assay_dict[target_id][aid] = cids_with_activities
                print("Compounds found! Adding compounds to dictionary and passing to next assay.")
            else:
                print("No compounds found for assay. Passing to next assay.")
                continue
            
        a+=1
        display(a)
    print(target_id_assay_dict)
    """
