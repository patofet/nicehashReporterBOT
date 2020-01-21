import os
import json
import requests
print("This line will be printed.")
urlB = "https://api.nicehash.com/api?method=stats.provider.workers&addr=36WwfnEKfBWHXddE3hQq9NpMuQCKF9CTpQ"
myResponse = requests.get(urlB)
if(myResponse.ok):
	jData = json.loads(myResponse.content)
	print("The response contains {0} properties".format(len(jData)))
	print("\n")
	for key in jData:
		if(key=="result"):
			for keyIn in jData[key]:
				if(keyIn=="workers"):
					print keyIn + ": "
					for keyInIn in jData[key][keyIn]:
						print "Name:" + keyInIn[0]
						print "\tSpeed:" + str(keyInIn[1]['a'])
						print "\tConec:" + str(keyInIn[2])
						print "\tXnSub:" + str(keyInIn[3])
						print "\tDiffi:" + str(keyInIn[4])
						print "\tLocat:" + str(keyInIn[5])
						print "\tAlgor:" + str(keyInIn[6])
				else:
					print keyIn + " : " + str(jData[key][keyIn])
os.system("pause")