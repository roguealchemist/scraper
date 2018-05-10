'''

Automated Security Tool
May 4, 2018

Email Scraper Tool:
Purpose of tool is to scan websites for email addresses that
could be harvested by web crawlers and spiders that could be misused
for spamming and social engineering application.  The tool collects all
the emails and writes them into a file and then emails the results to
devops for review. The script could be automated and ran weekly on a
cron job to ensure email addresses on not posted on a company website.

'''

# /usr/bin/env python

# Libraries used for scraper
from bs4 import BeautifulSoup
import re
from urllib.request import urlopen
import sys
# Libraries user for emailing results
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# Def logfile where scraper will leave captured info
class Logger (object):
    def _init_(self):
        self.terminal = sys.stdout
        self.log = open("logfile.log", "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass


def main():
    # Opens URL to scrape
    f = urlopen('http://www.guideon.org')

    s = BeautifulSoup(f, 'html.parser')
    s = s.get_text()

    emails = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,3}",s)


    # Msg no email addresses found.
    if len(emails) == 0:
        print("Sorry, no email address found.")
        print('------------')
        print()

    # Shows found email addresses
    else:
        count = 1
        for item in emails:
            #print(count, ' email address(es) found : ', item)
            results=str(count) + ' email address(es) found : ' + item + ' \n'
            # Output to file
            f=open("emailScraper_results.txt",'a')
            #print (results)
            f.write(results)
            f.close()
            count = count + 1

    # Define variables
    userEmail = 'cyb216testemail@gmail.com'
    tarEmail = 'devops@hrtroops.org'
    subject = 'Results for EmailScraper'
    server = smtplib.SMTP('smtp.gmail.com',587)

    # Define Email from/to/subject lines
    msg = MIMEMultipart()
    msg['From'] = userEmail
    msg['To'] = tarEmail
    msg['Subject'] = subject

    # Define the body of the Email
    body = 'Attached please find the EmailScraper Results'
    msg.attach(MIMEText(body,'plain'))

    # Define attachment, upload, and encode for transportation through email
    filename = './emailScraper_results.txt' # Use direct path
    attachment = open (filename, 'rb')
    part = MIMEBase('application','octlet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition','attachment; filename= '+filename)
    msg.attach(part)

    # Converts msg variable to a string
    text = msg.as_string()

    # Start connection with SMTP server and send Email
    server.starttls()
    server.login (userEmail, 'cyb216TE') #sender's email, password
    server.sendmail(userEmail, tarEmail, text)
    server.quit()
    print ('email sent to', tarEmail)

if __name__ =="__main__":
    main()

	# End of Code
