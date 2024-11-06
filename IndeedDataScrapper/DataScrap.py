import requests
from bs4 import BeautifulSoup
import pandas as pd

# Define the base URL for the search query
def get_job_listings(query, location, num_pages=1):
    job_listings = []

    for page in range(0, num_pages * 10, 10):  # Indeed shows 10 results per page
        #url = f"https://www.indeed.com/jobs?q={query}&l={location}&start={page}"
        url = "https://in.indeed.com/jobs?q=data+analyst&l=Gurugram%2C+Haryana"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Find all job listings on the page
        jobs = soup.find_all('div', class_='css-zu9cdh eu4oa1w0')

        for job in jobs:
            title = job.find('h2', class_='title')
            company = job.find('span', class_='company')
            location = job.find('div', class_='location')
            salary = job.find('span', class_='salaryText')
            summary = job.find('div', class_='summary')

            # Clean and extract text
            job_info = {
                'title': title.text.strip() if title else 'N/A',
                'company': company.text.strip() if company else 'N/A',
                'location': location.text.strip() if location else 'N/A',
                'salary': salary.text.strip() if salary else 'N/A',
                'summary': summary.text.strip() if summary else 'N/A',
            }
            job_listings.append(job_info)
    
    return job_listings

# Function to save the data to a CSV file
def save_to_csv(job_listings, filename='indeed_jobs.csv'):
    df = pd.DataFrame(job_listings)
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

if __name__ == '__main__':
    # Define the job search query and location
    search_query = "data+analyst"
    search_location = "Gurugram%2C+Haryana"
    
    # Get job listings from the first 2 pages
    job_data = get_job_listings(search_query, search_location, num_pages=2)
    
    # Save the data to a CSV file
    save_to_csv(job_data)
