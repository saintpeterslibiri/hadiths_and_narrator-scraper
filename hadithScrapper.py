import requests
from bs4 import BeautifulSoup
import csv

# Base URL
base_url = 'https://www.hadisveritabani.info/hadis/ara?kelimeg=ا&aramaTuru=ig&arama=g&sayfa='

# To track unique hadiths
unique_hadiths = set()

# Writing to CSV file
with open('hadis.csv', mode='w', newline='', encoding='utf-8') as hadiths_file:
    writer = csv.writer(hadiths_file, quoting=csv.QUOTE_ALL)
    writer.writerow(['ID', 'Arabic', 'Turkish', 'Books', 'Topics', 'Chain'])  # Write header
    
    for page_number in range(1, 11):  # Adjust the range as needed
        url = base_url + str(page_number)
        # Fetching Webpage content
        response = requests.get(url)
        web_content = response.content

        # Parse content with BeautifulSoup
        soup = BeautifulSoup(web_content, 'html.parser')

        # Taking Arabic content
        hadiths_arabic = soup.find_all('h3', class_='search')
        # Taking Turkish content
        turkish_content = soup.find_all('p', class_='u-mb-small', align='justify')
        # Taking books 
        books_content = soup.find_all('ul', class_='u-mt-zero', align='right')
        # Taking topics 
        topic_content = soup.find_all('div', class_='col-md-6 col-lg-4')
        # Taking chain divs
        chain_divs = soup.find_all('div', class_='c-feed')

        # Debugging: Check the length of both lists
        print(f'Page {page_number} - Arabic Hadiths: {len(hadiths_arabic)}, Turkish Hadiths: {len(turkish_content)}')
        
        for index, hadith in enumerate(hadiths_arabic, start=1):
            # Arabic text
            arabic_text = hadith.get_text(separator=' ', strip=True).replace('\n', ' ').replace('\r', ' ')
            arabic_text = ' '.join(arabic_text.split())  # Remove excessive whitespace
            
            # Turkish text
            if index <= len(turkish_content):
                turkish = turkish_content[index - 1]
                turkish_text = turkish.get_text(separator=' ', strip=True).replace('\n', ' ').replace('\r', ' ')
                turkish_text = ' '.join(turkish_text.split())  # Remove excessive whitespace
            else:
                turkish_text = ""

            # Books text
            books_text = ""
            if index <= len(books_content):
                books = books_content[index - 1].find_all('li')
                books_text = '; '.join(book.get_text(separator='; ', strip=True) for book in books)
            
            # Topics text
            topic_text = ""
            if index <= len(topic_content):
                topics = topic_content[index - 1].find_all('li')
                topic_text = '; '.join(topic.get_text(separator='; ', strip=True) for topic in topics)

            # Chain text
            chain_ids = []
            if index <= len(chain_divs):
                chain_div = chain_divs[index - 1]
                chain_items = chain_div.find_all('div', style='margin-bottom: 5px;')
                for chain_item in chain_items:
                    a_tag = chain_item.find('a', onclick='raviKarti(this)')
                    if a_tag and 'data-id' in a_tag.attrs:
                        chain_ids.append(a_tag['data-id'])
            chain_text = '; '.join(chain_ids)

            # ID creation
            unique_id = f'{page_number}.{index}'  # Create a unique identifier based on page number and order

            # Writing 
            if unique_id not in unique_hadiths:
                writer.writerow([unique_id, arabic_text, turkish_text, books_text, topic_text, chain_text])
                unique_hadiths.add(unique_id)
        
        print(f'Page {page_number} has been processed')

print('Hadiths have been successfully written to the file')
