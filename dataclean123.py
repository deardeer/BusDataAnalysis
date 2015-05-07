#encoding=utf-8
import csv
from time import gmtime, strftime
import datetime
from datetime import datetime
import time
import os, sys
import pdb


#delete the disorder list
def examRouteFromCSV(filename):
	LonList = []; 
	LatList = [];
	print('begin exam' + filename);
	with open(filename, 'rb') as f:
		reader = csv.reader(f, delimiter=',');
		for row in reader:
			print(row);
			print(row[5]);
			sDateTime = row[5];
			print(sDateTime);
			# date = datetime.strptime(sDateTime, "%Y-%m-%d %H:%M:%S");
			# print(date);
			DateTime = datetime.strptime(sDateTime, "%Y-%m-%d %H:%M:%S"); 
			# print(DateTime.time);
			break;

def clean(filename):
	LonList = []; 
	LatList = [];
	liNewRecord = [];
	fMinLon = 115;
	fMaxLon = 118;
	fMinLat = 39; 
	fMaxLat = 42;
	print('begin clean' + filename);
	iReadIndex = 0;
	iCurrentDir = -1;
	liRemoveBeginEndIndex = [];

	with open(filename, 'rb') as f:
		reader = csv.reader(f, delimiter=',');
		# iLineNum = sum(1 for row in reader);
		# print "linenum " + str(iLineNum);		
		dataList = list(f)
		# for row in reader:
		print(" len(dataList) - 1 " + str(len(dataList) - 1));
		for i in range(0, len(dataList)):
			i = iReadIndex;
			
			if(i >= len(dataList) - 1):
				break;

			rowStr = dataList[i];
			row = rowStr.split(",");

			# if(i == 593):
			# 	print('593 ' + rowStr);

			# print('index ' + str(iIndex) + ' iReadIndex ' + str(iReadIndex));
			iThisDir = int(row[4]);
			if(iCurrentDir == -1):
				iCurrentDir = iThisDir;

			sDateTime = row[5];
			DateTime = datetime.strptime(sDateTime, '%Y-%m-%d %H:%M:%S'); 
			
			Lon = float(row[6]);
			Lat = float(row[7]);
			#0. check for date
			bDelete =  False;
			if(DateTime.day != 2):
				print('1');
				bDelete = True;
			#1. check for lat,lon 
			if(Lon < fMinLon or Lon > fMaxLon):
				print('2 ' + str(Lon));
				bDelete = True;
			if(Lat < fMinLat or Lat > fMaxLat):
				print('3 ' + str(Lat));
				bDelete = True;
			#2. check for order
			iPreIndex = i - 1;
			if(iPreIndex >= 0):
				preRowStr = dataList[iPreIndex]; 
				preRow = preRowStr.split(",");
				# print('======preRow' + str(iPreIndex) + ', ' + preRow);
				iPreDir = int(preRow[4]);
				if(iPreDir == iThisDir):
					preDateTime = preRow[5];
					preDateTime = datetime.strptime(preDateTime, '%Y-%m-%d %H:%M:%S');
					if(preDateTime > DateTime):
						print('4');
						bDelete = True;
			#if delete
			# print('bDelete ' + str(bDelete));
			if(bDelete == True):
				iBeginRowIndex = i;
				iEndRowIndex = i;
				paBeginEndIndex = findDirBlock(i, iThisDir, dataList);
				iBeginRowIndex = paBeginEndIndex[0];
				iEndRowIndex = paBeginEndIndex[1];
				liRemoveBeginEndIndex.append((iBeginRowIndex, i, iEndRowIndex, True));
				print("i = ", i);
				# print("=== Begin, End " + str(iBeginRowIndex) + ' , ' + str(iEndRowIndex));
				iReadIndex = iEndRowIndex + 1;
				continue;
			else:
				iReadIndex += 1;
				# liNewRecord.append(dataList[iIndex]);
				# print(row);	
			# print('XXX iReadIndex ' + str(iReadIndex) + " iIndex " + str(iIndex));	

	print('end clean' + filename);

	# for i in range(0, len(liRemoveBeginEndIndex)):
	# 	print('Remove ' + str(liRemoveBeginEndIndex[i][0]) + ' , ' + str(liRemoveBeginEndIndex[i][1]));

	# with open(filename, 'rb') as f:
	# 	reader = csv.reader(f, delimiter=',');
	# 		iIndex = 0;
	# 		iRemoveReaderIndex = 0;
	# 		iRemoveBeginIndex = liRemoveBeginEndIndex[iRemoveReaderIndex][0];
	# 		iRemoveEndIndex = liRemoveBeginEndIndex[iRemoveReaderIndex][1];
	# 	for row in reader:

	# 		if(iIndex)
	# 		iIndex += 1;

	return liRemoveBeginEndIndex;

def getCleanData(liRemoveBeginEndIndex):
	cleanedRowList = [];
	with open(filename, 'rb') as f:
		reader = csv.reader(f, delimiter=',');
		iErrorPair = len(liRemoveBeginEndIndex);
		if iErrorPair == 0:
			#not error
			for row in reader:
				cleanedRowList.append(row);
		else:
			iReaderIndex = 0;
			iErrorReaderIndex = 0;
			currentBeginEndIndex = [liRemoveBeginEndIndex[iErrorReaderIndex][0], liRemoveBeginEndIndex[iErrorReaderIndex][2]];

			iMultiTime = 1;
			Base = iMultiTime * 2;
			iPreRouteDir = -1;

			print (str(currentBeginEndIndex[0]) + ', ' + str(currentBeginEndIndex[1]));
			for row in reader:
				if (iReaderIndex == currentBeginEndIndex[1] + 1):
					if(iReaderIndex == currentBeginEndIndex[1] + 1):
						iErrorReaderIndex += 1;
						if(iErrorReaderIndex < len(liRemoveBeginEndIndex)):
							currentBeginEndIndex = [liRemoveBeginEndIndex[iErrorReaderIndex][0], liRemoveBeginEndIndex[iErrorReaderIndex][2]];
						else:
							currentBeginEndIndex = [-1, -1];
					iMultiTime += 1;
					Base = iMultiTime * 2;

				if(iReaderIndex < currentBeginEndIndex[0] or iReaderIndex > currentBeginEndIndex[1]):
					iCurrentRouteDir = int(row[4]);
					if(iPreRouteDir != iCurrentRouteDir):
						iMultiTime += 1;
						Base = iMultiTime * 2;
					iPreRouteDir = iCurrentRouteDir;
					iCurrentRouteDir += Base;
					row[4] = str(iCurrentRouteDir);
					cleanedRowList.append(row);
				
				iReaderIndex += 1;
	return cleanedRowList;

def findDirBlock(iIndex, iCurrentDir, dataList):
	iBeginRowIndex = iIndex;
	iEndRowIndex = iIndex;
	for iBeginRowIndex in xrange(iIndex, 0, -1):
		iTempPreDir = getDirofRow(iBeginRowIndex, dataList);
		if iTempPreDir == -1:
			break;
		if(iTempPreDir == iCurrentDir):
			continue;
		else:
			iBeginRowIndex += 1;
			break;
	while True:
		iTempAftDir = getDirofRow(iEndRowIndex, dataList);
		if iTempAftDir == -1:
			break;
		if(iTempAftDir == iCurrentDir):
			iEndRowIndex += 1;
			continue;
		else:
			iEndRowIndex -= 1;
			break;
	print(" iBeginRowIndex " + str(iBeginRowIndex) + " iEndRowIndex " \
		+ str(iEndRowIndex) + " iCurrentIndex " + str(iIndex));

	return (iBeginRowIndex, iEndRowIndex);


def getDirofRow(iRowIndex, dataList):
	iPreDir = -1;
	if(iRowIndex >= len(dataList)):
		print('iRowIndex = ' + str(iRowIndex));
		return iPreDir;
	preRowString = dataList[iRowIndex];
	preRow = preRowString.split(',');
	# print('get row' + preRow);
	iPreDir = int(preRow[4]);
	return iPreDir;


def writetoCSV(filename, extractData):
	with open(filename, 'wb') as csvfile:
		writer = csv.writer(csvfile, delimiter = ',');
		for row in extractData:
			writer.writerow(row);

dir = './20130202_BFD/'
filename = dir + 'extractedVehicle.csv';
wFileName = dir + 'extractedVehicle_cleaned.csv';
liCleanBEIndex = clean(filename);	

liCleanData = getCleanData(liCleanBEIndex);

print('clean data pair ' + str(len(liCleanBEIndex)));

# examRouteFromCSV(filename);
writetoCSV(wFileName, liCleanData);	
