from CsvRead import CsvReader
from CsvRead import CsvWriter


def modifyData(result,interSec):
	
	resultUse= {};
	for res in result:

		#resultUse[res] = result[res];
		resultUse[int(res)] = {'price':float(result[res])}
		res = str(int(res) + interSec);
	
	print 'modify data done'
	return resultUse

def MacdCalc():
	
	# read from csv
	result = CsvReader("data.csv");

	# modify result
	interSec = 60;
	resultUse = modifyData(result,interSec);
	#print resultUse

	# find min key
	minKey = min(resultUse.keys());
	
	resultMacd = {};


	# calc first line macd
	resultMacd[minKey] = {};
	resultMacd[minKey]['price'] = resultUse[minKey]['price'];
	resultMacd[minKey]['ema12'] = 0;
	resultMacd[minKey]['ema26'] = 0;
	resultMacd[minKey]['diff'] = 0;
	resultMacd[minKey]['dea'] = 0;
	resultMacd[minKey]['macd'] = 0;

	LastDayEma12 = resultMacd[minKey]['ema12'];
	LastDayEma26 = resultMacd[minKey]['ema26'];
	LastDea = resultMacd[minKey]['dea'];
	LastPrice = resultMacd[minKey]['price'];

	# calc second line macd
	key = minKey+interSec;
	resultMacd[key] = {};
	price = resultUse[key]['price'];
	resultMacd[key]['price'] = price;
	resultMacd[key]['ema12'] = LastPrice + (price - LastPrice)*2/13;
	resultMacd[key]['ema26'] = LastPrice + (price - LastPrice)*2/27;
	resultMacd[key]['diff'] = resultMacd[key]['ema12'] - resultMacd[key]['ema26'] ;
	resultMacd[key]['dea'] = LastDea*8/10 + resultMacd[key]['diff'] *2/10 ;
	resultMacd[key]['macd'] = 2 * (resultMacd[key]['diff'] - resultMacd[key]['dea']);

	LastDayEma12 = resultMacd[key]['ema12'];
	LastDayEma26 = resultMacd[key]['ema26'];
	LastDayDea = resultMacd[key]['dea'];
	LastPrice = resultMacd[key]['price'];	

	keylist = resultUse.keys();
	keylist.remove(key);
	keylist.remove(minKey);
	keylist.sort();
	

	# calc all macd
	for key in keylist:
		resultMacd[key] = {};
		price = resultUse[key]['price'];
		resultMacd[key]['price'] = price;
		resultMacd[key]['ema12'] = LastDayEma12 * 11/13 + price *2/13;
		resultMacd[key]['ema26'] = LastDayEma26 * 25/27 + price *2/27;
		resultMacd[key]['diff'] = resultMacd[key]['ema12'] - resultMacd[key]['ema26'] ;
		resultMacd[key]['dea'] = LastDayDea*8/10 + resultMacd[key]['diff'] *2/10 ;
		resultMacd[key]['macd'] = 2 * (resultMacd[key]['diff'] - resultMacd[key]['dea']);


		LastDayEma12 = resultMacd[key]['ema12'];
		LastDayEma26 = resultMacd[key]['ema26'];
		LastDayDea = resultMacd[key]['dea'];
		LastPrice = resultMacd[key]['price'];
		key = key+interSec;

	CsvWriter('data1.csv',resultMacd)

	print 'macd calc done'
	

def btcControl():
	resultMacd = MacdCalc()



if __name__=="__main__":   
	btcControl()
	pass
    
	
