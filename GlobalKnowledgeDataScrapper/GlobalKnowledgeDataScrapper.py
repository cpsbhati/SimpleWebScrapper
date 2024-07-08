from bs4 import BeautifulSoup
import requests
import re
from docx import Document

def scrap_data_from_web(file_name, url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses

        # Parse the content with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Collect course details
        course_name = soup.find('h1').text.strip()
        course_desc = soup.find(class_="editor").find('p').text.strip()
        course_what_you_will_learn = soup.findAll(class_ = "course-overview__content")


        # Find the <script> tag(s)
        script_tags = soup.find_all('script')

        # Define a regular expression to match date ranges
        date_pattern = re.compile(
            r'Virtual Classroom Live \| [A-Za-z]{3} \d{2} - (?:[A-Za-z]{3} )?\d{2}, \d{4} \| \d{1,2}:\d{2} [APM]{2} - \d{1,2}:\d{2} [APM]{2} [A-Z]{3} \| ONLINE'
        )

        # Initialize an empty list to collect all event dates
        all_events = []

        # Extract events from each <script> tag
        for script in script_tags:
            script_content = script.string
            if script_content:
                events = date_pattern.findall(script_content)
                if events:
                    all_events.extend(events)

        # Create a Word document
        doc = Document()

        # Add course name as title
        title = doc.add_heading(course_name, level=0)

        # Add course description
        doc.add_heading("Course description", level=1)
        doc.add_paragraph(course_desc + '\n')
        for element in course_what_you_will_learn:
            doc.add_paragraph(element.text)

        doc.add_heading("Course dates", level=1)
        # Add dates as bullet points
        for date in all_events:
            p = doc.add_paragraph()
            p.style = 'List Bullet'
            run = p.add_run(date.replace("Virtual Classroom Live | ", "").replace(" | ONLINE", ""))

        # Save the Word file
        doc.save(course_name+' '+file_name)

        print(f"Data scraped from {url} and saved to {file_name}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
    except AttributeError as e:
        print(f"Error parsing HTML content: {e}")

if __name__ == "__main__":
    url_string = input("Enter the Global Knowledge course page URL: ")
    scrap_data_from_web("course_details.docx", url_string)
    input("Press any key to exit...")
