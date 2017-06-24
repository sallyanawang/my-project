from flask import Flask, render_template, request
from app import app
from urllib2 import urlopen
from contextlib import closing
import re
import json

@app.route('/upload4', methods=['GET', 'POST'])
def upload4():
   if request.method == 'POST':
		uploadedfile = request.files.get('newfile')
		
		#task 4 detect SQLi with found entries to flat text file
		#to store found entries
		list = []
		#entries with or = , or like, delete, select, update, create, drop and insert keywords in the request or url are considered SQLi in this case
		regexes = [
				".*?( (?i)or ).*?(=|(?i)LIKE).*?",
				".*?(;).*?((?i)DELETE|(?i)SELECT|(?i)UPDATE|(?i)CREATE|(?i)DROP|(?i)INSERT).*?",
				]
		combined = "(" + ")|(".join(regexes) + ")"
		
		#search through the file to find entries which matches the regex above
		for line in uploadedfile:
			test = False
			#searching for url in the entry and find potential SQLi in it
			httpSearch = re.search('(?i)http(.*)',line.rstrip("\n"))
			if httpSearch:
				web = httpSearch.group(0)
				if re.match(combined, web):
					#add entry to the list
					list.append(line.rstrip("\n"))
					test = True
			
			#searching for GET/POST request in the entry and find potential SQLi in it
			requestSearch = re.search('((?i)GET |(?i)POST )(.+?) ',line.rstrip("\n"))
			if not test and requestSearch:
				req = requestSearch.group(2)
				if re.match(combined, req):
					#add entry to the list
					list.append(line.rstrip("\n"))
				
		#write results to flat file
		file = open("task4.txt", "w")
		for sqli in list:
			file.write(sqli)
		file.close()
		
   return render_template('about.html')