# test BLE Scanning software
# jcs 6/8/2014
THIS WIRKS
import blescan
import sys
import json
import bluetooth._bluetooth as bluez
from lookup_engine import lookup_user
import requests
from firebase import firebase


dev_id = 0
try:
	sock = bluez.hci_open_dev(dev_id)

except:
	print "error accessing bluetooth device..."
    	sys.exit(1)

firebase = firebase.FirebaseApplication('https://ble-prototype.firebaseio.com', None)	
blescan.hci_le_set_scan_parameters(sock)
blescan.hci_enable_le_scan(sock)
# count = 50
# existing_beacon_UUIDs = []
while True:
	current_beacon = ''	
	last_user = {'name': ''}
	returnedList = blescan.parse_events(sock, 10)
	for beacon in returnedList:
		print "Beacon found"
		print beacon	
		print "============="
		beacon_arr = beacon.split(',')
		combined_id = ".".join(beacon_arr[1:4]).upper()
		found_user = lookup_user(combined_id)
		if found_user is not None and not (found_user['name'] == last_user["name"]):
			print "New Beacon"	
			print "==============="	
			last_user = found_user	
			current_beacon = combined_id	
			user = firebase.get('/levelTest', None)	
			if user is not None:
				print user
				print "============"
				print "Incrementing Score"
				print "============"
				jsonResponse = user
				jsonResponse['score'] = jsonResponse['score'] + 1
				requests.put('https://ble-prototype.firebaseio.com/levelTest.json', data=json.dumps(jsonResponse))
