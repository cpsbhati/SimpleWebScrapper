from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

# Set up Chrome options
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Run Chrome in headless mode (optional)
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Initialize WebDriverManager and get the path to the ChromeDriver executable
service = Service(ChromeDriverManager().install())

# Initialize the WebDriver with the Service object
driver = webdriver.Chrome(service=service, options=chrome_options)

# URL of the page to scrape
url = "https://in.indeed.com/jobs?q=data+analyst&l=Gurugram%2C+Haryana"

# Open the page
driver.get(url)

# Let the page load completely
time.sleep(10)  # Adjust the sleep time if needed

# Get the page source after loading
html = driver.page_source

# Parse the page source with BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

# Find the <ul> tag
ul_tag = soup.find(class_="mosaic-zone")

# Extract all <li> tags within the <ul>
li_tags = ul_tag.find_all('li')

# Print each <li> tag's details
for li in li_tags:
    job_title_tag = li.find('h2', class_='jobTitle')
    company_tag = li.find('span', class_='company-name')
    location_tag = li.find('div', class_='text-location')
    job_posted_tag = li.find('div', class_='myJobsStateDate')
    
    job_title = job_title_tag.get_text(strip=True) if job_title_tag else 'N/A'
    company = company_tag.get_text(strip=True) if company_tag else 'N/A'
    location = location_tag.get_text(strip=True) if location_tag else 'N/A'
    job_posted = job_posted_tag.get_text(strip=True) if job_posted_tag else 'N/A'
    
    print(f"Job Title: {job_title}")
    print(f"Company: {company}")
    print(f"Location: {location}")
    print(f"Posted: {job_posted}")
    print("-" * 50)

# Close the browser
# driver.quit()
