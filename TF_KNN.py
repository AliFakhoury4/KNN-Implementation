import numpy as np
import pandas as pd
import sys

#returns the columns of the dataset along with the index to the name for the column
def getColumns(inFile, delim="\t", header=True):
	cols = {}
	indexToName = {}
	for lineNum, line in enumerate(inFile):
		if lineNum == 0:
			headings = line.split(delim)
			i = 0
			for heading in headings:
				heading = heading.strip()
				if header:
					cols[heading] = []
					indexToName[i] = heading
				else:
					# in this case the heading is actually just a cell
					cols[i] = [heading]
					indexToName[i] = i
				i += 1
		else:
			cells = line.split(delim)
			i = 0
			for cell in cells:
				cell = cell.strip()
				cols[indexToName[i]] += [cell]
				i += 1

	return cols, indexToName

#returns the sequences from the dataset
def readSequences(fileName):
	dataset = open(fileName, 'r');

	stringArray = []

	for line in dataset:
		lineArray = line.split()
		stringArray.append(lineArray[1])

	return stringArray

#returns the columns and indexes according to the filename
def readOutputVector(fileName):
	output = open(fileName, 'r')
	cols, indexToName = getColumns(output)
	output.close()

	return cols, indexToName;

#returns distance between two different strings
def compareTwoStrings(firstString, secondString):
	differenceValue = 0
	for x,y in zip(firstString, secondString):
		if x!=y:
			differenceValue += 1
	return differenceValue

#returns the distance between a single string and every other string in an array of strings
def createDistanceVector(string, array):
	distanceVector = []

	for elem in array:
		distanceDifference = compareTwoStrings(string, elem)
		distanceVector = np.append(distanceVector, compareTwoStrings(string, elem))

	return distanceVector;


#returns the closest K strings indexes by sorting the list and getting the indexes of the first k elements
def getClosestKIndexes(k, distanceVector):
	sortedIndexes = np.argsort(distanceVector)
	firstKIndexes = sortedIndexes[:k]

	return firstKIndexes

#returns the average of the closest K strings
def getAverageOfKStrings(KIndexes, sizeOfOutputVector):
	averageVector = []

	columns, indexToName = readOutputVector(outputFile)

	indexes = []

	for index in KIndexes:
		indexes.append(indexToName[index])

	for x in range(sizeOfOutputVector):
		sum = 0
		for index in range(len(indexes)):
			sum += float(columns[indexes[index]][x])


		average = sum/len(KIndexes)
		averageVector = np.append(averageVector, round(average, 4))	

	return averageVector

#returns the sequence of strings after splitting them from their name
def readSequences(fileName):
	dataset = open(fileName, 'r');

	stringArray = []

	for line in dataset:
		lineArray = line.split()
		stringArray.append(lineArray[1])

	return stringArray

#returns an array of the unseen data
def readUnseenData(fileName):
	unseenData = open(fileName, 'r')

	sequenceNames = []
	sequenceStrings = []

	for line in unseenData:
		lineArray = line.split()
		sequenceNames.append(lineArray[0])
		sequenceStrings.append(lineArray[1])

	return sequenceNames, sequenceStrings

#performs KNN on the unseen data, and saves results in a csv file
def KnnOnUnseenData(unseenDataNames, unseenDataSequence, k):
	dataset = readSequences(sequencesFile)

	allAverage = []

	for index, sequence in enumerate(unseenDataSequence):
		distanceVector = createDistanceVector(sequence, dataset)
		closestKIndexes = getClosestKIndexes(k, distanceVector)
		averageOutput = getAverageOfKStrings(closestKIndexes, 32896)

		outputArray = []
		
		for i in range(len(averageOutput)):
			outputArray.append(float(averageOutput[i]))

		allAverage.append(outputArray)

	dictionary = dict(zip(unseenDataNames, allAverage))

	df = pd.DataFrame(dictionary)
	df.to_csv("unseenOutput.csv")


sequencesFile = sys.argv[1]
outputFile = sys.argv[2]
unseenDataFile = sys.argv[3]

dataset = readSequences(sequencesFile)
unseenDataNames, unseenDataSequence = readUnseenData(unseenDataFile)

k = 3

KnnOnUnseenData(unseenDataNames, unseenDataSequence, k)