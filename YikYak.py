#! /usr/bin/env python3
import API as pk
import pygeocoder
import requests

def main():
	# Title text
	print("\nYik Yak Command Line Edition : Created by djtech42\n\n")
	
	# Initialize Google Geocoder API
	geocoder = pygeocoder.Geocoder("AIzaSyAGeW6l17ATMZiNTRExwvfa2iuPA1DvJqM")
	
	try:
		# If location already set in past, read file
		f = open("locationsetting", "r")
		fileinput = f.read()
		f.close()
		
		# Extract location coordinates and name from file
		coords = fileinput.split('\n')
		
		currentlatitude = coords[0]
		currentlongitude = coords[1]
		print("Location is set to: ", coords[2])
		
		# Set up coordinate object
		coordlocation = pk.Location(currentlatitude, currentlongitude)
		
	except FileNotFoundError:
		# If first time using app, ask for preferred location
		coordlocation = newLocation(geocoder)
		
		# If location retrieval fails, ask user for coordinates
		if coordlocation == 0:
			print("Please enter coordinates manually: ")
			
			currentlatitude = input("Latitude: ")
			currentlongitude = input("Longitude: ")
			coordlocation = pk.Location(currentlatitude, currentlongitude)
	
	print()
	
	try:
		# If user already has ID, read file
		f = open("userID", "r")
		userID = f.read()
		f.close()
		
		# start API with saved user ID
		remoteyakker = pk.Yakker(userID, coordlocation, False)
		
	except FileNotFoundError:
		# start API and create new user ID
		remoteyakker = pk.Yakker(None, coordlocation, True)
		
		try:
			# Create file if it does not exist and write user ID
			f = open("userID", 'w+')
			f.write(remoteyakker.id)
			f.close()
			
		except:
			pass
			
	# Print User Info Text
	print("User ID: ", remoteyakker.id, "\n")
	print("Connecting to Yik Yak server...\n")
	print("Yakarma Level:",remoteyakker.get_yakarma(), "\n")
	print("Type one of the one-letter commands below or use the command in conjunction with a parameter.")
	
	currentlist = []
	
	# When actions are completed, user can execute another action or quit the app
	while True:
		# Insert line gap
		print()
		
		# Show all action choices
		choice = input("*Read Latest Yaks\t\t(R)\n*Read Top Local Yaks\t\t(T)\n\n*Read Best Yaks of All Time\t(B)\n\n*Show User Yaks\t\t\t(S)\n*Show User Comments\t\t(O)\n\n*Post Yak\t\t\t(P) or (P <message>)\n*Post Comment\t\t\t(C) or (C <yak#>)\n\n*Upvote Yak\t\t\t(U) or (U <yak#>)\n*Downvote Yak\t\t\t(D) or (D <yak#>)\n\n*Upvote Comment\t\t\t(V) or (V <yak# comment#>)\n*Downvote Comment\t\t(H) or (H <yak# comment#>)\n\n*Yakarma Level\t\t\t(Y)\n\n*Choose New User ID\t\t(I) or (I <userID>)\n*Choose New Location\t\t(L) or (L <location>)\n\n*Quit Yik Yak\t\t\t(Q)\n\n-> ")
		
		# Read Yaks
		if choice == 'R' or choice == 'r':
			currentlist = remoteyakker.get_yaks()
			read(currentlist)
		
		# Read Local Top Yaks
		elif choice == 'T' or choice == 't':
			currentlist = remoteyakker.get_area_tops()
			read(currentlist)
			
		# Read Best of All Time
		elif choice == 'B' or choice == 'b':
			currentlist = remoteyakker.get_greatest()
			read(currentlist)
			
		# Show User Yaks
		elif choice == 'S' or choice == 's':
			currentlist = remoteyakker.get_my_recent_yaks()
			read(currentlist)
			
		# Show User Comments
		elif choice == 'O' or choice == 'o':
			currentlist = remoteyakker.get_recent_replied()
			read(currentlist)
			
		# Post Yak
		elif choice[0] == 'P' or choice[0] == 'p':
			# set message from parameter or input
			if len(choice) > 2:
				message = choice[2:]
			else:
				message = input("Enter message to yak: \n")
				
			# handle and location options
			handle = input("Add handle: (Blank to omit): \n")
			showlocation = input("Show location? (Y/N) ")
			
			if showlocation == 'Y' or showlocation == 'y':
				allowlocation = True
			else:
				allowlocation = False
				
			if handle == '':
				posted = remoteyakker.post_yak(message, showloc=allowlocation)
			else:
				posted = remoteyakker.post_yak(message, showloc=allowlocation, handle=handle)
				
			if posted:
				print("\nYak successful :)")
			else:
				print("\nYak failed :(\t", end='')
				print (posted.status_code, end='')
				print (" ", end='')
				print (requests.status_codes._codes[posted.status_code][0])
				
		# Post Comment
		elif choice[0] == 'C' or choice[0] == 'c':
			# set message from parameter or input
			if len(choice) > 2:
				yakNum = int(choice[2:])
			else:
				yakNum = int(input("Enter yak number (displayed above each one): "))
			
			comment = input("Enter comment:\n")
			
			posted = remoteyakker.post_comment(currentlist[yakNum-1].message_id, comment)
				
			if posted:
				print("\nComment successful :)")
			else:
				print("\nComment failed :(\t", end='')
				print (posted.status_code, end='')
				print (" ", end='')
				print (requests.status_codes._codes[posted.status_code][0])
				
		# Upvote Yak
		elif choice[0] == 'U' or choice[0] == 'u':
			if len(choice) > 2:
				voteYakNum = int(choice[2:])
			else:
				voteYakNum = int(input("Enter yak number to upvote (displayed above each one): "))
				
			if len(currentlist) > 0:
				upvoted = remoteyakker.upvote_yak(currentlist[voteYakNum-1].message_id)
			else:
				yaklist = remoteyakker.get_yaks()
				upvoted = remoteyakker.upvote_yak(currentlist[voteYakNum-1].message_id)
				
			if upvoted:
				print("\nUpvote successful :)")
			else:
				print("\nUpvote failed :(\t", end='')
				print (posted.status_code, end='')
				print (" ", end='')
				print (requests.status_codes._codes[posted.status_code][0])
				
		# Downvote Yak	
		elif choice[0] == 'D' or choice[0] == 'd':
			if len(choice) > 2:
				voteYakNum = int(choice[2:])
			else:
				voteYakNum = int(input("Enter yak number to downvote (displayed above each one): "))
				
			if len(currentlist) > 0:
				downvoted = remoteyakker.downvote_yak(currentlist[voteYakNum-1].message_id)
			else:
				yaklist = remoteyakker.get_yaks()
				downvoted = remoteyakker.downvote_yak(currentlist[voteYakNum-1].message_id)
				
			if downvoted:
				print("\nDownvote successful :)")
			else:
				print("\nDownvote failed :(\t", end='')
				print (posted.status_code, end='')
				print (" ", end='')
				print (requests.status_codes._codes[posted.status_code][0])
		
		# Upvote Comment
		elif choice[0] == 'V' or choice[0] == 'v':
			parameters = choice.split()
			
			if len(parameters) == 3:
				yakNum = int(parameters[1])
				voteCommentNum = int(parameters[2])
			elif len(parameters) == 2:
				yakNum = int(parameters[1])
				voteCommentNum = int(input("Enter comment number to upvote (displayed above each one): "))
			else:
				yakNum = int(input("Enter yak number (displayed above each one): "))
				voteCommentNum = int(input("Enter comment number to upvote (displayed above each one): "))
				
			if len(currentlist) > 0:
				upvoted = remoteyakker.upvote_comment(currentlist[yakNum-1].get_comments()[voteCommentNum-1].comment_id)
			else:
				yaklist = remoteyakker.get_yaks()
				upvoted = remoteyakker.upvote_comment(currentlist[yakNum-1].get_comments()[voteCommentNum-1].comment_id)
				
			if upvoted:
				print("\nUpvote successful :)")
			else:
				print("\nUpvote failed :(\t", end='')
				print (posted.status_code, end='')
				print (" ", end='')
				print (requests.status_codes._codes[posted.status_code][0])
				
		# Downvote Comment	
		elif choice[0] == 'H' or choice[0] == 'h':
			parameters = choice.split()
			
			if len(parameters) == 3:
				yakNum = int(parameters[1])
				voteCommentNum = int(parameters[2])
			elif len(parameters) == 2:
				yakNum = int(parameters[1])
				voteCommentNum = int(input("Enter comment number to downvote (displayed above each one): "))
			else:
				yakNum = int(input("Enter yak number (displayed above each one): "))
				voteCommentNum = int(input("Enter comment number to downvote (displayed above each one): "))
				
			if len(currentlist) > 0:
				downvoted = remoteyakker.downvote_comment(currentlist[yakNum-1].get_comments()[voteCommentNum-1].comment_id)
			else:
				yaklist = remoteyakker.get_yaks()
				downvoted = remoteyakker.downvote_comment(currentlist[yakNum-1].get_comments()[voteCommentNum-1].comment_id)
				
			if downvoted:
				print("\nDownvote successful :)")
			else:
				print("\nDownvote failed :(\t", end='')
				print (posted.status_code, end='')
				print (" ", end='')
				print (requests.status_codes._codes[posted.status_code][0])
				
		# Yakarma Level
		elif choice == 'Y' or choice == 'y':
			print ("\nYakarma Level:",remoteyakker.get_yakarma())
			
		# Change User ID
		elif choice[0] == 'I' or choice[0] == 'i':
			if len(choice) > 2:
				remoteyakker = setUserID(remoteyakker.location, choice[2:])
			else:
				remoteyakker = setUserID(remoteyakker.location)
			
			# Print User Info Text
			print("\nUser ID: ", remoteyakker.id, "\n")
			print("Connecting to Yik Yak server...\n")
			print ("Yakarma Level:",remoteyakker.get_yakarma(), "\n")
				
		# Change Location
		elif choice[0] == 'L' or choice[0] == 'l':
			# set location from parameter or input
			if len(choice) > 2:
				coordlocation = changeLocation(geocoder, choice[2:])
			else:
				coordlocation = changeLocation(geocoder)
				
			remoteyakker.update_location(coordlocation)
			
			yaklist = remoteyakker.get_yaks()
			currentlist = yaklist
			
		# Quit App
		elif choice == 'Q' or choice == 'q':
			break;
			
def newLocation(geocoder, address=""):
	# figure out location latitude and longitude based on address
	if len(address) == 0:
		address = input("Enter college name or address: ")
	try:
		currentlocation = geocoder.geocode(address)
	except:
		print("\nGoogle Geocoding API is offline or has reached the limit of queries.\n")
		return 0
		
	coordlocation = 0
	try:
		coordlocation = pk.Location(currentlocation.latitude, currentlocation.longitude)
		
		# Create file if it does not exist and write
		f = open("locationsetting", 'w+')
		coordoutput = str(currentlocation.latitude) + '\n' + str(currentlocation.longitude)
		f.write(coordoutput)
		f.write("\n")
		f.write(address)
		f.close()
	except:
		print("Unable to get location.")
		
	return coordlocation
	
def setUserID(location, userID=""):
	if userID == "":
		userID = input("Enter userID or leave blank to generate random ID: ")
		
	if userID == "":
		# Create new userID
		remoteyakker = pk.Yakker(None, location, True)
	else:
		# Use existing userID
		remoteyakker = pk.Yakker(userID, location, False)
	try:
		# Create file if it does not exist and write user ID
		f = open("userID", 'w+')
		f.write(remoteyakker.id)
		f.close()
		
	except:
		pass
	
	return remoteyakker
	
def changeLocation(geocoder, address=""):
	coordlocation = newLocation(geocoder, address)
	
	# If location retrieval fails, ask user for coordinates
	if coordlocation == 0:
		print("\nPlease enter coordinates manually: ")
		currentlatitude = input("Latitude: ")
		currentlongitude = input("Longitude: ")
		coordlocation = pk.Location(currentlatitude, currentlongitude)
		
	return coordlocation
	
def read(yaklist):
	yakNum = 1
	for yak in yaklist:
		# line between yaks
		print ("_" * 93)
		# show yak
		print (yakNum)
		yak.print_yak()
		
		commentNum = 1
		# comments header
		comments = yak.get_comments()
		print ("\n\t\tComments:", end='')
		# number of comments
		print (len(comments))
		
		# print all comments separated by dashes
		for comment in comments:
			print ("\t   {0:>4}".format(commentNum), end=' ')
			print ("-" * 77)
			comment.print_comment()
			commentNum += 1
			
		yakNum += 1
		
main()