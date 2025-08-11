import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://example-county.gov/property-tax-records'  # Replace with your real URL

response = requests.get(url)
if response.status_code != 200:
    print("Failed to retrieve page")
    exit()

soup = BeautifulSoup(response.text, 'html.parser')
table = soup.find('table', {'id': 'tax-records-table'})  # Replace selector

rows = table.find_all('tr')

data = []
for row in rows[1:]:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    data.append(cols)

df = pd.DataFrame(data, columns=['Parcel Number', 'Owner', 'Address', 'Assessed Value', 'Tax Amount'])
print(df.head())
df.to_csv('scraped_tax_records.csv', index=False)

