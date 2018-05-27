from CsvRead import CsvReader
from CsvRead import CsvWriter
from CsvRead import TextWriter



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
	LastDayDea = lastresult['dea'];
	LastPrice = lastresult['price'];

	resultMacd = {};
	price = result['price'];
	resultMacd['price'] = price;
	resultMacd['ema12'] = LastPrice + (price - LastPrice)*2/13;
	resultMacd['ema26'] = LastPrice + (price - LastPrice)*2/27;
	resultMacd['diff'] = resultMacd['ema12'] - resultMacd['ema26'] ;
	resultMacd['dea'] = LastDayDea*8/10 + resultMacd['diff'] *2/10 ;
	resultMacd['macd'] = 2 * (resultMacd['diff'] - resultMacd['dea']);
	
	return resultMacd

def MacdNomalCalc(lastresult,result):

	LastDayEma12 = lastresult['ema12'];
	LastDayEma26 = lastresult['ema26'];
	LastDayDea = lastresult['dea'];
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


def CheckBuySignal(Macd30Min,TimeNow,TimeInter):
	if Macd30Min[TimeNow-TimeInter]['macd'] < 0 :
		if Macd30Min[TimeNow]['macd'] > 0 :
			return 1
	else:
		return 0

def CheckSellSignal(Macd30Min,TimeNow,TimeInter):
	if Macd30Min[TimeNow-TimeInter]['macd'] > 0 :
		if Macd30Min[TimeNow]['macd'] < 0 :
			return 1
	else:
		return 0

def OpenBuyBill(AccountState,BuyBill,price,time):
	TextWriter('log.txt','OpenBuyTime:'+str(time));
	
	AccountState['BuyState']=1;
	buycoin = min(AccountState['CoinAmount']*0.5,0.5);
	AccountState['CoinAmount'] -= buycoin;
	BuyBill['OpenPrice'] = price;
	BuyBill['CoinAmount'] = buycoin;

	TextWriter('log.txt','OpenPrice:'+str(price));
	TextWriter('log.txt','CoinAmount:'+str(AccountState['CoinAmount']+BuyBill['CoinAmount']));
	TextWriter('log.txt','-'*25);

	return AccountState,BuyBill

def CloseBuyBill(AccountState,BuyBill,price,time):

	TextWriter('log.txt','CloseBuyTime:'+str(time));
	AccountState['BuyState']=0;
	
	closeprice = price;
	
	# boom
	if (closeprice/BuyBill['OpenPrice']-1)*20 <= -1:
		Gain = -BuyBill['CoinAmount'];
	else :
		Gain = (closeprice/BuyBill['OpenPrice']-1)*BuyBill['CoinAmount']*BuyBill['Rate'];
	TextWriter('log.txt','Gain:'+str(Gain));

	AccountState['CoinAmount'] += Gain+BuyBill['CoinAmount'];

	BuyBill['OpenPrice'] = 0;
	BuyBill['CoinAmount'] = 0;
	
	
	TextWriter('log.txt','ClosePrice:'+str(price));
	TextWriter('log.txt','CoinAmount:'+str(AccountState['CoinAmount']));
	TextWriter('log.txt','-'*25);

	return AccountState,BuyBill


def OpenSellBill(AccountState,SellBill,price,time):
	TextWriter('log.txt','OpenSellTime:'+str(time));
	
	AccountState['SellState']=1;
	buycoin = min(AccountState['CoinAmount']*0.5,0.5);
	AccountState['CoinAmount'] -= buycoin;
	SellBill['OpenPrice'] = price;
	SellBill['CoinAmount'] = buycoin;

	TextWriter('log.txt','OpenPrice:'+str(price));
	TextWriter('log.txt','CoinAmount:'+str(AccountState['CoinAmount']+SellBill['CoinAmount']));
	TextWriter('log.txt','-'*25);

	return AccountState,SellBill

def CloseSellBill(AccountState,SellBill,price,time):

	TextWriter('log.txt','CloseSellTime:'+str(time));
	AccountState['SellState']=0;
	
	closeprice = price;
	
	# boom
	if (1-closeprice/SellBill['OpenPrice'])*20 <= -1:
		Gain = -SellBill['CoinAmount'];
	else :
		Gain = (1-closeprice/SellBill['OpenPrice'])*SellBill['CoinAmount']*SellBill['Rate'];
	TextWriter('log.txt','Gain:'+str(Gain));

	AccountState['CoinAmount'] += Gain+SellBill['CoinAmount'];

	SellBill['OpenPrice'] = 0;
	SellBill['CoinAmount'] = 0;
	
	
	TextWriter('log.txt','ClosePrice:'+str(price));
	TextWriter('log.txt','CoinAmount:'+str(AccountState['CoinAmount']));
	TextWriter('log.txt','-'*25);

	return AccountState,SellBill






def TradeSimu():

	# read from csv
	result = CsvReader("data.csv");

	# modify result
	resultUse = modifyData(result);

	# get start time
	startTime = min(resultUse.keys());
	startTime = 1517496840;


	TimeNow = startTime;

	TimeInter = 60;
	Time15Min = 60*15;
	Time30Min = 60*30;
	Time1Hour = 60*60;
	Time4Hour = 60*60*4;
	Time1Day = 60*60*24;

	Macd30Min = {};
	Macd15Min = {};

	TimeInter = Time15Min;

	AccountState = {
		'CoinAmount' : 1,
		'SellState':0,
		'BuyState':0,
	}
	BuyBill= {
		'OpenPrice':0,
		'CoinAmount':0,
		'Rate':20
	}
	SellBill= {
		'OpenPrice':0,
		'CoinAmount':0,
		'Rate':20
	}

	while 1:
		if 	resultUse.has_key(TimeNow) == 0:
			break

		
		TimeInter = Time30Min;
		# macd calc
		if TimeNow == startTime:
			# start macd
			Macd30Min[TimeNow] = {};
			Macd30Min[TimeNow] = MacdHead(resultUse[TimeNow]);
			TextWriter('log30.txt',str(TimeNow)+str(Macd30Min[TimeNow]));
		elif TimeNow == startTime+TimeInter:
			Macd30Min[TimeNow] = {};
			Macd30Min[TimeNow] = MacdSeconline(Macd30Min[TimeNow-TimeInter],resultUse[TimeNow]);
			TextWriter('log30.txt',str(TimeNow)+str(Macd30Min[TimeNow]));
		elif (TimeNow - startTime)/TimeInter > 1 and (TimeNow-startTime)%TimeInter == 0:
			Macd30Min[TimeNow] = {};
			Macd30Min[TimeNow] = MacdNomalCalc(Macd30Min[TimeNow-TimeInter],resultUse[TimeNow]); 
			TextWriter('log30.txt',str(TimeNow)+str(Macd30Min[TimeNow]));


		TimeInter = Time15Min;
		# macd calc
		if TimeNow == startTime:
			# start macd
			Macd15Min[TimeNow] = {};
			Macd15Min[TimeNow] = MacdHead(resultUse[TimeNow]);
			TextWriter('log15.txt',str(TimeNow)+str(Macd15Min[TimeNow]));
		elif TimeNow == startTime+TimeInter:
			Macd15Min[TimeNow] = {};
			Macd15Min[TimeNow] = MacdSeconline(Macd15Min[TimeNow-TimeInter],resultUse[TimeNow]);
			TextWriter('log15.txt',str(TimeNow)+str(Macd15Min[TimeNow]));
		elif (TimeNow - startTime)/TimeInter > 1 and (TimeNow-startTime)%TimeInter == 0:
			Macd15Min[TimeNow] = {};
			Macd15Min[TimeNow] = MacdNomalCalc(Macd15Min[TimeNow-TimeInter],resultUse[TimeNow]); 
			TextWriter('log15.txt',str(TimeNow)+str(Macd15Min[TimeNow]));
		
		
		
		if len(Macd30Min.keys())>2 and Macd30Min.has_key(TimeNow):
			# open buy bill
			if CheckBuySignal(Macd30Min,TimeNow,Time30Min):
				if AccountState['BuyState']==0:
					(AccountState,BuyBill)=OpenBuyBill(AccountState,BuyBill,Macd30Min[TimeNow]['price'],TimeNow);
			# open sell bill
			if CheckSellSignal(Macd30Min,TimeNow,Time30Min):
				if AccountState['SellState']==0:
					(AccountState,SellBill)=OpenSellBill(AccountState,SellBill,Macd30Min[TimeNow]['price'],TimeNow);
			


		if len(Macd15Min.keys())>2 and Macd15Min.has_key(TimeNow):			
			# close buy bill
			if CheckSellSignal(Macd15Min,TimeNow,Time15Min):
				if AccountState['BuyState']==1:
					(AccountState,BuyBill)=CloseBuyBill(AccountState,BuyBill,Macd15Min[TimeNow]['price'],TimeNow)
			# close sell bill
			if CheckBuySignal(Macd15Min,TimeNow,Time15Min):
				if AccountState['SellState']==1:
					(AccountState,SellBill)=CloseSellBill(AccountState,SellBill,Macd15Min[TimeNow]['price'],TimeNow)







		if AccountState['CoinAmount']<0:
			print TimeNow;			
			break
		#print Macd30Min[TimeNow];
		

		TimeNow = TimeNow + 60;

	print AccountState['CoinAmount'];


	
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
    
	
