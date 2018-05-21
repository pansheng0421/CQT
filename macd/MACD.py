from CsvRead import CsvReader
from CsvRead import CsvWriter


def modifyData(result,time):
	# read from csv
	result = CsvReader("data.csv");
	
	interSec = time;
	resultUse= {};
	for res in result:

		#resultUse[res] = result[res];
		resultUse[res] = {'price':result[res]}
		res = str(int(res) + interSec);
	
	return resultUse

def MacdCalc():
	
	result = {};
	resultUse = modifyData(result,60);
	#print resultUse
	print resultUse.keys()

	resultMacd = {};
	#resultMacd[0] ={'price':resultUse[0]} ;
	print resultMacd




if __name__=="__main__":   
	MacdCalc()
    
	
