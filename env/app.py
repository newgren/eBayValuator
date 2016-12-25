#!flask/bin/python
from flask import Flask, request
import base64
import urllib
import urllib2
import json
from xml.dom.minidom import parse
import datetime
import time
from datetime import date, timedelta

app = Flask(__name__)


@app.route('/')
def index():
	return "Main"

@app.route('/search')
def search():
	keys = ""
	num = 50
	if 'keywords' in request.args:
		keys = str(request.args['keywords'])
		print keys
	if 'num' in request.args:
		num = int(str(request.args['num']))
	now = datetime.datetime.now().time()



	# properly formats spaces
	inputList = ['macbook pro','macbook air','macbook','htc']
	newList = []
	for i in xrange(len(inputList)):
		newList.append(urllib2.quote(inputList[i]))
	inputList = newList
	avgList = []
	imgList = []
	for query in inputList:
		url = "http://svcs.ebay.com/services/search/FindingService/v1?OPERATION-NAME=findCompletedItems&SECURITY-APPNAME=TravisNe-Project1-PRD-e45f6444c-e24c2db3&keywords="+query+"&RESPONSE-DATA-FORMAT=JSON&paginationInput.entriesPerPage="+str(num)+"&itemFilter(0).name=ListingType&itemFilter(0).value(0)=FixedPrice&sortOrder=endingTimeSoonest"#&itemFilter(1).name=EndTimeFrom&itemFilter(1).value="#+str(now)
		arequest = urllib2.Request(url)
		response = urllib2.urlopen(arequest).read()
		obj = json.loads(response)
		resultsArr = obj['findCompletedItemsResponse'][0]['searchResult'][0]['item']
		total = 0.0
		for i in xrange(num):
			imgList.append(resultsArr[i]['galleryURL'][0])
			total += float(resultsArr[i]['sellingStatus'][0]['currentPrice'][0]['__value__'])
		avgList.append(total/num)
	outputString = ""
	imgOutput = ""
	for i in xrange(len(inputList)):
		outputString += inputList[i] + "\t" + str(avgList[i]) + "<br>"
	for i in xrange(len(imgList)):
		imgOutput+= '<img src="' + str(imgList[i]) + '"/>'
	return outputString + "<br>" + imgOutput
	




if __name__ == '__main__':
	app.run(debug=True)


