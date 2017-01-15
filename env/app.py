#!flask/bin/python
from flask import Flask, request
import base64
import urllib
import urllib2
import json
from xml.dom.minidom import parse

app = Flask(__name__)


@app.route('/')
def index():
	return "Main"

@app.route('/debug')
def debug():
	keys = ""
	num = 20
	if 'keywords' in request.args:
		keys = str(request.args['keywords'])
		print keys
	if 'num' in request.args:
		num = int(str(request.args['num']))
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
		return str(obj)
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
	

@app.route('/getcomparison')
def getcomparison():
	'''
	Request Parameters:
		itemName
	'''
	itemName = ""
	itemsPerPage = 50
	try:
		itemName = urllib2.quote(request.args['itemName'])
		print itemName
	except ValueError:
		print ValueError

	outputString = ""

	# Num sold in past week, month

	# Auction vs BIN
	auctionUrl = "http://svcs.ebay.com/services/search/FindingService/v1?OPERATION-NAME=findCompletedItems&SECURITY-APPNAME=TravisNe-Project1-PRD-e45f6444c-e24c2db3&keywords="+str(itemName)+"&RESPONSE-DATA-FORMAT=JSON&paginationInput.entriesPerPage="+str(itemsPerPage)+"&itemFilter(0).name=ListingType&itemFilter(0).value(0)=Auction&itemFilter(1).name=Condition&itemFilter(1).value(0)=3000&itemFilter(2).name=SoldItemsOnly&itemFilter(2).value=true"
	aobj = urlToJSON(auctionUrl)
	aprices = []
	for i in xrange(itemsPerPage):
		aprices.append(float(aobj[i]['sellingStatus'][0]['currentPrice'][0]['__value__']))
	aprices = removeOutliers(sorted(aprices))

	fixedUrl = "http://svcs.ebay.com/services/search/FindingService/v1?OPERATION-NAME=findCompletedItems&SECURITY-APPNAME=TravisNe-Project1-PRD-e45f6444c-e24c2db3&keywords="+str(itemName)+"&RESPONSE-DATA-FORMAT=JSON&paginationInput.entriesPerPage="+str(itemsPerPage)+"&itemFilter(0).name=ListingType&itemFilter(0).value(0)=FixedPrice&itemFilter(1).name=Condition&itemFilter(1).value(0)=3000&itemFilter(2).name=SoldItemsOnly&itemFilter(2).value=true"
	bobj = urlToJSON(fixedUrl)	
	bprices = []
	for i in xrange(itemsPerPage):
		bprices.append(float(bobj[i]['sellingStatus'][0]['currentPrice'][0]['__value__']))
	bprices = removeOutliers(sorted(bprices))

	outputString += str(median(aprices)) + "<br>" + str(median(bprices))+"<br><br>"

	# Free Shipping vs Shipping
	freeUrl = "http://svcs.ebay.com/services/search/FindingService/v1?OPERATION-NAME=findCompletedItems&SECURITY-APPNAME=TravisNe-Project1-PRD-e45f6444c-e24c2db3&keywords="+str(itemName)+"&RESPONSE-DATA-FORMAT=JSON&paginationInput.entriesPerPage="+str(itemsPerPage)+"&itemFilter(0).name=Condition&itemFilter(0).value(0)=3000&itemFilter(1).name=SoldItemsOnly&itemFilter(1).value=true&itemFilter(2).name=FreeShippingOnly&itemFilter(2).value=true"
	aobj = urlToJSON(freeUrl)
	aprices = []
	for i in xrange(itemsPerPage):
		aprices.append(float(aobj[i]['sellingStatus'][0]['currentPrice'][0]['__value__']))
	aprices = removeOutliers(sorted(aprices))

	paidUrl = "http://svcs.ebay.com/services/search/FindingService/v1?OPERATION-NAME=findCompletedItems&SECURITY-APPNAME=TravisNe-Project1-PRD-e45f6444c-e24c2db3&keywords="+str(itemName)+"&RESPONSE-DATA-FORMAT=JSON&paginationInput.entriesPerPage="+str(itemsPerPage)+"&itemFilter(0).name=Condition&itemFilter(0).value(0)=3000&itemFilter(1).name=SoldItemsOnly&itemFilter(1).value=true&itemFilter(2).name=FreeShippingOnly&itemFilter(2).value=false"
	bobj = urlToJSON(paidUrl)	
	bprices = []
	for i in xrange(itemsPerPage):
		#this is broken
		bprices.append(float(bobj[i]['sellingStatus'][0]['currentPrice'][0]['__value__']))#+ float(bobj[i]['shippingInfo'][0]['shippingServiceCost'][0]['__value__']))
	bprices = removeOutliers(sorted(bprices))

	outputString += str(median(aprices)) + "<br>" + str(median(bprices))

	# US vs International

	return outputString





@app.route('/oldCompare')
def oldCompare():
	keys = "iphone"
	num = 100
	if 'keywords' in request.args:
		keys = str(request.args['keywords'])
		print keys
	if 'num' in request.args:
		num = int(str(request.args['num']))

	
	inputList = ['samsung galaxy s7']
	newList = []
	for i in xrange(len(inputList)):
		newList.append(urllib2.quote(inputList[i])) # properly formats spaces

	avgList = []
	medListFixed = []
	medListAuction = []
	imgListFixed = []
	imgListAuction = []
	for query in newList:
		fixedUrl = "http://svcs.ebay.com/services/search/FindingService/v1?OPERATION-NAME=findCompletedItems&SECURITY-APPNAME=TravisNe-Project1-PRD-e45f6444c-e24c2db3&keywords="+query+"&RESPONSE-DATA-FORMAT=JSON&paginationInput.entriesPerPage="+str(num)+"&sortOrder=endingTimeSoonest&itemFilter(0).name=ListingType&itemFilter(0).value(0)=FixedPrice&itemFilter(1).name=Condition&itemFilter(1).value(1)=3000&itemFilter(2).name=SoldItemsOnly&itemFilter(2).value=true"
		auctionUrl = "http://svcs.ebay.com/services/search/FindingService/v1?OPERATION-NAME=findCompletedItems&SECURITY-APPNAME=TravisNe-Project1-PRD-e45f6444c-e24c2db3&keywords="+query+"&RESPONSE-DATA-FORMAT=JSON&paginationInput.entriesPerPage="+str(num)+"&sortOrder=endingTimeSoonest&itemFilter(0).name=ListingType&itemFilter(0).value(0)=Auction&itemFilter(0).value(1)=AuctionWithBIN&itemFilter(1).name=Condition&itemFilter(1).value(0)=3000&itemFilter(2).name=SoldItemsOnly&itemFilter(2).value=true"

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
	

def urlToJSON(url):
	arequest = urllib2.Request(url)
	return json.loads(urllib2.urlopen(arequest).read())['findCompletedItemsResponse'][0]['searchResult'][0]['item']

def removeOutliers(data):
	n = len(data)
	med = data[n/2]
	print med
	Q1 = data[n/4]
	print Q1
	Q3 = data[3*n/4]
	print Q3
	IQR = Q3-Q1
	lower = med - 1.5*IQR
	upper = med + 1.5*IQR
	newData = []
	for thing in data:
		if thing > lower and thing < upper:
			newData.append(thing)
	return newData

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


