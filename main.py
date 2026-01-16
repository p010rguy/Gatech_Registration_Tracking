import json
import smtplib
from email.message import EmailMessage
import time
from datetime import datetime
import sys
import select

import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup

course = {
        6239: 35419,
        6270: 34931,
        } #Enter course reference number here
re_add_course_duration = 10 # in seconds
update_rate = 5 # in seconds
cooldown = {}  # courseNumber -> (crn, ready_timestamp)

classSubject = ["CS", "ECE"] #Enter subject here(s)
term = "202602" #Enter term here

sender = "" #Enter your Gmail here
receiver = "" #Enter your Gmail here
password = "" #Enter App password here. Link to get app password: https://www.google.com/url?sa=t&source=web&rct=j&opi=89978449&url=https://myaccount.google.com/apppasswords&ved=2ahUKEwjM1ajegouSAxUWj2oFHVJsN6AQFnoECB8QAQ&usg=AOvVaw1rVibBR6kQTiUjqa0l_f8W
subject = "Registration Check"
body = ""

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_TIMEOUT_SECONDS = 15

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
TIMEOUT_SECONDS = 12
MAX_RETRIES = 4
BACKOFF_SECONDS = 1.5
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
}


def log(message: str) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")


def get_with_retry(session: requests.Session, url: str, *, params: dict | None = None) -> requests.Response:
    attempt = 0
    while True:
        try:
            response = session.get(url, params=params, headers=HEADERS, timeout=TIMEOUT_SECONDS)
            response.raise_for_status()
            return response
        except RequestException as exc:
            attempt += 1
            if attempt >= MAX_RETRIES:
                raise
            wait_seconds = BACKOFF_SECONDS * (2 ** (attempt - 1))
            log(f"request failed ({exc}); retrying in {wait_seconds:.1f}s")
            time.sleep(wait_seconds)


def send_email_with_retry(msg: EmailMessage) -> None:
    attempt = 0
    while True:
        try:
            with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=SMTP_TIMEOUT_SECONDS) as server:
                server.starttls()
                server.login(sender, password)
                server.send_message(msg)
            return
        except smtplib.SMTPException as exc:
            attempt += 1
            if attempt >= MAX_RETRIES:
                raise
            wait_seconds = BACKOFF_SECONDS * (2 ** (attempt - 1))
            log(f"smtp failed ({exc}); retrying in {wait_seconds:.1f}s")
            time.sleep(wait_seconds)


def quit_requested() -> bool:
    if select.select([sys.stdin], [], [], 0.0)[0]:
        return sys.stdin.readline().strip().lower() == "q"
    return False


try:
    stop_requested = False
    while (len(course) or cooldown) and not stop_requested:
        now = time.time()
        for courseNumber, (crn, ready_at) in list(cooldown.items()):
            if now >= ready_at:
                course[courseNumber] = crn
                del cooldown[courseNumber]
                log(f"{crn} re-added after cooldown")

        for courseNumber in list(course.keys()):
            removed_course = False
            for subject in classSubject:
                session = requests.Session()
                get_with_retry(session, f"{BASE}/term/search?mode=search&term={term}")
                params["txt_subject"] = subject
                params["txt_courseNumber"] = courseNumber

                r = get_with_retry(
                    session,
                    f"{BASE}/searchResults/searchResults",
                    params=params,
                ).json()
                
                for sec in r["data"]:
                    if int(sec["courseReferenceNumber"]) == course[courseNumber]:
                        log(f"{course[courseNumber]} : {sec['seatsAvailable']}")
                        if sec["seatsAvailable"]: 
                            body = f"{courseNumber} current open seats: {sec['seatsAvailable']}" # Email message. Can change 

                            msg = EmailMessage()
                            msg['Subject'] = subject
                            msg['From'] = sender
                            msg['To'] = receiver
                            msg.set_content(body)

                            send_email_with_retry(msg)
                            log("email has been sent")
                            cooldown[courseNumber] = (course[courseNumber], time.time() + re_add_course_duration) #The course will be re-added after x seconds of sending the email.
                            del course[courseNumber]
                            removed_course = True
                            break
                if removed_course:
                    break
        if quit_requested():
            log("quit requested by user")
            stop_requested = True
            break
        time.sleep(update_rate) # Update rate. Can change if need be. Unit in Second (currently checking once per minute)
except KeyboardInterrupt:
    log("stopped by user")
