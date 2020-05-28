import re

import requests
import pandas as pd

CIRCUIT_CLERKS_URL = "https://kcoj.kycourts.net/ContactList/Search/Results"
CIRCUIT_CLERKS_BODY = {"SelectedCategory": "CCC", "SelectedCounty": "All"}

ADDRESS_RE = re.compile(r"^.* Circuit Court Clerk")

if __name__ == "__main__":
    res = requests.post(CIRCUIT_CLERKS_URL, data=CIRCUIT_CLERKS_BODY)
    clerks_list_df = pd.read_html(res.text)[0]
    clerks_list_df['Phone Number'] = clerks_list_df['Phone Number'].apply(lambda pn: pn[:14])
    clerks_list_df['Address'] = clerks_list_df['Address'].apply(lambda a: ADDRESS_RE.sub("", a).strip())
    clerks_list_df.to_csv('clerks.csv')
