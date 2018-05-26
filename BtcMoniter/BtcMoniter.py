import urllib,urllib2
import time

def sleeptime(hour,min,sec):
	return hour*3600 + min*60 + sec;

def getDataFromWeb(id):
# getdata
	url='https://api.coinmarketcap.com/v2/ticker/'+str(id)+'/';
	
	#url='https://api.coinmarketcap.com/v2/ticker/1/'
	req = urllib2.Request(url)
	res = urllib2.urlopen(req)
	res = res.read()
	return res

def modifyData(res):
	# find name
	index1 = res.find("name", 0, len(res))
	index2 = res.find("\",", index1, len(res))
	name = res[index1+8:index2]
	#	print name
	
	# find price
	index1 = res.find("price", 0, len(res))
	index2 = res.find(",", index1, len(res))
	price = res[index1+8:index2]
	#	print price

	# find price
	index1 = res.find("symbol", 0, len(res))
	index2 = res.find("\"", index1+10, len(res))
	symbol = res[index1+10:index2]
	# print symbol


	# find time
	index = res.find("timestamp", 0, len(res))
	timestamp = int(res[index+12:index+22])
	#	print(timestamp)
	time_local = time.localtime(timestamp)
	dt = time.strftime("%Y-%m-%d %H:%M:%S",time_local)
	#	print dt
	
	data = {}
	data['name'] = name
	data['price'] = price
	data['time'] = dt
	data['timestamp'] = timestamp
	data['symbol'] = symbol

	print(data['time']),
	print(' '*5),
	print(data['symbol']),
	print(' '*5),
	print(data['price'])

	return data
	

def ffbtc():
	second1 = sleeptime(0,5,0);
	second2 = sleeptime(0,0,1);

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


if __name__=="__main__":   
    ffbtc()
	









