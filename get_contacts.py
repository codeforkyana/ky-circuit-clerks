import re

import requests
import pandas as pd

NEW_LINE_RE = re.compile(r"<br/?>\n?")
ADDRESS_RE = r"^(?:.+-NEW-)?(.+?)-NEW-(.+?)-NEW-(.+)"

CONTACT_LIST_URL = "https://kcoj.kycourts.net/ContactList/Search/Results"
CONTACT_LIST_CATEGORIES = {
    "clerks": "CCC",
    "district_judges": "DTJ",
    "circuit_judges": "CCJ",
    "supreme_court_judges": "SUP",
    "court_of_appeals_judges": "CAP",
}

if __name__ == "__main__":
    for key, category in CONTACT_LIST_CATEGORIES.items():
        body = {"SelectedCategory": category, "SelectedCounty": "All"}
        res = requests.post(CONTACT_LIST_URL, data=body)
        clerks_list_df = pd.read_html(NEW_LINE_RE.sub("-NEW-", res.text))[0]
        clerks_list_df['Phone Number'] = clerks_list_df['Phone Number'].apply(lambda pn: pn[:14])
        clerks_list_df[['Address1', 'Address2', 'CityStateZip']] = clerks_list_df.Address.str.extract(ADDRESS_RE)
        del clerks_list_df['Address']
        clerks_list_df.to_csv(f'{key}.csv')
