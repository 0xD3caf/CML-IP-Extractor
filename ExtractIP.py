import re
'''This program will take a given input text file and extract all IP addresses from the file. Next it will strip masks and wildcards and format the IP into a ping command.

!!!! The script may remove Ip addreses if they are part of large subnets !!!!

USAGE:

Place the script in the same location as the text(or yaml file) that you want to extact IPs from. 
Change the cml_file variable to the name of the file you want to extract. Run the script using idle or cmd. 
										!!!! Cannot be run by double clicking !!!!

All commands will be found in the same folder in a new file called Ping List.
List will have router name and the commands to ping each IP on that router.


Notes on the Final Ping List:

Due to naming some routers may be missed and will be added to other routers lists.

Due to configuration there may be duplicates of IP addressses listed under the wrong router 
	this is very hard to stop as it pulls these from commands for things like GRE tunnels
	If you super wanted to you could probably parse with regex for interface commands and then
	use those to make sure you only get valid interfaces from that router

--------------------------------------------------------------------------------------------------------------
'''

cml_file = "MSummers Lab6.yaml"

invalid_IP = ["255.255.255.255","255.255.255.254","255.255.255.252","255.255.255.248","255.255.255.240","255.255.255.224","255.255.255.192","255.255.255.128","255.255.255.0",
"255.255.254.0","255.255.252.0","255.255.248.0","255.255.240.0","255.255.224.0","255.255.192.0","255.255.128.0","255.255.0.0","255.254.0.0","255.252.0.0","255.248.0.0","255.240.0.0",
"255.224.0.0","255.192.0.0","255.128.0.0","255.0.0.0","254.0.0.0","252.0.0.0","248.0.0.0","240.0.0.0","224.0.0.0","192.0.0.0","128.0.0.0","0.0.0.0", "0.0.0.0","0.0.0.1","0.0.0.3","0.0.0.7","0.0.0.15","0.0.0.31","0.0.0.63","0.0.0.127","0.0.0.255","0.0.1.255","0.0.3.255","0.0.7.255","0.0.15.255","0.0.31.255","0.0.63.255",
"0.0.127.255","0.0.255.255","0.1.255.255","0.3.255.255","0.7.255.255","0.15.255.255","0.31.255.255","0.63.255.255","0.127.255.255","0.255.255.255","1.255.255.255","3.255.255.255",
"7.255.255.255","15.255.255.255","31.255.255.255","63.255.255.255","127.255.255.255"]

#Variable setup

ip_regex = "\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
router_regex = "hostname SUMMERS-R\d\d?"
text_dict = {}
ip_dict = {}
visited_routers = []
missed_list = []
file = open(cml_file)
text = file.readlines()
								#This section seperates the data into text blobs associated with a Router ID
curr_router = "R1"
for line in text:																	
	if re.search(router_regex, line):												#IF we find a Router config start point
		visited_routers.append(curr_router)											# add the current router to visited list
		prospective_next = re.search(router_regex, line)[0][-3:].strip("- ")		#Get new router ID
		if prospective_next not in visited_routers:									#check if router ID has alread been visited
			curr_router = prospective_next											# IF not visited then make this the new current router
	else:
		blob = str(text_dict.get(curr_router)) + line								#IF not a router ID line, add current line to text blob from dict
		text_dict.update({curr_router: blob})										#update dict with new text blob			

								#Takes the text blobs and parses them for IP addreses maintaining the association between IP and Router ID
for key in text_dict.keys():
	print(key)
	testlst = []
	text_blob = text_dict.get(key)
	ip_list = re.findall(ip_regex, text_blob)							#regex search to find IP addreses and build a list
	for IP in ip_list:														#iterates through all IP and checks if valid or if a subnet mask or subnet address
		if IP not in invalid_IP and IP[-2:] != ".0" and IP[-4:] !=".0.0" and IP[-6:] != "0.0.0":
			print(IP)
			testlst.append(IP)
	ip_dict.update({key: testlst})										#updates dict to contain only valid IP addresses

								#takes all valid IP addrs and writes them to file
out_file = open("Ping List.txt", "w")										
for key in ip_dict.keys():
	final_ips = []															
	final_ips = ip_dict.get(key)											#gets IP list associated with router ID
	final_ips = set(final_ips)												#convert from list to set to remove duplicates
	out_file.write("\n\nRouter: {}".format(key))							#writes Router ID to file
	for IP in final_ips:													#Writes IP associated with router ID to file
		out_file.write("\nping {}".format(IP))

file.close()
out_file.close()
