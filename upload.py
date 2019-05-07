#!/usr/bin/env python3

'''
	Here's how you upload an image. For this example, put the cutest picture
	of a kitten you can find in this script's folder and name it 'Kitten.jpg'

	For more details about images and the API see here:
		https://api.imgur.com/endpoints/image
'''

# Pull authentication from the auth example (see auth.py)
from auth import authenticate
from datetime import datetime
from flask import Flask, request
import json
from subprocess import call

import string
from random import *
import datetime
from queue import Queue
from threading import Thread
import logging

app = Flask(__name__)
album = None # You can also enter an album ID here
characters = string.ascii_letters + string.digits
job_details = {}
completed = {}
pending = {}
failed = {}
q = Queue(maxsize=0)

#image upload api
@app.route('/v1/images/upload', methods=['POST'])
def post():
		imgUrls = []
		imgUrls = request.json['urls']
		print(imgUrls)
		job_id =  "".join(choice(characters) for x in range(randint(16, 16)))
		print("job id created: "+job_id)
		status = "pending"
		finished = "null"
		job_created = datetime.datetime.utcnow().isoformat()
		job_details.update({job_id : {"id" : job_id, "status" : status, "finished" : finished, "created" : job_created, "uploaded" : "no"}})

		num_threads = min(1, len(imgUrls))
		completed.update({job_id : {"urls" : []}})
		pending.update({job_id : {"urls" : []}})
		failed.update({job_id : {"urls" : []}})

		#load queue with urls
		for i in range(len(imgUrls)):
		#need the index and the url in each queue item.
			q.put(imgUrls[i])

		#client authentication to imgur
		client = authenticate()

		#Initiating threads for each image upload
		for i in range(num_threads):
				print("Threads")
				logging.debug('Starting thread ', i)
				worker = Thread(target=crawl, args=(q, job_id, client))
				worker.setDaemon(True)    #setting threads as "daemon" allows main program to
											#exit eventually even if these dont finish
											#correctly.
				worker.start()
		q.join()

		#job finish time
		job_completed = datetime.datetime.utcnow().isoformat()
		job_details.get(job_id).update({"finished" : job_completed})

		return job_id

def crawl(q, job_id, client):
		#get image url from queue and download to local. Upload the download image
		while not q.empty():
			work = q.get()                      #fetch new work from the Queue
			call('curl '+str(work)+' --output downloaded/image_to_be_uploaded', shell=True)
			image_path = 'downloaded/image_to_be_uploaded'
			try:
				client.upload_from_path(image_path, anon=False)
				completed.get(job_id).get("urls").append(work)
			except Exception as e:
				logging.error(e, exc_info=True)
				failed.get(job_id).get("urls").append(work)

			#signal to the queue that task has been processed
			q.task_done()
		return True

#get image-upload job details
@app.route('/v1/images/uploaded/<jobId>', methods=['GET'])
def get(jobId):
		jobId = jobId
		uploaded = {"completed" : [], "pending" : [], "failed" : []}
		pending.get(jobId)["urls"] = list(q.queue)
		uploaded.get("failed").extend(failed.get(jobId).get("urls"))
		uploaded.get("pending").extend(pending.get(jobId).get("urls"))
		uploaded.get("completed").extend(completed.get(jobId).get("urls"))
		if not completed.get(jobId).get("urls"):
			job_details.get(jobId).update({"status": "pending"})
		elif completed.get(jobId).get("urls") and pending.get(jobId).get("urls"):
			job_details.get(jobId).update({"status": "in-progress"})
		elif not pending.get(jobId).get("urls"):
			job_details.get(jobId).update({"status": "completed"})
		job_details.get(jobId).update({"uploaded" : uploaded})
		return json.dumps(job_details.get(jobId))

#to receive all images on the account
@app.route('/v1/images', methods=['GET'])
def get_all():
	client = authenticate()
	images = []
	for album1 in client.get_account_albums('me'):
		for image in client.get_album_images(album1.id):
			images.append(image.link)
	return json.dumps({"images" : images})

# If you want to run this as a standalone script
if __name__ == "__main__":
	app.run(debug=True, port=8080)