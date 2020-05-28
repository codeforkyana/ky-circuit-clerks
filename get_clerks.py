import requests
import pandas as pd

CIRCUIT_CLERKS_URL = "https://kcoj.kycourts.net/ContactList/Search/Results"
CIRCUIT_CLERKS_BODY = {"SelectedCategory": "CCC", "SelectedCounty": "All"}

if __name__ == "__main__":
    res = requests.post(CIRCUIT_CLERKS_URL, data=CIRCUIT_CLERKS_BODY)
    clerks_list = pd.read_html(res.text)
    clerks_list[0].to_csv('clerks.csv')
