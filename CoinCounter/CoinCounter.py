import urllib,urllib2
import time
import json  
import csv

def sleeptime(hour,min,sec):
	return hour*3600 + min*60 + sec;

def getCoinDataFromWeb():
	# getdata
	url='https://api.coinmarketcap.com/v2/listings/';
	req = urllib2.Request(url)
	res = urllib2.urlopen(req)
	res = res.read()

	res = json.loads(res);
	return res

def GetCoinData(CoinId):
	# getdata


	url='https://api.coinmarketcap.com/v2/ticker/'+str(CoinId)+'/';
	
	
	#url='https://api.coinmarketcap.com/v2/ticker/1/'
	req = urllib2.Request(url)
	res = urllib2.urlopen(req)
	res = res.read()

	res = json.loads(res);

	CoinCurData = {};
	CoinCurData['id']=res['data']['id'];
	CoinCurData['name']=res['data']['name'];
	CoinCurData['symbol']=res['data']['symbol'];
	CoinCurData['website_slug']=res['data']['website_slug'];
	CoinCurData['rank']=res['data']['rank'];
	CoinCurData['circulating_supply']=res['data']['circulating_supply'];
	CoinCurData['total_supply']=res['data']['total_supply'];
	CoinCurData['max_supply']=res['data']['max_supply'];
	CoinCurData['price']=res['data']['quotes']['USD']['price'];
	CoinCurData['volume_24h']=res['data']['quotes']['USD']['volume_24h'];
	CoinCurData['market_cap']=res['data']['quotes']['USD']['market_cap'];
	CoinCurData['percent_change_1h']=res['data']['quotes']['USD']['percent_change_1h'];
	CoinCurData['percent_change_24h']=res['data']['quotes']['USD']['percent_change_24h'];
	CoinCurData['percent_change_7d']=res['data']['quotes']['USD']['percent_change_7d'];
	CoinCurData['last_updated']=res['data']['last_updated'];

	return	CoinCurData

def modifyCoinData(res):
	
	resUse = res['data'];
	CoinData = {}
	while len(resUse):
		PreCoinData = resUse.pop();
		key = str(PreCoinData['name']);
		CoinData[key] = {};
		CoinData[key]['symbol'] = str(PreCoinData['symbol']);
		CoinData[key]['website_slug'] = str(PreCoinData['website_slug']);
		CoinData[key]['id'] = int(PreCoinData['id']);

	return CoinData

def CsvReader(file):
	
	csvFile = open(file, "r")
	reader = csv.reader(csvFile)

	
	result = {}
	for item in reader:
	    result[item[0]] = {};
	    result[item[0]]['num'] = float(item[1]);

	csvFile.close()
	print 'read done'
	return result
	
def CsvWriter(file,CoinAcount,totalmoney):

	fileHeader = [
		"symbol", 
		"name",
		"website_slug",
		"price",
		"num",
		"totalmoney",
		"moneypercent",
		"percent_change_1h",
		"percent_change_24h",
		"percent_change_7d",
		"rank",
		"circulating_supply",
		"total_supply",
		"max_supply",
		"volume_24h",
		"market_cap",
		"last_updated",
	];

	csvFile = open(file, "w")
	writer = csv.writer(csvFile);

	writer.writerow(fileHeader);

	for key in CoinAcount:
		res = [
			CoinAcount[key]['symbol'], 
			CoinAcount[key]['name'],
			CoinAcount[key]['website_slug'],
			CoinAcount[key]['price'],
			CoinAcount[key]['num'],
			CoinAcount[key]['totalmoney'],
			CoinAcount[key]['moneypercent'],
			CoinAcount[key]['percent_change_1h'],
			CoinAcount[key]['percent_change_24h'],
			CoinAcount[key]['percent_change_7d'],
			CoinAcount[key]['rank'],
			CoinAcount[key]['circulating_supply'],
			CoinAcount[key]['total_supply'],
			CoinAcount[key]['max_supply'],
			CoinAcount[key]['volume_24h'],
			CoinAcount[key]['market_cap'],
			CoinAcount[key]['last_updated'],
		];
		writer.writerow(res);

	res = [' ','totalmoney',':',totalmoney];
	
	writer.writerow(res);

	csvFile.close();
	print 'write done'
	pass 

def CoinCounter():

	second1 = sleeptime(0,5,0);
	second2 = sleeptime(0,0,1);
	res = getCoinDataFromWeb();
	CoinData = modifyCoinData(res);
	CoinAcount = CsvReader('data.csv');
	for key in CoinAcount:
		if 	CoinData.has_key(key):
			CoinId = CoinData[key]['id'];
			CoinCurData = GetCoinData(CoinId);
			CoinAcount[key].update(CoinCurData);
			CoinAcount[key]['totalmoney'] = CoinAcount[key]['price'] * CoinAcount[key]['num']; 
		else :
			print 'Error!',
			print key,
			print 'is not a key'

	totalmoney = 0;
	for key in CoinAcount:
		totalmoney += CoinAcount[key]['totalmoney'] ;

	print 'we have money :',
	print totalmoney

	for key in CoinAcount:
		CoinAcount[key]['moneypercent'] =  CoinAcount[key]['totalmoney']/totalmoney;

	CsvWriter('result.csv',CoinAcount,totalmoney);
	





	#CoinData = {};
	#CoinData = eval(res);
	

	#print isinstance(CoinData,str);
	#print isinstance(CoinData,dict);
	#print CoinData;
	'''
	while 1==1:
		
		res=getDataFromWeb(1);
		data=modifyData(res);
		
		res=getDataFromWeb(1027);
		data=modifyData(res);
		
		res=getDataFromWeb(1765);
		data=modifyData(res);

		res=getDataFromWeb(1908);
		data=modifyData(res);
		
		#
		
		i = 60*5;
		while i:
			time.sleep(second2);
			print('.'),
			i-=1;
			pass
			
		print('='*50)
		
		pass
	'''

if __name__=="__main__":   
    CoinCounter();
	









