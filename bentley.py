import requests
from bs4 import BeautifulSoup
import csv

# CSV file to save the data
csv_file = 'bentley.csv'

# Define the column headers
fieldnames = ['JobTitle', 'JobLocation', 'JobLink', 'JobDate']

# Open the CSV file in write mode
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()

    var = [0, 25, 50, 75, 100, 125, 150, 200]
    for i in var:
        # URL to scrape
        url = f"https://jobs.bentley.com/search/?q=&sortColumn=referencedate&sortDirection=desc&searchby=location&d=10&startrow={i}"

        # Send a GET request to the URL
        response = requests.get(url)

        # Parse the HTML content of the page with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all rows containing job information
        job_rows = soup.find_all('tr', class_='data-row')

        # Loop through each job row and extract the required information
        for job_row in job_rows:
            # Extract job title
            job_title_tag = job_row.find('a', class_='jobTitle-link')
            job_title = job_title_tag.text.strip()

            # Extract job location
            job_location_tag = job_row.find('span', class_='jobLocation')
            job_location = job_location_tag.text.strip()

            # Extract job link
            job_link = job_title_tag['href']

            # Extract job date
            job_date_tag = job_row.find('span', class_='jobDate')
            job_date = job_date_tag.text.strip()

            # Create a dictionary for the row data
            row_data = {
                'JobTitle': job_title,
                'JobLocation': job_location,
                'JobLink': f"https://jobs.bentley.com{job_link}",
                'JobDate': job_date
            }

            # Write the row data to the CSV file
            writer.writerow(row_data)

print(f"Data has been saved to {csv_file}")
