import json
def lookup_user(UUID):
	data = None
	with open('./data.json', 'rb') as datafile:
		data = json.load(datafile)['data']
	try:
		target = filter(lambda datum: datum['UUID'] == UUID, data)[0]
		return target["User"]
	except (KeyError, ValueError, IndexError):
		return None

if __name__ == '__main__':
    UUID1 = "B9407F30F5F8466EAFF925556B57FE6D.40695.39049"
    assert lookup_user(UUID1)["name"] == "Myra"
    UUID2 = "B9407F30F5F8466EAFF925556B57FE6D.19154.47296"
    assert lookup_user(UUID2)["age"] == 6
    print "Tests pass!"
