# test BLE Scanning software
# jcs 6/8/2014

import blescan
import sys
import json
import bluetooth._bluetooth as bluez
from lookup_engine import lookup_user
import requests


dev_id = 0
try:
	sock = bluez.hci_open_dev(dev_id)

except:
	print "error accessing bluetooth device..."
    	sys.exit(1)

blescan.hci_le_set_scan_parameters(sock)
blescan.hci_enable_le_scan(sock)
# count = 50
# existing_beacon_UUIDs = []

while True:
	last_user = {'name': ''}
	returnedList = blescan.parse_events(sock, 10)
	for beacon in returnedList:
		beacon_arr = beacon.split(',')
		combined_id = ".".join(beacon_arr[1:4]).upper()
		found_user = lookup_user(combined_id)
		if found_user is not None and not(found_user['name'] == last_user["name"]):
			if int(beacon_arr[-1]) > -40:
				requests.put('https://ble-prototype.firebaseio.com/basic.json', data=json.dumps(found_user))
				# print "#===============#"
				# print "name:{},\nage:{},\nlink:{},\ntx power at 1m:{},\nrssi: {}db".format(found_user['name'], found_user['age'], found_user['image'], beacon_arr[-2], beacon_arr[-1])
				# print "#===============#"
				last_user = found_user
		# else:
		# 	print "#===============#"
		# 	print "UUID:{},\nmajor:{},\nminor:{},\ntx power at 1m:{},\nrssi: {}db".format(beacon_arr[1], beacon_arr[2], beacon_arr[3], beacon_arr[-2], beacon_arr[-1])
		# 	print "#===============#"
