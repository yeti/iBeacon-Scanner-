# test BLE Scanning software
# jcs 6/8/2014

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

myfirebase = firebase.FirebaseApplication('https://ble-prototype.firebaseio.com', None)
blescan.hci_le_set_scan_parameters(sock)
blescan.hci_enable_le_scan(sock)

range_beacons = list()

# continuously scans for new beacons
while True:
	returned_beacons = blescan.parse_events(sock, 10)
	returned_beacon_ids = []
	# parse the ids from all nearby beacons
	for beacon in returned_beacons:
		beacon_arr = beacon.split(',')
		beacon_id = "".join(beacon_arr[1:4]).upper()
		returned_beacon_ids.append(beacon_id)
	# for each id nearby
	for beacon_id in returned_beacon_ids:
		# if the beacon wasn't already in range of pi
		if beacon_id not in range_beacons:
			user = myfirebase.get('/users/{}'.format(beacon_id), None)

			# checks that user exists
			if user is not None:
				range_beacons.append(beacon_id)
				print "Incrementing " + user['name'] + "'s Score"
				print "============"
				user['score'] = user['score'] + 25
				attraction = myfirebase.get('/attractions/volcanoJamboree', None)

				if 'volcanoJamboree' in user['experiences']:
					user['experiences']['volcanoJamboree']['visits'] = user['experiences']['volcanoJamboree']['visits'] + 1
					if user['experiences']['volcanoJamboree']['visits'] is 2:
						user['badges']['diamond'] = attraction['badges']['diamond']
					elif user['experiences']['volcanoJamboree']['visits'] is 3:
						user['badges']['star'] = attraction['badges']['star']
				else:
					user['experiences']['volcanoJamboree'] = {'visits': 1}
					user['badges']['mountHaleakala'] = attraction['badges']['mountHaleakala']

				requests.put('https://ble-prototype.firebaseio.com/users/{}.json'.format(beacon_id), data=json.dumps(user))
				attraction['user'] = user
				requests.put('https://ble-prototype.firebaseio.com/attractions/volcanoJamboree.json', data=json.dumps(attraction))


	for beacon in range_beacons:
		if beacon not in returned_beacon_ids:
			print "User out of range!"
			print "==============="
			myfirebase.delete('/attractions/volcanoJamboree/user', None)
			range_beacons.remove(beacon)
