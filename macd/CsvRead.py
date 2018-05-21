import csv


		
def CsvReader(file):
	
	csvFile = open(file, "r")
	reader = csv.reader(csvFile)

	
	result = {}
	for item in reader:
	    
	    result[item[0]] = item[1]

	csvFile.close()
	return result

def CsvWriter(file,result):

	fileHeader = ["data", "price"];

	csvFile = open(file, "w")
	writer = csv.writer(csvFile);

	writer.writerow(fileHeader);

	for item in result:
		res = [item , result[item]];
		writer.writerow(res);

	csvFile.close();
	pass 