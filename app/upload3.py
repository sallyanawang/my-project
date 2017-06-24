from flask import Flask, render_template, request
from app import app
from urllib2 import urlopen
from contextlib import closing
import re
import json

@app.route('/upload3', methods=['GET', 'POST'])
def upload3():
   if request.method == 'POST':
		uploadedfile = request.files.get('newfile')
		
		#task 3 list of all activity per IP address to individual flat text files per IP
		#to store ip address and the corresponding activity
		output3 = {}
		#search through file to find ip addresses, assume second ip address is client's ip, add it to output if ip is found, and add the activity as dictionary value
		for line in uploadedfile:
			ipsearch = re.search('(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).*?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})',line.rstrip("\n"))
			if ipsearch:
				output3ip = ipsearch.group(2)
				#if ip exists, append the new activity to the activity list
				if output3ip in output3:
					output3[output3ip].append(line.rstrip("\n"))
				#if ip does not exists, assign a new array to the ip and append the new activity to the activity list
				else:
					output3[output3ip] = []
					output3[output3ip].append(line.rstrip("\n"))
		
		#write results to individual flat file per ip
		for output3ip in output3:
			file = open("ip\\"+output3ip+".txt", "w")
			for activity in output3[output3ip]:
				file.write(activity)
			file.close()
		
   return render_template('about.html')