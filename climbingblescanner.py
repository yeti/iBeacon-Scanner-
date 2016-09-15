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
				print "Incrementing " + user['name'] + "'s Score"
				print "============"
				user['score'] = user['score'] + 10
				if 'rockClimbing' in user['experiences']:
					user['experiences']['rockClimbing']['visits'] = user['experiences']['rockClimbing']['visits'] + 1
					climbing_badges = myfirebase.get('/attractions/climbingWall/badges', None)
					if user['experiences']['rockClimbing']['visits'] is 2:
						user['badges']['yosemite'] = climbing_badges['yosemite']
				else:
					user['experiences']['rockClimbing'] = {'visits': 1}

				requests.put('https://ble-prototype.firebaseio.com/users/{}.json'.format(beacon_id), data=json.dumps(user))
			range_beacons.append(beacon_id)

	for beacon in range_beacons:
		if beacon not in returned_beacon_ids:
			range_beacons.remove(beacon)
