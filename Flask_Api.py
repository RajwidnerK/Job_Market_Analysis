from flask import Flask
from flask_jsonpify import jsonify
import requests
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim
import simplejson as json
app = Flask(__name__)

@app.route("/")
def hello():
    #Author Rajwinder
    # Collect and parse first page
    page = requests.get('https://ca.indeed.com/software-jobs')
    # https://ca.indeed.com/viewjob?cmp=Adamson-Systems-Engineering&t=Software+Engineer&jk=02e60387021269b5&sjdu=vQIlM60yK_PwYat7ToXhk9I8NiHOQ-7v2o66QU9DKp25gg8ltlYMwsB723eeJewasQRwRpNzkHw5l1vcLi0knw&tk=1dmp4geja4ntl800&adid=306745201&pub=4a1b367933fd867b19b072952f68dceb&vjs=3
    #page = requests.get('https://ca.indeed.com/viewjob?cmp=Adamson-Systems-Engineering&t=Software+Engineer&jk=02e60387021269b5&sjdu=vQIlM60yK_PwYat7ToXhk9I8NiHOQ-7v2o66QU9DKp25gg8ltlYMwsB723eeJewasQRwRpNzkHw5l1vcLi0knw&tk=1dmp4geja4ntl800&adid=306745201&pub=4a1b367933fd867b19b072952f68dceb&vjs=3

    soup = BeautifulSoup(page.text, 'html.parser')

    #Author Rajwinder# Pull all text from the BodyText div
    #artist_name_list = soup.find(class_='summary')
    job_div = soup.find(class_='sjcl')
    job_title_div = soup.find(class_='title')
    job_location_div = soup.find(class_='location accessible-contrast-color-location')

    # Pull text from all instances of <a> tag within BodyText div
    artist_name_list_items = job_div.find_all('span')

    # Pull text from all instances of <a> tag within BodyText div
    job_title = job_title_div.find('a').text

    # Pull text from all instances of <a> tag wiartist_name_listthin BodyText div
    company_name = job_div.find('div').text

    job_location = job_location_div.text

    
    geolocator = Nominatim(user_agent="your Google Key...")
    location = geolocator.geocode(job_location)
    lng = location.longitude
    lat = location.latitude

    # Create for loop to print out all artists' names
    print(job_title)
    print(company_name)
    print(job_location)
    print(lng)
    print(lat)
    print("Success!")
    # Initialize a employee list
    return jsonify({'lng':lng,'lat':lat,'jobs':job_title,'open':'false' })

if __name__ == '__main__':
     app.run(port=5002)