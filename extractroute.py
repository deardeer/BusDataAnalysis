import csv
from time import gmtime, strftime
import datetime
import time
import os, sys

#extract records from bus data

#read bus csv
def extractRouteFromCSV(filename, routeId, liResultRecord):
	print('begin extract' + filename);
	bFound = False;
	bPrint = True;
	with open(filename, 'rb') as f:
		reader = csv.reader(f, delimiter=',');
		for row in reader:
			iThisRouteId = getRouteId(row);
			if(iThisRouteId == routeId):
				if(bPrint == True):
					# print(row);
					bPrint = False;
				liResultRecord.append(row);
				bFound = True;
	print('end extract' + filename);
	# for i in range(0, 1):
	# 	print(liResultRecord[i]);
	return bFound;

def getRouteId(row):
	Attri3 = row[3];
	if Attri3.isdigit():
		Attri3 = int(Attri3);
	return Attri3;

def getAllFileName(dir):
	liFileName = [];
	files = os.listdir(dir);
	for f in files:
		liFileName.append(f);
	return liFileName;

def writetoCSV(filename, extractData):
	with open(filename, 'wb') as csvfile:
		writer = csv.writer(csvfile, delimiter = ',');
		for row in extractData:
			writer.writerow(row);

iFindRouteId = 676;
dir = './20130202_BUS/'
liFileName = getAllFileName(dir);
liFoundFileName = [];
liAllFoundRecord = [];
for f in liFileName:
	FileName = dir + f;
	liFoundRecord = [];
	bFound = extractRouteFromCSV(FileName, iFindRouteId, liAllFoundRecord);

print('Found file num = ' + str(len(liFoundFileName)));
for f in liFoundFileName:
	print('Found in file: ' + f);

for i in range(0, 10):
	print(liAllFoundRecord[i]);

writeFN = dir + 'extractedRoute' + str(iFindRouteId) + '.csv';
writetoCSV(writeFN, liAllFoundRecord);

