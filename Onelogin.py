import requests
import pprint
import webbrowser
import sys
import json
import datetime 
from datetime import date
from pyfiglet import Figlet



#Standard URL's used in API calls
api_generateURL = "https://api.eu.onelogin.com/auth/oauth2/v2/token"
api_baseURL = "https://api.eu.onelogin.com/api/2/"
user_baseURL = 'https://yourcompany.onelogin.com/users'

#generate fresh API key
r = requests.post(api_generateURL,
  auth=('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX','XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'),
  json={
    "grant_type": "client_credentials"
  }
)

ak = r.json()
af = ak['access_token']


#API headers
headers = {
    'Authorization': "bearer " + ak['access_token'],
    'Content-Type': 'application/json',
}

#Print Onelogin header
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
onelogin_banner = Figlet(font='big')
print(onelogin_banner.renderText('OneLogin'))
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

#Menu choice 
choice = input("What do you wanna do ? [1] | 1: Create a user | 2: Check last login  ")
choice = int(choice)

#User Creation Steps
def user_creation():
	#User creation info
	firstname = str(input("Firstname: "))
	lastname = str(input("Lastname: "))
	username = str(input("Username: "))
	password = str(input("Password: "))
	email = str(input("Email: "))
	password_confirmation = str(password)
	#Example groups 
	olgroups = {
	  "Example Group": "1", 
	  "Example Group 2": "2",
	  "Example Group 3": "3"
	}
	pprint.pprint(olgroups)
	#Make sure to change role id to your role id
	group_id = str(input("User group: "))
	if group_id == "1":
		role_id = "XXXXXXX"
		group_id = "XXXXXXX"
	elif group_id == "2" or "3":
		role_id = "XXXXXXX"

	#converts all the info to right url form
	data = ("{" + "\n" + '"username"' + ":" + '"' + username + '"' + "," + "\n" + '"email"' + ":" + '"' + email + '"' + "," + "\n" + '"firstname"' + ":" + '"' + firstname + '"' + "," + "\n" + '"lastname"' + ":" + '"' + lastname + '"' + "," + "\n" + '"password"' + ":" + '"' + password + '"' + "," + "\n" + '"password_confirmation"' + ":" + '"' + password_confirmation + '"' + "," + "\n" + '"group_id"' + ":" + '"' + group_id + '"' + "," + "\n" + '"role_ids"' + ":" + '"' + role_id + '"' + "\n" + "}")
	print(data)	
	#confirms info and makes API call
	cf = input(str("Is the information correct? y/n "))
	if cf == "y":
		response = requests.post(api_baseURL + "users", headers=headers, data=data)
		# first prints the response then converts to python response
		br = response.json()
		pprint.pprint(br)
		#Prints repsonse and confirms that user is created
		if response is None:
			print("User" + " " + firstname + " " + lastname + " " + "not created")
		elif response != None:
			print("User" + " " + firstname + " " + lastname + " " + "created")
		#creates temporary json file to grab user id value to open web browser
		vr = response.json()
		fileName = firstname + "_" + lastname + ".json"
		strVr = str(vr['id'])

		ob = input(str("Do you want to open the user in a web browser? (y/n) "))
		if ob == "y":
			url = user_baseURL + "/" + strVr + "/edit"
			webbrowser.open_new(url) 	
	
	elif cf == "n":
		user_creation()

#new function that lists user
def list_users():
	uN = str(input("Search for user: "))
	print("Searching for emails with" + " " + uN + " " + "in the name")
	response = requests.get(user_baseURL + "?" + "email=" + uN + "*", headers=headers)
	file = open(uN + ".txt", "a+")
	file.write(response.text)
	file.close()


#calls function on choice
if choice == 1: 
	user_creation()
elif choice == 2:
	list_users()	






