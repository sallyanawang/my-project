from flask import Flask, render_template, request
from app import app
from urllib2 import urlopen
from contextlib import closing
import re
import json

@app.route('/upload6', methods=['GET', 'POST'])
def upload6():
   if request.method == 'POST':
		uploadedfile = request.files.get('newfile')
		
		#task 6 detect web shells with found entries to flat text file
		#to store found entries
		list = []
		for line in uploadedfile:
			#searching for url in the entry and find potential web shells in it
			webSearch = re.search('(?i)http(.+?) ',line.rstrip("\n"))
			test = False
			if webSearch:
				web = webSearch.group(0)
				#entries with file,cmd.exe,@eval,B374K,c99,system,r57shell,base64_decode,shell,php-backdoor ,aspxspy keywords are considered web shells in this case
				if re.search('.*?((?i)cmd.exe|(?i)@eval|(?i)B374K|(?i)c99|(?i)system|(?i)r57shell|(?i)base64_decode|(?i)shell|(?i)php-backdoor |(?i)aspxspy).*?',web):
					#add entry to the list
					list.append(line.rstrip("\n"))
					test = True
					
			#searching for GET/POST request in the entry and find potential web shells in it
			reqSearch = re.search('((?i)GET |(?i)POST )(.+?) ',line.rstrip("\n"))
			if not test and reqSearch:
				req = reqSearch.group(2)
				#entries with file,cmd.exe,@eval,B374K,c99,system,r57shell,base64_decode,shell,php-backdoor ,aspxspy keywords are considered web shells in this case
				if re.search('.*?((?i)cmd.exe|(?i)@eval|(?i)B374K|(?i)c99|(?i)system|(?i)r57shell|(?i)base64_decode|(?i)shell|(?i)php-backdoor |(?i)aspxspy).*?',req):
					#add entry to the list
					list.append(line.rstrip("\n"))
		
		#write results to flat file
		file = open("task6.txt", "w")
		for webshells in list:
			file.write(webshells)
		file.close()
		
   return render_template('about.html')