from BSTree import *

import requests
from bs4 import BeautifulSoup
import bs4 # for types
from urllib.parse import urljoin
import asyncio
import threading
import time
from colored import fg, attr

lock = threading.Lock()

all_letters = "abcdefghijklmnopqrstuvwxyz"

letter_to_num = {}
num_to_letter = []

urls = []
all_found = set()
tasks_scrape = []

words = set()

for index in range(len(all_letters)):
    letter_to_num[all_letters[index]] = index
    num_to_letter.append(all_letters[index])

# Function to tokenize the content
def tokenize(content):
    soup = BeautifulSoup(content, 'html.parser')
    # level 1
    title_words: bs4.element.NavigableString = soup.findAll("h1")[0].contents[0]

    tokens = [[],[]]
    for word in title_words.split():
        word = word.lower()
        should_skip = False

        for letter in word:
            if all_letters.find(letter) < 0:
                should_skip = True
                break
        
        if should_skip:
            continue

        tokens[0].append(word)
        words.add(word)

    # level 2
    desc_words= soup.get_text()

    for word in desc_words.split():
        word = word.lower()
        should_skip = False

        for letter in word:
            if all_letters.find(letter) < 0:
                should_skip = True
                break
            
        if should_skip:
            continue

        tokens[1].append(word.lower())
        words.add(word.lower())
            
    return tokens

    #print(desc_words)
    '''for paragraph in desc_words:
        if not paragraph.text:
            continue
        #print(paragraph)
        #print(paragraph.text)
     '''   
        

#h1
#p -> paragraph

# Function to scrape URLs from a given webpage
async def scrape_urls(base_url, target_url=None, num = None):
    #print(num)
    global urls
    tasks = []
    target_url = target_url or base_url
    num = num or 1

    response = requests.get(target_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    for sub_link_html in soup.findAll('a'):

        sub_link = sub_link_html['href']

        if not base_url + sub_link in urls:
            urls.append(base_url + sub_link)
            print("Should run recursive with depth:", num + 1)
            
            task = asyncio.create_task(scrape_urls(base_url, base_url + sub_link, num + 1))
            #print(task)
            tasks.append(task)

    print(f"Amount all urls: {len(urls)} - Depth:", num)
    return urls


async def scrape_and_tokenize_single(url, search_tree):
        response = requests.get(url)
        #print(url)
        tokens = tokenize(response.content)
        
        #lock.acquire()
        for token in tokens[0]:
            search_tree.insert(token, url, 0)

        for token in tokens[1]:
            search_tree.insert(token, url, 1)
        #lock.release()


async def run_tasks(args: list, fn):
    tasks = []
    print("Urls for tokenizing:", len(args))
    for index in range(len(args)):
        arg = args[index]
        tasks.append(asyncio.create_task(fn(*arg)))

    await asyncio.gather(*tasks)


def scrape_and_tokenize(url, max_scraped, search_tree=None):
    if search_tree is None:
        search_tree = BSTree()

    start_Time = time.time()

    scraped_urls = asyncio.run(scrape_urls(url))
    print("Amount urls:", len(scraped_urls))
    args = []

    print(f"{fg("yellow")}scraped urls after {time.time() - start_Time}{attr('reset')}")


    print("https://books.toscrape.com/catalogue/the-immortal-life-of-henrietta-lacks_753/index.html" in urls)

    for i in range(max_scraped if len(scraped_urls) > max_scraped else len(scraped_urls)):
        current_url = scraped_urls[i]
        
        if current_url == url or current_url == url + "index.html":
            continue
            
        args.append((current_url, search_tree))
    
    print("Started tokenizing")
    asyncio.run(run_tasks(args, scrape_and_tokenize_single))

    print("Amount words:", len(words))

    return search_tree

# Function to query the binary search tree
def query(search_tree):
    print(f"{fg("blue")}(Enter nothing and) Press enter to exit!{attr('reset')}")
    while True:
        look_for = input("What do you want to search for?: ").lower().strip()
        if look_for == "":
            break
        
        startTime = time.time()
        result = search_tree.search(look_for)
        print(f"{fg("yellow")}Results after {time.time() - startTime} seconds{attr('reset')}")
        print(result)

# Function to run the search engine
def run_search_engine():

    startTime = time.time()

    # Scrape data and insert into binary tree
    start_url = "https://books.toscrape.com/"
    max_scraped = 3600

    search_tree = scrape_and_tokenize(start_url, max_scraped)

    print(f"{fg("yellow")}Time to scrape and tokenize: {time.time() - startTime} seconds {attr('reset')}\n")
    

    should_traverse = input("Would you like to traverse? (y/n): ").lower().strip() == "y"

    if should_traverse:
        # Perform in-order traversal (optional for verification)
        startTime = time.time()
        amount = search_tree.inorder_traversal()
        print(f"{fg("yellow")}Time to traverse: {time.time() - startTime} seconds {attr('reset')}")
        print(f"{fg("blue")}Total amount of elements found: {amount}{attr('reset')}\n")
        

    print()    
    
    # Query the binary search tree
    query(search_tree)

    

if __name__ == "__main__":
    run_search_engine()