import requests
from bs4 import BeautifulSoup
import csv

def fetch_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return None

def parse_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    data = []
    # Modify the following lines to extract the specific data you need.
    divs = soup.find_all('div', class_='tabstable')

    # Filter divs to exclude those with 'tabsearch' class
    table = None
    for div in divs:
        if 'tabsearch' not in div['class']:
            table = div
            break
    if table:
        index = 0
        rows = table.find_all('tr')
        for row in rows:
            if index == 0:
                index += 1
                continue  # Skip the first <tr> element
            
            row_data = []
            cells = row.find_all('td')
            # Only process rows with the expected number of cells (e.g., avoid headers or empty rows)
            if cells:  
                for cell in cells:
                    row_data.append(cell.text.strip())
                data.append(row_data)
                print(row_data)  # Debugging: Print the row data
    return data

def scrape_multiple_pages(base_url, start_page, end_page):
    all_data = []
    for page in range(start_page, end_page + 1):
        url = f"{base_url}?page={page}"
        html = fetch_page(url)
        if html:
            page_data = parse_page(html)
            all_data.extend(page_data)
        else:
            print(f"Failed to retrieve page {page}")
    return all_data

base_url = 'https://www.indianspices.com/marketing/price/domestic/daily-price-small.html'
start_page = 1
end_page = 447

all_scraped_data = scrape_multiple_pages(base_url, start_page, end_page)
# for data in all_scraped_data:
#     print(data)

# Function to write data to CSV file
def write_to_csv(data, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerows(data)

# Usage:
filename = 'scraped_data.csv'
write_to_csv(all_scraped_data, filename)
print(f"Data has been written to '{filename}'")