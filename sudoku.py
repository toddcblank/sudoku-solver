
#"Hard" from Hemispheres, June 2013
#board = [
#[-1,-1, 3,-1, 4,-1, 5,-1,-1],
#[-1,-1,-1, 9,-1,-1,-1,-1,-1],
#[-1, 4,-1,-1, 6, 8,-1,-1,-1],
#[-1, 2,-1,-1, 8,-1, 3, 9,-1],
#[ 1,-1, 8,-1, 2,-1,-1,-1,-1],
#[ 5,-1,-1,-1,-1, 6,-1,-1,-1],
#[-1, 5,-1,-1, 3, 1,-1,-1, 8],
#[-1, 8,-1,-1, 5,-1,-1,-1, 3],
#[-1,-1, 4,-1,-1, 7,-1,-1, 6],
#]

#3. Medium from Hemispheres, June 2013
board = [
[-1, 2,-1,-1,-1,-1,-1, 8,-1],
[ 4,-1, 7,-1,-1,-1,-1,-1,-1],
[ 6,-1,-1, 5,-1, 1,-1,-1,-1],
[-1,-1, 1, 2,-1, 8,-1,-1,-1],
[-1, 9,-1,-1,-1, 4, 3,-1,-1],
[-1,-1,-1,-1, 9, 3, 8,-1,-1],
[-1,-1, 9,-1, 3, 6,-1,-1, 7],
[-1,-1, 8,-1,-1, 9,-1,-1, 2],
[-1,-1,-1, 4,-1,-1,-1,-1,-1],
]

def removeValueFromSet(value, nodes):
	for node in nodes:
		if len(node) == 1:
			continue
		if value in node:
			node.remove(value)	
	
def removePossibleValuesBasedOnBoard():
	updated = False
	for y in range(0, 9):
		for x in range(0, 9):
			value = board[y][x]
			
			if(value != -1):
				possibilities[y][x] = [value]
				updated = removeValueFromSet(value, getSetForRow(y)) or updated
				updated = removeValueFromSet(value, getSetForColumn(x)) or updated
				updated = removeValueFromSet(value, getSetForSection(int(x/3), int(y/3))) or updated

	return updated

def updateBoardBasedOnPossibleValues():
	update = False
	rowIndex = 0;
	for row in possibilities:
		columnIndex = 0;
		for column in row:
			if len(column) == 1:
				value = board[rowIndex][columnIndex]
				if(value == -1):
					update = True
					board[rowIndex][columnIndex] = column[0]
			columnIndex += 1
		rowIndex += 1
	return update

def updateAllRows():

	updateMade = False
	for i in range(0,9):
		updateMade = updateBasedOnAvailability(getSetForRow(i)) or updateMade

	return updateMade

def updateBasedOnAvailability(nodes):
	updateMade = False
	for i in range(1,10):
		availableSquares = 0
		index = 0
		candidateSquare = 0
		for node in nodes:
			if i in node:
				availableSquares += 1
				candidateSquare = index
			index += 1

		if availableSquares == 1:
			if len(nodes[candidateSquare]) > 1:
				updateMade = True
				del nodes[candidateSquare][0:]
				nodes[candidateSquare].append(i)
	
	return updateMade

def updateAllColumns():
	updateMade = False
	for i in range(0,9):
		updateMade = updateBasedOnAvailability(getSetForColumn(i)) or updateMade

	return updateMade

def updateAllSections():
	updateMade = False
	for i in range(0,3):
		for j in range(0,3):
			updateMade = updateBasedOnAvailability(getSetForSection(i,j))
	return updateMade

def updateIteration():
	updatesMade = removePossibleValuesBasedOnBoard() 
	updatesMade = updateAllSections() or updatesMade 
	updatesMade = updateAllRows() or updatesMade
	updatesMade = updateAllColumns() or updatesMade
	updatesMade = updateBoardBasedOnPossibleValues() or updatesMade
	updatesMade = findEqualNodes() or updatesMade

	printBoard()

	return updatesMade

def updateUntilNoChange():
	while(updateIteration()):
		pass

def getSetForRow(row):
	return possibilities[row]

def getSetForColumn(column):
	#should be a better way to do this
	columns = []
	for row in possibilities:
		columns.append(row[column])

	return columns

def getSetForSection(xSection, ySection):
	#should be a better way to do this too
	nodes = []
	for row in possibilities[ySection * 3:ySection * 3 + 3]:
		for column in row[xSection * 3:xSection *3 + 3]:
			nodes.append(column)
	
	return nodes


def findEqualNodes():
	update = False
	for i in range(0,9):
		update = findPairsInNodes(getSetForRow(i)) or update
		update = findPairsInNodes(getSetForColumn(i)) or update

	for i in range(0,3):
		for j in range(0,3):
			update = findPairsInNodes(getSetForSection(i,j)) or update

	return update

def findPairsInNodes(nodes):
	update = False
	index = 0
	for cell in nodes:
		if len(cell) > 1 and nodes.count(cell) == len(cell):
			#remove values from non-equal cellsA
			for checkCell in nodes:
				if checkCell == cell:
					continue
				else:
					for value in cell:
						if value in checkCell:
							update = True
							checkCell.remove(value)

	return update

def possibleValues(y, x):
	if(board[x][y] != -1):
		return [board[x][y]]

	return range(1, 10)

def printBoard():

	rowIndex = 0;
	for row in board:
		if rowIndex % 3 == 0:
			print "-------------"
		rowStr = ""
		columnIndex = 0
		for column in row:
			if columnIndex % 3 == 0:
				rowStr += "|"
			
			if board[rowIndex][columnIndex] == -1:
				rowStr += " "
			else:
				rowStr += str(board[rowIndex][columnIndex])

			columnIndex = columnIndex + 1
		
		rowStr += "|"
		print rowStr
		rowIndex = rowIndex + 1

	print "-------------"

printBoard()
possibilities = []

for x in range(0,9):
	possibilities.append([])
	for y in range(0,9):
		possibilities[x].append([])
		possibilities[x][y] = possibleValues(y,x)

