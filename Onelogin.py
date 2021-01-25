import requests
import pprint
import webbrowser
import sys
import json
import os
from cowpy import cow
import random
from datetime import date
from datetime import datetime, timedelta

#Standard URL's used in API calls
api_generateURL = "https://api.eu.onelogin.com/auth/oauth2/v2/token"
api_baseURL = "https://api.eu.onelogin.com/api/2/"
api_UserbaseURL = "https://api.eu.onelogin.com/api/2/users"
user_baseURL = 'https://yourcompany.onelogin.com/users'

#generate fresh API key
r = requests.post(api_generateURL,
  auth=('XXXXXXXXXXXXXXXXXXXXXXXXXXX','XXXXXXXXXXXXXXXXXXXXXXXXXXX'),
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

#declare today to use in header
today = str(date.today())
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print(cow.milk_random_cow("Onelogin CLI " + today))
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

#Main menu 
choice = input("Select your choice [1-3] \n 1: Create a user \n 2: Check last login \n 3: List all Users that hasn't changed password in over 100 days \n 4: Update user \n")
choice = int(choice)


#User Creation Steps
def user_creation():
	firstname = str(input("Firstname: "))
	lastname = str(input("Lastname: "))
	username = str(input("Username: "))
	password = str(input("Password: "))
	email = str(input("Email: "))
	password_confirmation = str(password)
	olgroups = {
	  "Users NL": "1", 
	  "Users US": "2",
	  "Process US": "3"
	}
	pprint.pprint(olgroups)
	group_id = str(input("User group: "))
	if group_id == "391705" or "1":
		role_id = "XXXX"
		group_id = "XXXX"
	elif group_id == "392630" or "2" or "3":
		role_id = "XXXX"

	data = ("{" + "\n" + '"username"' + ":" + '"' + username + '"' + "," + "\n" + '"email"' + ":" + '"' + email + '"' + "," + "\n" + '"firstname"' + ":" + '"' + firstname + '"' + "," + "\n" + '"lastname"' + ":" + '"' + lastname + '"' + "," + "\n" + '"password"' + ":" + '"' + password + '"' + "," + "\n" + '"password_confirmation"' + ":" + '"' + password_confirmation + '"' + "," + "\n" + '"group_id"' + ":" + '"' + group_id + '"' + "," + "\n" + '"role_ids"' + ":" + '"' + role_id + '"' + "\n" + "}")
	print(data)	

	cf = input(str("Is the information correct? y/n "))
	if cf == "y":
		response = requests.post(api_baseURL + "users", headers=headers, data=data)

		# pprint.pprint(br)
		if response is None:
			print("User" + " " + firstname + " " + lastname + " " + "not created")
		elif response != None:
			print("User" + " " + firstname + " " + lastname + " " + "created")
			
		vr = response.json()
		fileName = firstname + "_" + lastname + ".json"
		strVr = str(vr['id'])

		ob = input(str("Do you want to open the user in a web browser? (y/n) "))
		if ob == "y":
			url = user_baseURL + "/" + strVr + "/edit"
			webbrowser.open_new(url)
			exit() 	
	
	elif cf == "n":
		user_creation()

#List users that start with email
def list_users():
	uN = str(input("Search for user: "))
	response = requests.get(api_UserbaseURL + "?" + "email=" + uN + "*", headers=headers).json()
	jr = response
	for items in jr:
		print("Searching last login for: " + items['firstname'] + " " +items['lastname'])
		print("Username:" ,items['email'])
		print("Last login:",items['last_login'])
		print("Last password changed: ", items['password_changed_at'])
	exit()


#change to password not last login	
#List all users that hasn't logged in over 100 days
def list_all():
	response = requests.get(api_UserbaseURL, headers=headers).json()
	jr = response
	for items in jr:
		a = items['password_changed_at']
		b = items['username']
		# print(a)
		if a != None and a < "2020-10-10T15:50:52+0000":
			print(a, b)
	exit()

def update_user():
	u = str(input("Which user do you want to change? (e.g. j.doe or j.d) "))
	response = requests.get(api_UserbaseURL + "?" + "email=" + u + "*", headers=headers)
	if response.status_code == 200:
		ur = response.json()
		for items in ur:
			ch = str(input("Is this the correct user ? " + items['firstname'] + " " + items['lastname'] + " y/n "))
			if ch == "y":
				for items in ur:
					wb = str(input("Do you want to open the user in the browser? "))
					if wb == "y":
						ud = str(items['id'])					
						url = user_baseURL + "/" + ud + "/edit"
						webbrowser.open_new(url)
					else:
						ch = print("What do you want to change?")
						userC = {
						  "Firstname": "1", 
						  "Lastname": "2",
						  "Username / Email (Username == email)": "3",
						  "Company": "4",
						  "Phone Number": "5"
						}
						pprint.pprint(userC)
						change = str(input("What do you want to change? "))
						if change == "1":
							uud = str(items['id'])
							print(uud)
							uid = str(input("Change firstname to: "))
							data = ("{" + "\n" + '"' + "firstname" + '"' + ":" + '"' + uid + '"' + "\n" + "}")
							print(data)
							resp = requests.put(api_UserbaseURL + "/:" + uud, headers=headers, data=data).json()
							print(resp)
			elif ch != "y":
				update_user()

	else:
		exit()

#exit function
def exit():
	r = str(input("Do you want to return to the main menu? y/n "))
	if r == "y":
		os.system('python "C:/path/to/your/script.py"') 
	elif r != "y":
		input("Press Enter to exit....")
		sys.exit(0)		

#main menu choice
if choice == 1: 
	user_creation()
elif choice == 2:
	list_users()	
elif choice == 3:
	list_all()
elif choice == 4:
	update_user()




