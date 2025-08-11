import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_tax_records(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to access {url}")
        return None
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the table by id or class - update this based on real page structure
    table = soup.find('table', {'id': 'tax-records-table'})
    if not table:
        print("Table not found on the page")
        return None

    rows = table.find_all('tr')
    data = []
    for row in rows[1:]:  # skip header
        cols = row.find_all('td')
        cols_text = [ele.text.strip() for ele in cols]
        data.append(cols_text)

    df = pd.DataFrame(data, columns=['Parcel Number', 'Owner', 'Address', 'Assessed Value', 'Tax Amount'])
    return df

if __name__ == "__main__":
    url = "https://example-county.gov/property-tax-records"  # Replace with actual URL
    df_tax = scrape_tax_records(url)
    if df_tax is not None:
        df_tax.to_csv('scraped_tax_records.csv', index=False)
        print("Scraping completed and saved to scraped_tax_records.csv")
