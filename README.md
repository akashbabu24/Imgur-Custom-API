Python custom API application for imgur
===========

A Python API intermediate app for the [Imgur API](http://api.imgur.com/). It can be used to auto-logon to imgur and upload multiple images, 
to track the upload jobs and the individual uploads, and to get all images that are uploaded to the account.

You must [register](http://api.imgur.com/oauth2/addclient) your client with the Imgur API, and provide the Client-ID to
make *any* request to the API (see the [Authentication](https://api.imgur.com/#authentication) note). If you want to
perform actions on accounts, the user will have to authorize your application through OAuth2.

Requirements
------------
Once client application is registered with imgur, please add below values to auth.ini,

client_id=

client_secret=

refresh_token=

imgur_username=

imgur_password=

It is a Dockerized application. So, required tools are included as part of Dockerfile. Just plug and play.

Application:

Once client is registered with imgur and credentials are saved in auth.ini file, the app can be used. Operations are explained as below,
1) The auth.py takes care of automated logon to user account on imgur using the client credentials supplied. Selenium for Python and PhantomJS have been used for this purpose.

2) The upload.py has three APIs - for upload job, for status check, and for retrieval of all image links

	a) Each image upload stream/request is given an unique alphanumeric ID that is returned as response. Images are uploaded to the account and can be found in 'All Images' on imgur account.
	
		Eg: curl -X POST -H "Content-Type: application/json" -d '{"urls" : ["https://i.imgur.com/gAGub9k.jpg", "https://www.factslides.com/imgs/black-cat.jpg"]}' http://127.0.0.1:8080/v1/images/upload
			{"job_id": "zb8sgTGBUruHuchx"}
	b) Queue and Threads are used to track the image upload jobs and also individual image uploads. Image upload status and job status/details are returned as response.
	
		Eg: curl http://127.0.0.1:8080/v1/images/uploaded/zb8sgTGBUruHuchx
			{"status": "completed", "uploaded": {"failed": ["https://www.factslides.com/imgs/black-cat.jpg"], "completed": ["https://i.imgur.com/gAGub9k.jpg"], "pending": []}, "finished": "2019-05-09T19:37:39.130685", "created": "2019-05-09T19:37:33.770511", "id": "zb8sgTGBUruHuchx"}
	c) get_account_images() method from imgur python library is used to fetch all images from the account,	
	
		Eg: curl -H "Accept: application/json" "http://127.0.0.1:8080/v1/images"
		{"images": ["https://i.imgur.com/K2Puw4S.jpg", "https://i.imgur.com/XzQl8EL.jpg", "https://i.imgur.com/157Qf83.jpg", "https://i.imgur.com/D2IJrn7.jpg", "https://i.imgur.com/Dn5wQdA.jpg"]}

Docker runtime setup (add sudo before docker commands if not priviledged user)
------------
#Build the Flask app as Docker image

docker build -t <tag> <Dockerfile directory>

Eg: docker build -t myuploader .

#run Flask app as a container

docker run -p 8080:8080 <image-tag>

Eg: docker run -p 8080:8080 myuploader

App Usage (add sudo before docker commands if not priviledged user)
------------
Once container is run, logon to the container and run the CURL commands for image operations,

#find the container that was executed,

docker container ls

#Logon to the container using below command

docker exec -it <container id or name> /bin/bash

Eg: docker exec -it 4de42ba3711a /bin/bash

#Execute the below CURL commands for mentioned operations,
# Image upload POST request

curl -X POST -H "Content-Type: application/json" -d '{"urls" : <image-list>}' http://127.0.0.1:8080/v1/images/upload

Eg: curl -X POST -H "Content-Type: application/json" -d '{"urls" : ["https://i.imgur.com/gAGub9k.jpg", "https://www.factslides.com/imgs/black-cat.jpg"]}' http://127.0.0.1:8080/v1/images/upload

# Status check GET request

curl http://127.0.0.1:8080/v1/images/uploaded/<job id returned as response in the previous upload command>

Eg: curl http://127.0.0.1:8080/v1/images/uploaded/GYvgEqVCH5RsaTg6

#GET request to get all images

curl -H "Accept: application/json" "http://127.0.0.1:8080/v1/images"

Imgur entry points
==================
| entry point                         |  content                       |
|-------------------------------------|--------------------------------|
| /v1/images/upload					  | image upload 				   |
| /v1/images/uploaded/<jobId>	      | upload job/image status/details|
| /v1/images			              | get links of all images        |

Known gaps:
------------
1) Upload job is returned once the upload process is completed. It can be made asynchronous with an additional effort using threads, however, as of now, it is not asynchronous.

2) Images are uploaded to 'All Images' and not to any specific Album purposefully. Images are not given any name or description.

3) To send request to the Docker application, one needs to logon to the container and initiate CUrl requests. Docker networking part is not worked on yet, to enable access from outside the container.
