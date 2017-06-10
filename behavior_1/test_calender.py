import os
from oauth2client.client import SignedJwtAssertionCredentials
import json
import requests
import datetime


with open('Google-service.json') as json_file:
    json_data = json.load(json_file)

credential = SignedJwtAssertionCredentials(json_data['client_email'], json_data['private_key'], 'https://www.googleapis.com/auth/calendar')

r2 = requests.post("https://accounts.google.com/o/oauth2/token", data={'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer','assertion': credential._generate_assertion()})
accessToken = r2.json()['access_token']

######################

date = datetime.datetime.today().strftime('%Y-%m-%d')
print("Today is " + date)
CalendarID = "b7td4c1cqsifaj5erj0mc7asgs@group.calendar.google.com"
r = requests.get("https://www.googleapis.com/calendar/v3/calendars/" + CalendarID + "/events?timeMin=" + date + "T00:00:00Z&timeMax=" + date + "T23:59:59Z", headers={'Authorization': 'Bearer ' + accessToken})
print(str(r.json()))

Events = r.json()['items']
AppointmentList = []

if(len(Events) > 0):
    for item in Events:
        People = item['description'].split("|")
        if(len(People) > 1):
            for i in range(1,len(People)):
                Visitor = str(People[i]).strip()
                if ' ' in Visitor:
                    Visitor = Visitor.split(' ')
                    if(len(Visitor) == 2):
                        AppointmentList.append([str(Visitor[0]),str(People[0])])
                        AppointmentList.append([str(Visitor[1]),str(People[0])])
                        AppointmentList.append([str(Visitor[0]) + " " + str(Visitor[1]),str(People[0])])
                    else:
                        print("Cant manage this name format at the moment")
                else:
                   AppointmentList.append([str(People[i]),str(People[0])])
        else:
            print("Meeting with invalid format, no visitors?")

        self.memory.insertData("ERReceptionist/AppointmentList", str(AppointmentList))
        AppointmentConcept = []

        for Visitor in AppointmentList:
           try:
               AppointmentConcept.append(Visitor[0])
           except:
               pass

        self.ALDialog.setConcept( "VisitorNames", "enu", AppointmentConcept )
else:
    print("No Events in the calendar")
