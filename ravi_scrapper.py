import requests
from bs4 import BeautifulSoup
import csv

# Base URL
base_url = 'https://www.hadisveritabani.info/ravi/ara?sayfa='

# Writing to CSV file
with open('ravi.csv', mode='w', newline='', encoding='utf-8') as ravi_file:
    writer = csv.writer(ravi_file, quoting=csv.QUOTE_ALL)
    writer.writerow(['ID', 'Name', 'Birth Year', 'Death Year', 'Places Lived', 'Degree', 'Reliability'])  # Write header
    
    for page_number in range(1, 5):  # Adjust the range as needed
        url = base_url + str(page_number)
        response = requests.get(url)
        web_content = response.content

        soup = BeautifulSoup(web_content, 'html.parser')

        rows = soup.select('tbody > tr.c-table__row')
        
        for row in rows:
            # Extracting details
            ravi_id = row.select_one('a.modalRaviKarti')['data-id']
            name = row.select_one('a.modalRaviKarti').get_text(strip=True)
            
            birth_year_td = row.select('td.c-table__cell')[4]
            birth_year = birth_year_td.contents[0].strip() if birth_year_td.contents else ''
            death_year = birth_year_td.select_one('span.u-block.u-text-xsmall.u-text-mute').get_text(strip=True)

            places_lived = ', '.join([place.get_text(strip=True) for place in row.select('td.c-table__cell')[5].select('span.u-block')])
            degree = row.select('td.c-table__cell')[3].get_text(strip=True).split('\n')[0]
            reliability = ', '.join(row.select('td.c-table__cell')[3].select_one('span.u-block').get_text(strip=True).split(', '))

            # Writing to CSV
            writer.writerow([ravi_id, name, birth_year, death_year, places_lived, degree, reliability])
        
        print(f'Page {page_number} has been processed')

print('Narrators have been successfully written to the file')
