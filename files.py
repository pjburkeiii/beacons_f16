import jsonimport requestsimport datetimefrom flask import Flask, jsonify, requestapp = Flask(__name__)# YOUR CANVAS KEYcanvasKey = ''courseID_1 = 36417 #exploration of beaconsdef get_user_id():	op = {'access_token': canvasKey}	req = requests.get('https://canvas.vt.edu/api/v1/users/self/profile', params=op)	return req.json()['id']	def get_file_id(courseID, folderPath, fileName):	id = 0	op = {'access_token': canvasKey}		# get folder ID from path	req1 = requests.get( ('https://canvas.vt.edu/api/v1/courses/' + str(courseID) + 			'/folders/by_path' + folderPath ), params=op)		# list files in folder	req2 = requests.get( ('https://canvas.vt.edu/api/v1/folders/' + 		str(req1.json()[len(req1.json()) - 1]['id']) + '/files' ), params=op)		# get file ID from list	for i in range(0, len(req2.json())):		if(req2.json()[i]['filename'] == fileName):			id = req2.json()[i]['id']		return iddef get_file_url(fileID):	op = {'access_token': canvasKey}	req = requests.get('https://canvas.vt.edu/api/v1/files/' + str(fileID), params=op)	return req.json()['url']	def get_group_name(courseID):	group = ''	op = {'access_token': canvasKey}	req = requests.get('https://canvas.vt.edu/api/v1/users/self/groups/', params=op)	for i in range(0, len(req.json())):		if(req.json()[i]['course_id'] == courseID):			group = req.json()[i]['name']	return group@app.route('/get_agenda', methods=['GET'])def return_agenda():	data = {}		# lookup uuid to student id	userID = request.args.get('uuid')	print userID		if(userID == None):		data = {'error': 'requires uuid key parameter'}	else:		url = get_file_url(get_file_id(courseID_1, '/demo/', 'test_file.txt'))		grp = get_group_name(courseID_1)		data = { 'url': str(url), 'group_name': str(grp) }		return jsonify(**data)print get_file_url(get_file_id(courseID_1, '/demo/', 'test_file.txt'))print get_group_name(courseID_1)print str(datetime.datetime.now().date())app.run()