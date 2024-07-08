from bs4 import BeautifulSoup
import requests
import re

def scrape_learning_tree_course(url):
    # Check if the URL is from Learning Tree
    if not re.match(r'https?://(www\.)?learningtree\.com/courses/.+', url):
        print("Please enter a valid Learning Tree course page URL.")
        return

    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse the HTML content
        soup = BeautifulSoup(response.content, "html.parser")

        # Find the elements with specified class names
        course_name = soup.find(class_="page-hero__title")
        course_hero_details = soup.find_all(class_="page-hero-list")
        course_dates = soup.find_all(class_="courses-date__item-title")
        course_details = soup.find_all(class_="course-detail-info__content-outline col-8")

        # Open the text file in write mode
        with open('scraped_data.txt', 'w') as file:
            # Write course name
            if course_name:
                file.write(f"-------- {course_name.text.strip()} ---------\n\n")

            # Write course hero details
            file.write("-------- Course Summary Start ---------\n\n")
            for detail in course_hero_details:
                file.write(detail.text.strip() + '\n')
            file.write("-------- Course Summary End ---------\n\n")

            # Write course dates
            file.write("-------- Course Dates Start ---------\n\n")
            for date in course_dates:
                date_text = date.text.strip().replace('\n', " # ").replace("Guaranteed to Run - you can rest assured that the class will not be cancelled. #  # ", "")
                file.write(date_text + '\n')
            file.write("-------- Course Dates End ---------\n\n\n\n")

            # Write course details
            file.write("-------- Course Details ---------\n\n")
            for detail in course_details:
                file.write(detail.text.strip() + '\n\n')
            file.write("-------- Course Details End ---------\n\n\n\n")

        print("Scraped data written to the scraped_data.txt file")

    except requests.exceptions.RequestException as e:
        print(f"Failed to get the data from {url}: {e}")

# Prompt the user for the URL
course_url = input("Enter a Learning Tree course page URL (e.g., https://www.learningtree.com/courses/cissp-training/): ")
scrape_learning_tree_course(course_url)
