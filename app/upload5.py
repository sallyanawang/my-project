from flask import Flask, render_template, request
from app import app
from urllib2 import urlopen
from contextlib import closing
import re
import json

@app.route('/upload5', methods=['GET', 'POST'])
def upload5():
   if request.method == 'POST':
		uploadedfile = request.files.get('newfile')
		
		#task 5 detect remote file inclusion with found entries to flat text file
		#to store found entries
		list = []
		#entries with ip address, include (), trailing question mark(s), url and file keywords are considered RFI in this case
		regexes = [
				".*?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).*?",
				".*?((?i)include).*?(\().*?(\))",
				".*?(\?+$)",
				".*?((?i)http|(?i)www).*?",
				".*?((?i)file).*?(=).*?",
				]
		combined = "(" + ")|(".join(regexes) + ")"
		
		for line in uploadedfile:
			#searching for GET/POST request in the entry and find potential RFI in it
			reqSearch =  re.search('((?i)GET |(?i)POST )(.+?) ',line.rstrip("\n"))
			if reqSearch:
				req = reqSearch.group(2).rstrip()
				if re.match(combined, req):
					#add entry to the list
					list.append(line.rstrip("\n"))
		
		#write results to flat file		
		file = open("task5.txt", "w")
		for rfi in list:
			file.write(rfi+"\n")
		file.close()
		
   return render_template('about.html')