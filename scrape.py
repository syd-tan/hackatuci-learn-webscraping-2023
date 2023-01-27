from bs4 import BeautifulSoup
import requests
from typing import List
import csv

# Link to the Hack at UCI 2022 Project Gallery 
BASE_URL = 'https://hackuci-2022.devpost.com/project-gallery?page={page_num}'

# The name of each column in our CSV file export (The data we are scraping from each project)
HEADERS = ['Project Name', 'Project Description', 'Likes', 'Comments', 'Thumbnail', 'Is Winner']

def scrape() -> List[List]:
    """
    Scrapes all of the submissions for Hack at UCI 2022 and return the data as a list of lists.
    Each i-th inner list represents the data scraped from the i-th project.
    """
    
    project_gallery_data: List[List] = []    
    
    # There are two pages in the project gallery. Let's scrape each one
    for page_num in [1, 2]:
        
        # Construct the full URL of the page we want to scrape
        url = BASE_URL.format(page_num=page_num)
        
        # Make a GET request to the url to retrieve the page HTML
        page = requests.get(url, headers={'User-Agent': 'HackUCI Scraper'})
        
        # Read the page HTML into BeautifulSoup
        soup = BeautifulSoup(page.text, 'html.parser')
    
        # Loop through all of the project "tiles"
        for project in soup.find_all('div', class_='gallery-item'):
            data = []
            
            # Project Name
            print(project.findChild('h5').text.strip())
            data.append(project.findChild('h5').text.strip())
            
            # Project description
            print(project.findChild('p', class_="small tagline").text.strip())
            data.append(project.findChild('p', class_="small tagline").text.strip())
            
            # Number of likes
            print(project.findChild('span', class_="count like-count").text.strip())
            data.append(project.findChild('span', class_="count like-count").text.strip())
            
            # Number of comments
            print(project.findChild('span', class_="count comment-count").text.strip())
            data.append(project.findChild('span', class_="count comment-count").text.strip())
            
            # Link to thumbnail image           
            print(project.findChild('img', class_="software_thumbnail_image")['src'].strip())
            data.append(project.findChild('img', class_="software_thumbnail_image")['src'].strip())
            
            # Whether the project won a prize
            if project.findChild('img', class_='winner') is not None:
                print("Winner")
                data.append(True)
            else:
                data.append(False)
                
            project_gallery_data.append(data)
            
    print(project_gallery_data)
    return project_gallery_data
    

def write_to_csv(data: List[List], filename: str, headers: List[str] = HEADERS):
    with open(filename, 'w', newline='') as csvfile:
        # Creating a csv writer object 
        csvwriter = csv.writer(csvfile) 
            
        # Writing the fields (columns) 
        csvwriter.writerow(headers) 
            
        # Writing the data (rows) 
        csvwriter.writerows(data)
    
if __name__ == '__main__':
    project_data = scrape()
    write_to_csv(project_data, 'hackuci22_projects.csv')
