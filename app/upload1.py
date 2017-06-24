from flask import Flask, render_template, request
from app import app
from urllib2 import urlopen
from contextlib import closing
import re
import json

@app.route('/upload1', methods=['GET', 'POST'])
def upload1():
   if request.method == 'POST':
		uploadedfile = request.files.get('newfile')
		
		#task 1 list of unique IP addresses as a flat text file
		#to store unique ip
		output = set()
		#search through file to find ip addresses, assume second ip address is client's ip, add it to output if ip is found
		for line in uploadedfile:
			ipsearch = re.search('(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).*?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})',line.rstrip("\n"))
			if ipsearch:
				output.add(ipsearch.group(2))
				
		#write results to flat file
		file = open("task1.txt", "w")
		for ip in output:
			file.write(ip+"\n")
		file.close()
		
   return render_template('about.html')