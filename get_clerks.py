import re

import requests
import pandas as pd

CIRCUIT_CLERKS_URL = "https://kcoj.kycourts.net/ContactList/Search/Results"
CIRCUIT_CLERKS_BODY = {"SelectedCategory": "CCC", "SelectedCounty": "All"}

ADDRESS_RE = re.compile(r"[\w ]+ Circuit Court( Court)? Clerk\s?")
NEW_LINE_RE = re.compile(r"<br/>\n?")

if __name__ == "__main__":
    res = requests.post(CIRCUIT_CLERKS_URL, data=CIRCUIT_CLERKS_BODY)
    clerks_list_df = pd.read_html(NEW_LINE_RE.sub("*NEW*", ADDRESS_RE.sub("", res.text)))[0]
    clerks_list_df['Phone Number'] = clerks_list_df['Phone Number'].apply(lambda pn: pn[:14])
    clerks_list_df['CityStateZip'] = clerks_list_df['Address'].apply(lambda a: a.split("*NEW*")[3].strip() if len(a.split("*NEW*")) > 3 else "")
    clerks_list_df['Address2'] = clerks_list_df['Address'].apply(lambda a: a.split("*NEW*")[2].split(",")[0].strip())
    clerks_list_df['Address3'] = clerks_list_df['Address'].apply(lambda a: a.split("*NEW*")[2].split(",")[1].strip() if len( a.split("*NEW*")[2].split(",")) > 1 else "")
    clerks_list_df['Address'] = clerks_list_df['Address'].apply(lambda a: a.split("*NEW*")[1].strip())
    clerks_list_df.to_csv('clerks.csv')
