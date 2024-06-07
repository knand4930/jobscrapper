# import requests
# from bs4 import BeautifulSoup
# from selenium import webdriver
# from selenium.common import NoSuchElementException
# from selenium.webdriver import Keys
# from selenium.webdriver.support.select import Select
# from webdriver_manager.chrome import ChromeDriverManager
# from multiprocessing import Process
# from selenium.webdriver.common.by import By
# import time
# from selenium.webdriver.chrome.service import Service as ChromeService
# import csv
# from datetime import datetime
#
# base_url = "https://dell.wd1.myworkdayjobs.com/en-US/External"
# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--start-maximized')
# driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
# driver.get(base_url)
# time.sleep(5)
#
#
# def scrape_page(html_content, writer):
#     soup = BeautifulSoup(html_content, 'html.parser')
#
#     job_listings = soup.find_all(class_='css-1q2dra3')
#
#     for listing in job_listings:
#         try:
#             job_title = listing.find('a', class_='css-19uc56f').text.strip()
#             job_link = listing.find('a', class_='css-19uc56f')['href']
#             posted_on = listing.find('dd', class_='css-129m7dg').text.strip()
#             req_id = listing.find('li', class_='css-h2nt8k').text.strip()
#             location = job_link.split('/')[4].replace('-', ' ')
#             complete_job_link = base_url + job_link
#
#             # Write data to CSV
#             writer.writerow({'Job Title': job_title,
#                              'Job Link': complete_job_link,
#                              'Posted On': posted_on,
#                              'Req Id': req_id,
#                              'Location': location})
#
#             print("Job Title:", job_title)
#             print("Job Link:", complete_job_link)
#             print("Posted On:", posted_on)
#             print("Req Id:", req_id)
#             print("Location:", location)
#             print()
#         except AttributeError:
#             # Skip this listing if any attribute is None
#             continue
#
#
# # Open CSV file in append mode
# with open('output.csv', 'a', newline='', encoding='utf-8') as csvfile:
#     fieldnames = ['Job Title', 'Job Link', 'Posted On', 'Req Id', 'Location']
#     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#     # If the file is empty, write the header
#     if csvfile.tell() == 0:
#         writer.writeheader()
#
#     while True:
#         # Get the current page source
#         html_content = driver.page_source
#         scrape_page(html_content, writer)
#
#         # Check if there is a next page button
#         next_button = driver.find_elements(By.CLASS_NAME, "css-74r224")[-1]  # Get the last page button
#         next_text = next_button.text
#         if next_text == 'Next':
#             break
#
#         # Click the next page button and wait for page to load
#         next_button.click()
#         time.sleep(5)  # Adjust the duration as needed
#
# driver.quit()

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver import Keys
from selenium.webdriver.support.select import Select
from webdriver_manager.chrome import ChromeDriverManager
from multiprocessing import Process
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.service import Service as ChromeService
import csv
from datetime import datetime

base_url = "https://dell.wd1.myworkdayjobs.com/en-US/External"
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--start-maximized')
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
driver.get(base_url)
time.sleep(5)

def scrape_page(html_content, writer):
    soup = BeautifulSoup(html_content, 'html.parser')
    job_listings = soup.find_all(class_='css-1q2dra3')

    for listing in job_listings:
        try:
            job_title = listing.find('a', class_='css-19uc56f').text.strip()
            job_link = listing.find('a', class_='css-19uc56f')['href']
            posted_on = listing.find('dd', class_='css-129m7dg').text.strip()
            req_id = listing.find('li', class_='css-h2nt8k').text.strip()
            location = job_link.split('/')[4].replace('-', ' ')
            complete_job_link = base_url + job_link

            # Write data to CSV
            writer.writerow({'Job Title': job_title,
                             'Job Link': complete_job_link,
                             'Posted On': posted_on,
                             'Req Id': req_id,
                             'Location': location})

            print("Job Title:", job_title)
            print("Job Link:", complete_job_link)
            print("Posted On:", posted_on)
            print("Req Id:", req_id)
            print("Location:", location)
            print()
        except AttributeError:
            # Skip this listing if any attribute is None
            continue

# Open CSV file in append mode
with open('output.csv', 'a', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Job Title', 'Job Link', 'Posted On', 'Req Id', 'Location']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    # If the file is empty, write the header
    if csvfile.tell() == 0:
        writer.writeheader()

    while True:
        # Get the current page source
        html_content = driver.page_source
        scrape_page(html_content, writer)

        # Flush the buffer to write data to disk immediately
        csvfile.flush()

        # Check if there is a next page button
        next_buttons = driver.find_elements(By.CLASS_NAME, "css-74r224")  # Get all page buttons
        next_button = next_buttons[-1]  # Get the last page button
        if "aria-disabled" in next_button.get_attribute("class"):
            break

        # Click the next page button and wait for page to load
        next_button.click()
        time.sleep(5)  # Adjust the duration as needed

driver.quit()
