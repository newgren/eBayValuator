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
	num = 20
	if 'keywords' in request.args:
		keys = str(request.args['keywords'])
		print keys
	if 'num' in request.args:
		num = int(str(request.args['num']))
	now = datetime.datetime.now().time()



	# properly formats spaces
	inputList = ['iphone 5s 16GB']
	newList = []
	for i in xrange(len(inputList)):
		newList.append(urllib2.quote(inputList[i]))
	avgList = []
	imgList = []
	for query in newList:
		url = "http://svcs.ebay.com/services/search/FindingService/v1?OPERATION-NAME=findCompletedItems&SECURITY-APPNAME=TravisNe-Project1-PRD-e45f6444c-e24c2db3&keywords="+query+"&RESPONSE-DATA-FORMAT=JSON&paginationInput.entriesPerPage="+str(num)+"&itemFilter(0).name=ListingType&itemFilter(0).value(0)=FixedPrice&sortOrder=endingTimeSoonest"#&itemFilter(1).name=EndTimeFrom&itemFilter(1).value="#+str(now)
		arequest = urllib2.Request(url)
		response = urllib2.urlopen(arequest).read()
		obj = json.loads(response)
		#return str(obj)
		resultsArr = obj['findCompletedItemsResponse'][0]['searchResult'][0]['item']
		total = 0.0
		for i in xrange(num):
			imgList.append(resultsArr[i]['galleryURL'][0])
			total += float(resultsArr[i]['sellingStatus'][0]['currentPrice'][0]['__value__'])
		avgList.append(total/num)
	outputString = ""
	imgOutput = ""
	for i in xrange(len(newList)):
		outputString += inputList[i] + "\t" + str(avgList[i]) + "<br>"
	for i in xrange(len(imgList)):
		imgOutput+= '<img src="' + str(imgList[i]) + '"/>' +"<p>"+str(resultsArr[i]['listingInfo'][0]['endTime'])+"</p>"+"<p>"+str(resultsArr[i]['sellingStatus'][0]['currentPrice'][0]['__value__'])+"</p>"
	return outputString + "<br>" + imgOutput
	
@app.route('/compare')
def compare():
	keys = ""
	num = 10
	if 'keywords' in request.args:
		keys = str(request.args['keywords'])
		print keys
	if 'num' in request.args:
		num = int(str(request.args['num']))
	now = datetime.datetime.now().time()



	# properly formats spaces
	inputList = ['samsung galaxy note 7']
	newList = []
	for i in xrange(len(inputList)):
		newList.append(urllib2.quote(inputList[i]))

	avgList = []
	medListFixed = []
	medListAuction = []
	imgListFixed = []
	imgListAuction = []
	for query in newList:
		fixedUrl = "http://svcs.ebay.com/services/search/FindingService/v1?OPERATION-NAME=findCompletedItems&SECURITY-APPNAME=TravisNe-Project1-PRD-e45f6444c-e24c2db3&keywords="+query+"&RESPONSE-DATA-FORMAT=JSON&paginationInput.entriesPerPage="+str(num)+"&sortOrder=endingTimeSoonest&itemFilter(0).name=ListingType&itemFilter(0).value(0)=FixedPrice&itemFilter(1).name=Condition&itemFilter(1).value(1)=1000"
		auctionUrl = "http://svcs.ebay.com/services/search/FindingService/v1?OPERATION-NAME=findCompletedItems&SECURITY-APPNAME=TravisNe-Project1-PRD-e45f6444c-e24c2db3&keywords="+query+"&RESPONSE-DATA-FORMAT=JSON&paginationInput.entriesPerPage="+str(num)+"&sortOrder=endingTimeSoonest&itemFilter(0).name=ListingType&itemFilter(0).value(0)=Auction&itemFilter(0).value(1)=AuctionWithBIN&itemFilter(1).name=Condition&itemFilter(1).value(0)=1000"

		arequest = urllib2.Request(fixedUrl)
		response = urllib2.urlopen(arequest).read()
		obj = json.loads(response)
		#return str(obj)
		resultsArr = obj['findCompletedItemsResponse'][0]['searchResult'][0]['item']
		fixedTotal = 0.0
		for i in xrange(num):
			imgListFixed.append(resultsArr[i]['galleryURL'][0])
			fixedTotal += float(resultsArr[i]['sellingStatus'][0]['currentPrice'][0]['__value__'])
			medListFixed.append(float(resultsArr[i]['sellingStatus'][0]['currentPrice'][0]['__value__']))
		avgList.append(fixedTotal/num)


		arequest = urllib2.Request(auctionUrl)
		response = urllib2.urlopen(arequest).read()
		obj = json.loads(response)
		#return str(obj)
		resultsArr = obj['findCompletedItemsResponse'][0]['searchResult'][0]['item']
		auctionTotal = 0.0
		for i in xrange(num):
			imgListAuction.append(resultsArr[i]['galleryURL'][0])
			auctionTotal += float(resultsArr[i]['sellingStatus'][0]['currentPrice'][0]['__value__'])
			medListAuction.append(float(resultsArr[i]['sellingStatus'][0]['currentPrice'][0]['__value__']))
		avgList.append(auctionTotal/num)


	outputString = ""
	imgOutput = ""
	outputString += "Means:<br>"
	for i in xrange(len(avgList)):
		outputString += "<span>" + str(avgList[i]) + "</span><br>"
	for i in xrange(len(imgListFixed)):
		imgOutput+= '<img src="' + str(imgListFixed[i]) +"/>"
	outputString += "Medians:<br>"+str(median(medListFixed))+"<br>"+str(median(medListAuction))

	imgOutput+= "<br><br><br>"
	for i in xrange(len(imgListAuction)):
		imgOutput+= '<img src="' + str(imgListAuction[i]) +"/>"
	return outputString + "<br>" + imgOutput
	
def median(lst):
    sortedLst = sorted(lst)
    lstLen = len(lst)
    index = (lstLen - 1) // 2

    if (lstLen % 2):
        return sortedLst[index]
    else:
        return (sortedLst[index] + sortedLst[index + 1])/2.0


if __name__ == '__main__':
	app.run(debug=True)


