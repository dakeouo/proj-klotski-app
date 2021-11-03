# 數字華容道 Klotski
import keyboard
import random
from datetime import datetime
import time

random.seed(datetime.now())
level = 4
ARR_matrixSize = [3, 4, 5, 6, 7] #方陣大小
ARR_quizMove = [15, 30, 60, 105, 165]
matrixSize = ARR_matrixSize[level] #方陣大小
quizMove = ARR_quizMove[level]
moveTimes = 0
QUIZ_Matrix = []
GOAL_Matrix = []

def swap(a, b):
	t=a
	a=b
	b=t
	return a, b

def arraySame(arr_a, arr_b):
	if len(arr_a) != len(arr_b):
		return False
	for i in range(len(arr_a)):
		if arr_a[i] != arr_b[i]:
			return False
	return True

def num2FormatStr(digits, prefix, num): #數字轉含前綴字串
	result = str(num)
	while len(result) < digits:
		result = "%s%s" %(prefix, result)
	return result

def createMatrix(m_size): #建立華容道
	global QUIZ_Matrix, GOAL_Matrix

	num = m_size*m_size
	for i in range(1,num):
		GOAL_Matrix.append(i)
	GOAL_Matrix.append(0)
	QUIZ_Matrix = GOAL_Matrix.copy()

def moveMatrix(action, matrix): #移動華容道方塊
	global matrixSize
	empty = matrix.index(0)
	emptyPos = [int(empty/matrixSize), empty%matrixSize]
	target = -1
	if action == "up":
		if emptyPos[0]+1 < matrixSize:
			target = ((emptyPos[0]+1)*matrixSize)+emptyPos[1]
	elif action == "down":
		if emptyPos[0]-1 >= 0:
			target = ((emptyPos[0]-1)*matrixSize)+emptyPos[1]
	if action == "left":
		if emptyPos[1]+1 < matrixSize:
			target = (emptyPos[0]*matrixSize)+emptyPos[1]+1
	elif action == "right":
		if emptyPos[1]-1 >= 0:
			target = (emptyPos[0]*matrixSize)+emptyPos[1]-1
	if target != -1:
		matrix[empty], matrix[target] = swap(matrix[empty], matrix[target])
		return True, matrix
	else:
		return False, matrix

def makeQuizMatrix(move, matrix):
	ACT = ['up', 'down', 'left', 'right']
	RM = ['down', 'up', 'right', 'left']
	action = ACT.copy()
	while move != 0:
		idx = int(random.random()*len(action))
		mov = action[idx]
		success, matrix = moveMatrix(mov, matrix)
		if success:
			move -= 1
			action = ACT.copy()
			rmAction = RM[action.index(mov)]
			action.pop(action.index(rmAction))
		else:
			action.pop(idx)
	return matrix

def showMatrix(matrix): #顯示華容道
	global matrixSize
	digits = len(str(max(matrix)))
	bordlen = (digits+3)*matrixSize+1
	bordLine = "" # 橫向分隔線
	for i in range(bordlen):
		bordLine += '-'

	for i in range(len(matrix)):
		if i%matrixSize == 0:
			print(bordLine)
			print('|', end="")
		if matrix[i] != 0:
			numstr = num2FormatStr(digits, "0", matrix[i])
		else:
			numstr = num2FormatStr(digits, " ", "")
		if i%matrixSize == matrixSize-1:
			print(" %s |" %(numstr))
		else:
			print(" %s |" %(numstr), end="")
	print(bordLine)

createMatrix(matrixSize)
print("================================")
print("==  Welcome to play Klotski!  ==")
print("================================")
print("Use 'Arrow keys' to moving block")
print("  Press 'q' to leave this game. ")
print("================================")
QUIZ_Matrix = makeQuizMatrix(quizMove, QUIZ_Matrix)
showMatrix(QUIZ_Matrix)
startTime = datetime.now()
isFinish = True
while not arraySame(QUIZ_Matrix, GOAL_Matrix):
	key = keyboard.read_key()
	success, QUIZ_Matrix = moveMatrix(key, QUIZ_Matrix)
	if success:
		moveTimes += 1
	print("Moves:", moveTimes)
	showMatrix(QUIZ_Matrix)

	if keyboard.read_key() == "q":
		isFinish = False
		break
endTime = datetime.now()
time_s = (endTime - startTime).seconds
time_ms = (endTime - startTime).microseconds
fullsec = time_s + float(str("0.%d" %(time_ms)))
if isFinish:
	print("Congratulation! you move %d times to finish this game." %(moveTimes))
else:
	print("You are not finish yet!")
print('Spend Time (sec):', "%.3fms" %(fullsec))