import json
import smtplib
from email.message import EmailMessage
import time

import requests
from bs4 import BeautifulSoup

course = {
        1331: 24989,
        1332: 27210,
        4455: 20956, 
       3251: 20207} #Enter course reference number here

classSubject ="CS" #Enter subject here
term = "202602" #Enter term here

sender = "" #Enter your Gmail here
receiver = "" #Enter your Gmail here
password = "" #Enter App password here. Link to get app password: https://www.google.com/url?sa=t&source=web&rct=j&opi=89978449&url=https://myaccount.google.com/apppasswords&ved=2ahUKEwjM1ajegouSAxUWj2oFHVJsN6AQFnoECB8QAQ&usg=AOvVaw1rVibBR6kQTiUjqa0l_f8W
subject = "Registration Check"
body = ""

server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login(sender, password)

params = {
    "txt_subject": classSubject,
    "txt_courseNumber": 0,
    "txt_term": term,
    "pageOffset": 0,
    "pageMaxSize": 10,
    "sortColumn": "subjectDescription",
    "sortDirection": "asc"
}

BASE = "https://registration.banner.gatech.edu/StudentRegistrationSsb/ssb"


while len(course):
    for courseNumber in list(course.keys()):
        session = requests.Session()
        session.get(f"{BASE}/term/search?mode=search&term={term}")
        params["txt_courseNumber"] = courseNumber

        r = session.get(f"{BASE}/searchResults/searchResults", 
                params = params).json()
        
        for sec in r["data"]:
            if int(sec["courseReferenceNumber"]) == course[courseNumber]:
                print(f"{course[courseNumber]} : {sec["seatsAvailable"]}")
                if sec["seatsAvailable"]: 
                    body = f"{courseNumber} current open seats: {sec["seatsAvailable"]}" # Email message. Can change 

                    msg = EmailMessage()
                    msg['Subject'] = subject
                    msg['From'] = sender
                    msg['To'] = receiver
                    msg.set_content(body)

                    server.send_message(msg)
                    print("email has been sent")
                    del course[courseNumber]
                    break
    time.sleep(1) # Update rate. Can change if need be. Unit in Second (currently checking once per minute)


# params["txt_courseNumber"] = 1332

# r = session.post(f"{BASE}/searchResults/searchResults", 
#     params = params).json()
# with open("page1.json", "w") as f:
#     json.dump(r, f)

# session = requests.Session()
# session.get(f"{BASE}/term/search?mode=search&term={term}")

# params["txt_courseNumber"] = 1331

# r = session.post(f"{BASE}/searchResults/searchResults", 
#     params = params).json()
# with open("page2.json", "w") as f:
#     json.dump(r, f)