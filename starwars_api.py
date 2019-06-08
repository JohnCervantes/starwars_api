import requests
import csv
import os
import smtplib
from email.message import EmailMessage
import imghdr

count = int(requests.get('https://swapi.co/api/people').json()['count']) + 2

with open('star_wars.csv', 'w') as csv_file:
    fieldnames = ['Name', 'Gender', 'Birth_year',
                  'Homeworld', 'Height', 'Mass', 'Films']
    csv_writer = csv.DictWriter(
        csv_file, fieldnames=fieldnames, delimiter='\t')
    csv_writer.writeheader()
    for i in range(1, count):
        r = requests.get('https://swapi.co/api/people/' + str(i))
        swars_json = r.json()
        if r.ok == False:
            csv_writer.writerow({'Name': 'none', 'Gender': 'none', 'Birth_year': 'none',
                                 'Homeworld': 'none', 'Height': 'none', 'Mass': 'none', 'Films': 'none'})
            continue
        csv_writer.writerow({'Name': swars_json['name'], 'Gender': swars_json['gender'], 'Birth_year': swars_json['birth_year'],
                             'Homeworld': swars_json['homeworld'], 'Height': swars_json['height'], 'Mass': swars_json['mass'], 'Films': swars_json['films']})

username = os.environ.get('bs_user')
password = os.environ.get('bs_password')
msg = EmailMessage()
msg['Subject'] = 'Your Star Wars data is set!'
msg['From'] = username
msg['To'] = 'johncervantes@protonmail.com'
msg.set_content(
    'Thanks for using our data scraper service. You can find the data file attached to this email. Have a great day!')

with open('star_wars.csv','rb') as f:
    file_data = f.read()
    # file_type = imghdr.what(f.name)
    file_name = f.name

msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)


with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(username, password)
    smtp.send_message(msg)
