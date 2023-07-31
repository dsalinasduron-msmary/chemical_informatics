import pandas as pd
from collections import defaultdict
from sqlalchemy import create_engine
from sqlalchemy import text

from dotenv import dotenv_values

config = dotenv_values('database_url.env')
url = config['DATABASE_URL']

engine = create_engine(url, echo=False)


# grab targets from disease database
def get_targets(disease_id):
    with engine.begin() as conn:
        query = text("SELECT * FROM disease_to_target WHERE disease_id = '{disease_id}';".format(disease_id = disease_id))
        disease_df = pd.read_sql(query, conn)
    return disease_df

disease_id = "EFO_0005537"
df = get_targets(disease_id)
print(df)

"""
target_ids = disease_df.sort_values(by = ['association_score'], ascending=False)['target_ensemble_id'].values
print(target_ids)
target_id = target_ids[1]

print(target_id)
print(type(target_id))
"""
