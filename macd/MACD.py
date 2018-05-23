from CsvRead import CsvReader
from CsvRead import CsvWriter


def modifyData(result):
	
	interSec = 60;
	resultUse= {};
	for res in result:

		#resultUse[res] = result[res];
		resultUse[int(res)] = {'price':float(result[res])}
		res = str(int(res) + interSec);
	
	print 'modify data done'
	return resultUse

def MacdCalc(resultUse,interSec):

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

def MacdHead(result):
	# calc first line macd
	resultMacd = {};
	resultMacd['price'] = result['price'];
	resultMacd['ema12'] = 0;
	resultMacd['ema26'] = 0;
	resultMacd['diff'] = 0;
	resultMacd['dea'] = 0;
	resultMacd['macd'] = 0;
	return resultMacd

def MacdSeconline(lastresult,result):


	LastDayEma12 = lastresult['ema12'];
	LastDayEma26 = lastresult['ema26'];
	LastDea = lastresult['dea'];
	LastPrice = lastresult['price'];

	resultMacd = {};
	price = result['price'];
	resultMacd['price'] = price;
	resultMacd['ema12'] = LastPrice + (price - LastPrice)*2/13;
	resultMacd['ema26'] = LastPrice + (price - LastPrice)*2/27;
	resultMacd['diff'] = resultMacd['ema12'] - resultMacd['ema26'] ;
	resultMacd['dea'] = LastDea*8/10 + resultMacd['diff'] *2/10 ;
	resultMacd['macd'] = 2 * (resultMacd['diff'] - resultMacd['dea']);
	
	return resultMacd

def MacdNomalCalc(lastresult,result):

	LastDayEma12 = lastresult['ema12'];
	LastDayEma26 = lastresult['ema26'];
	LastDea = lastresult['dea'];
	LastPrice = lastresult['price'];

	resultMacd = {};
	price = result['price'];
	resultMacd['price'] = price;
	resultMacd['ema12'] = LastDayEma12 * 11/13 + price *2/13;
	resultMacd['ema26'] = LastDayEma26 * 25/27 + price *2/27;
	resultMacd['diff'] = resultMacd['ema12'] - resultMacd['ema26'] ;
	resultMacd['dea'] = LastDayDea*8/10 + resultMacd['diff'] *2/10 ;
	resultMacd['macd'] = 2 * (resultMacd['diff'] - resultMacd['dea']);

	return resultMacd




def TradeSimu():

	# read from csv
	result = CsvReader("data.csv");

	# modify result
	resultUse = modifyData(result);

	
	#resultMacd = MacdCalc(resultUse,60);
	#CsvWriter("data1.csv",resultMacd);


	'''
	resultMacd = MacdCalc(resultUse,interSec);
	
	moneyAmount = 10000;
	buySellState = 0;
	'''
	




if __name__=="__main__":   
	TradeSimu()
	pass
    
	
