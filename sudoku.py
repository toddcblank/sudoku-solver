

board = [
[ 9,-1,-1, 8,-1, 2, 4,-1,-1],
[-1,-1,-1,-1,-1,-1,-1,-1, 6],
[ 5,-1, 4,-1, 9,-1,-1,-1, 3],
[-1,-1,-1, 2,-1,-1,-1, 4,-1],
[-1, 5,-1,-1,-1,-1, 7,-1,-1],
[-1, 7,-1,-1,-1, 6, 9,-1, 8],
[-1, 2,-1,-1, 1, 4,-1, 6,-1],
[-1,-1, 6, 5,-1,-1,-1,-1, 9],
[-1,-1,-1,-1, 8,-1,-1,-1,-1]
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
		updateMade = updateMade or updateBasedOnAvailableRow(i)

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
				print "found only one square in set for %d" % i
				updateMade = True
				nodes[candidateSquare] = []
				nodes[candidateSquare].append(i)
	
	return updateMade

def updateBasedOnAvailableRow(row):
	updateMade = False
	#updates based on a number only being available to one square in the row
	for i in range(1,10):
		availableSquares = 0
		columnIndex = 0
		candidateSquare = 0
		for column in possibilities[row]:
			if i in column:
				availableSquares += 1
				candidateSquare = columnIndex	
			columnIndex += 1

		if availableSquares == 1:
			if board[row][candidateSquare] == -1:
				board[row][candidateSquare] = i
				updateMade = True

	return updateMade

def updateAllColumns():
	updateMade = False
	for i in range(0,9):
		#updateMade = updateMade or updateBasedOnAvailableColumn(i)
		updateMade = updateBasedOnAvailability(getSetForColumn(i)) or updateMade

	return updateMade

def updateBasedOnAvailableColumn(column):
	updateMade = False

	for i in range(1,10):
		availableSquares = 0
		rowIndex = -1
		candidateSquare = 0
		for row in possibilities:
			rowIndex += 1
			if i in row[column]:
				availableSquares += 1
				candidateSquare = rowIndex

		if availableSquares == 1:
			if board[candidateSquare][column] == -1:
				board[candidateSquare][column] = i
				updateMade = True

	return updateMade

def updateAllSections():
	updateMade = False
	for i in range(0,3):
		for j in range(0,3):
			updateMade = updateMade or updateBasedOnAvailableSection(i,j)
	return updateMade

def updateIteration():
	updatesMade = removePossibleValuesBasedOnBoard() 
	updatesMade = updateAllSections() or updatesMade 
	updatesMade = updateAllRows() or updatesMade
	updatesMade = updateAllColumns() or updatesMade
	updatesMade = updateBoardBasedOnPossibleValues() or updatesMade

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

def findPairsInRows():
	rowindex = -1
	for row in possibilities:
		rowindex += 1
		uniquePossibilities = []
		for cell in row:
			if cell in uniquePossibilities:
				print "found cell that is duplicated in row %d" % rowindex
				print cell
			else:
				uniquePossibilities.append(cell)

def updateBasedOnAvailableSection(xSection, ySection):
	
	updateMade = False

	#updates based on a number only being available to 1 square in the section
	for i in range(1,10):
		rowStart = ySection * 3
		availableSquares = 0
		candidateSquareY = ySection * 3	
		candidateSquareX = xSection * 3
		rowIndex = ySection * 3
		for row in possibilities[ySection * 3:ySection * 3 + 3]:
			columnIndex = xSection * 3
			for column in row[xSection * 3:xSection *3 + 3]:
				if i in column:
					availableSquares += 1
					candidateSquareY = rowIndex
					candidateSquareX = columnIndex
				columnIndex += 1		
			rowIndex += 1

		if availableSquares == 1:
			if board[candidateSquareY][candidateSquareX] == -1:
				updateMade = True
				board[candidateSquareY][candidateSquareX] = i

	return updateMade	

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

