import requests
from bs4 import BeautifulSoup as bs
import time
import random

# check if the site has robot.txt that we should adhere to
# url = f'https://www.luxstay.com/robot.txt'
# resp = requests.get(url)
# soup = bs(resp.content, 'html.parser')
#print(soup.prettify())
# time.sleep(0.1)

# get total number of pages
# luxstay support a maximum of 50 items per page
url = f'https://www.luxstay.com/api/search?page=1&limit=50'
resp = requests.get(url)
total_page = resp.json().get('meta').get('pagination').get('total_pages')
#print(total_page)
# time.sleep(0.1)

# for each page, get all apartment ids
apartment_ids = set()
for page in range(1, total_page+1, 1):
    print(f'Page: {page}/{total_page}')

    url = f'https://www.luxstay.com/api/search?page={page}&limit=50'
    resp = requests.get(url)

    # check if there's any 4xx client or 5xx server error
    if resp.raise_for_status() is None:
        apartments = resp.json().get('data')
        # save all ids from JSON response to a set
        apartment_ids.update(set(apartment.get('id') for apartment in apartments))

    time.sleep(random.uniform(0.1, 1))

print(f'Total ids: {len(apartment_ids)}')

with open('apartment_ids.txt', 'w') as output:
    output.write('\n'.join((str(val) for val in apartment_ids)))

print('All ids saved.')