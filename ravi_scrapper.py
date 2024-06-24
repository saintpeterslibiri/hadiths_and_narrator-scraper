import requests
from bs4 import BeautifulSoup
import csv
import json

# Base URL
base_url = 'https://www.hadisveritabani.info/ravi/ara?sayfa='
ravi_base_url = 'https://www.hadisveritabani.info/ravi/ajxRaviKarti?raviid='

# Writing to CSV file
with open('ravi.csv', mode='w', newline='', encoding='utf-8') as ravi_file:
    writer = csv.writer(ravi_file, quoting=csv.QUOTE_ALL)
    writer.writerow(['ID', 'Data_id', 'Name', 'Birth Year', 'Death Year', 'Places Lived', 'Tribe', 'Degree', 'Reliability', 'Biography'])  # Write header
    
    for page_number in range(1, 11):  # Adjust the range as needed
        url1 = base_url + str(page_number)
        response1 = requests.get(url1)
        web_content1 = response1.content

        soup1 = BeautifulSoup(web_content1, 'html.parser')
        rows = soup1.select('tbody > tr.c-table__row')

        for row in rows:
            # Extracting details
            ravi_id = row.select_one('a.modalRaviKarti')['data-id']
            name = row.select_one('a.modalRaviKarti').get_text(strip=True)
            
            data_id_td = row.select('td.c-table__cell')[1]
            data_id = data_id_td.select_one('span.u-block.u-text-xsmall.u-text-mute').get_text(strip=True)

            birth_year_td = row.select('td.c-table__cell')[4]
            birth_year = birth_year_td.contents[0].strip() if birth_year_td.contents else ''
            death_year = birth_year_td.select_one('span.u-block.u-text-xsmall.u-text-mute').get_text(strip=True)

            places_lived = ', '.join([place.get_text(strip=True) for place in row.select('td.c-table__cell')[5].select('span.u-block')])
            degree = row.select('td.c-table__cell')[3].get_text(strip=True).split('\n')[0]
            reliability = ', '.join(row.select('td.c-table__cell')[3].select_one('span.u-block').get_text(strip=True).split(', '))

            biography = row.find_next('div' , class_='u-p-medium')
            biography = biography.get_text(strip=True)

            # Definening web content 
            url2 = ravi_base_url + ravi_id
            response2 = requests.get(url2)
            ravi_details = json.loads(response2.text)

            # Fetching tribe information
            tribe = ravi_details.get('Kabilesi', '')

            unique_id = f'{page_number}.{ravi_id}'
            # Writing to CSV
            writer.writerow([unique_id, data_id, name, birth_year, death_year, places_lived, tribe, degree, reliability, biography])
        
        print(f'Page {page_number} has been processed')

print('Narrators have been successfully written to the file')
