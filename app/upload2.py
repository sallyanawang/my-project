from flask import Flask, render_template, request
from app import app
from urllib2 import urlopen
from contextlib import closing
import re
import json

@app.route('/upload2', methods=['GET', 'POST'])
def upload2():
   if request.method == 'POST':
		uploadedfile = request.files.get('newfile')
		
		#task 2 list of unique IP addresses with country and number of hits as a flat text file
		#to store unique ip and number of hit
		output2 = {}
		#search through file to find ip addresses, assume second ip address is client's ip, add it to output if ip is found, and add the number of hit as dictionary value
		for line in uploadedfile:
			ipsearch = re.search('(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).*?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})',line.rstrip("\n"))
			if ipsearch:
				output2ip = ipsearch.group(2)
				#add 1 to hit is exists
				if output2ip in output2:
					output2[output2ip] = output2[output2ip] + 1
				#assign 1 as value if not exists
				else:
					output2[output2ip] = 1

		#write results to flat file
		file = open("task2.txt", "w")
		for output2ip in output2:
			#to find the ip's country
			url = 'http://freegeoip.net/json/'+output2ip
			try:
				with closing(urlopen(url)) as response:
					location = json.loads(response.read())
					country = location['country_name']
					if not country:
						country = "Location could not be determined"
			except:
					country = "Location could not be determined"
			file.write(output2ip+"\t"+country+"\t"+str(output2[output2ip])+"\n")
		file.close()
		
   return render_template('about.html')