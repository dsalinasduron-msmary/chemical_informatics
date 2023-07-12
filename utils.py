import requests
import json

def get_disease_query(disease_id, num_targets=100):
    # Build query string to get target information as well as count
    query_string = """
query AssociatedTargets {{
  disease(efoId: "{disease_id}") {{
    id
    name
    associatedTargets(page: {{ size: {num_targets}, index: 0 }}) {{
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

def parse_target_json(api_response):
    #create list of target IDs by calling them from dictionary
    target_ids = api_response['data']['disease']['associatedTargets']['rows']
    target_id_list = []
    #pull IDs from dictionary and add to new list
    return [ t_id['target'].get('id') for t_id in target_ids ]

def get_targets_from_api(disease_id, num_targets):
    query_string = get_disease_query(disease_id,num_targets)
    # Set variables object of arguments to be passed to endpoint
    variables = {"efoId": disease_id}

    # Set base URL of GraphQL API endpoint
    base_url = "https://api.platform.opentargets.org/api/v4/graphql"

    # Perform POST request and check status code of response
    r = requests.post(base_url, json={"query": query_string, "variables": variables})

    #Transform API response from JSON into Python dictionary and print in console
    return json.loads(r.text)

def get_targets(disease_id, num_targets):
    return parse_target_json(get_targets_from_api(disease_id,num_targets))

global target_json
target_json = get_targets_from_api("EFO_0005537",10)
