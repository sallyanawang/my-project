from flask import Flask, render_template, request
from app import app
from urllib2 import urlopen
from contextlib import closing
import re
import json

@app.route('/upload', methods=['GET', 'POST'])
def upload():
   if request.method == 'POST':
		uploadedfile = request.files.get('newfile')
		
		
		#to store unique ip
		output = set()
		
		#to store unique ip and number of hit
		output2 = {}
		
		#to store ip address and the corresponding activity
		output3 = {}
		
		#to store found sqli entries
		list = []
		#entries with or = , or like, delete, select, update, create, drop and insert keywords in the request or url are considered SQLi in this case
		regexes = [
				".*?( (?i)or ).*?(=|(?i)LIKE).*?",
				".*?(;).*?((?i)DELETE|(?i)SELECT|(?i)UPDATE|(?i)CREATE|(?i)DROP|(?i)INSERT).*?",
				]
		combined = "(" + ")|(".join(regexes) + ")"
		
		#to store found rfi entries
		list5 = []
		#entries with ip address, include (), trailing question mark(s), url and file keywords are considered RFI in this case
		regexes5 = [
				".*?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).*?",
				".*?((?i)include).*?(\().*?(\))",
				".*?(\?+$)",
				".*?((?i)http|(?i)www).*?",
				".*?((?i)file).*?(=).*?",
				]
		combined5 = "(" + ")|(".join(regexes5) + ")"
		
		#to store found web shells entries
		list6 = []
		
		#search through file to find ip addresses, assume second ip address is client's ip, add it to output if ip is found
		for line in uploadedfile:
			ipsearch = re.search('(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).*?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})',line.rstrip("\n"))
			if ipsearch:
				outputip = ipsearch.group(2)
				
				#for task 1
				output.add(outputip)
				
				#for task 2
				#add 1 to hit if exists
				if outputip in output2:
					output2[outputip] = output2[outputip] + 1
				#assign 1 as value if not exists
				else:
					output2[outputip] = 1
					
				#for task 3
				#if ip exists, append the new activity to the activity list
				if outputip in output3:
					output3[outputip].append(line.rstrip("\n"))
				#if ip does not exists, assign a new array to the ip and append the new activity to the activity list
				else:
					output3[outputip] = []
					output3[outputip].append(line.rstrip("\n"))
					
			#for task 4
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
			#for task 5
			if requestSearch:
				req = requestSearch.group(2).rstrip()
				if re.match(combined5, req):
					#add entry to the list
					list5.append(line.rstrip("\n"))
				
			#for task 6
			webSearch = re.search('(?i)http(.+?) ',line.rstrip("\n"))
			test6 = False
			if webSearch:
				web = webSearch.group(0)
				#entries with file,cmd.exe,@eval,B374K,c99,system,r57shell,base64_decode,shell,php-backdoor ,aspxspy keywords are considered web shells in this case
				if re.search('.*?((?i)cmd.exe|(?i)@eval|(?i)B374K|(?i)c99|(?i)system|(?i)r57shell|(?i)base64_decode|(?i)shell|(?i)php-backdoor |(?i)aspxspy).*?',web):
					#add entry to the list
					list6.append(line.rstrip("\n"))
					test6 = True
					
			#searching for GET/POST request in the entry and find potential web shells in it
			reqSearch = re.search('((?i)GET |(?i)POST )(.+?) ',line.rstrip("\n"))
			if not test6 and reqSearch:
				req = reqSearch.group(2)
				#entries with file,cmd.exe,@eval,B374K,c99,system,r57shell,base64_decode,shell,php-backdoor ,aspxspy keywords are considered web shells in this case
				if re.search('.*?((?i)cmd.exe|(?i)@eval|(?i)B374K|(?i)c99|(?i)system|(?i)r57shell|(?i)base64_decode|(?i)shell|(?i)php-backdoor |(?i)aspxspy).*?',req):
					#add entry to the list
					list6.append(line.rstrip("\n"))

		#task 1 list of unique IP addresses as a flat text file
		#write results to flat file
		file = open("task1.txt", "w")
		for ip in output:
			file.write(ip+"\n")
		file.close()
		
		#task 2 list of unique IP addresses with country and number of hits as a flat text file
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
		
		#task 3 list of all activity per IP address to individual flat text files per IP	
		#write results to individual flat file per ip
		for output3ip in output3:
			file = open("ip\\"+output3ip+".txt", "w")
			for activity in output3[output3ip]:
				file.write(activity)
			file.close()
		
		#task 4 detect SQLi with found entries to flat text file		
		#write results to flat file
		file = open("task4.txt", "w")
		for sqli in list:
			file.write(sqli+"\n")
		file.close()
		
		#task 5 detect remote file inclusion with found entries to flat text file

		#write results to flat file		
		file = open("task5.txt", "w")
		for rfi in list5:
			file.write(rfi+"\n")
		file.close()
		
		#task 6 detect web shells with found entries to flat text file
		
		#write results to flat file
		file = open("task6.txt", "w")
		for webshells in list6:
			file.write(webshells)
		file.close()
		
   return render_template('about.html')