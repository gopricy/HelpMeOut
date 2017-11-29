import math
import random

# the student's status at time t
class Emotion:
	# 0 - 1 elemental
	def __init(self):
		self.anger = 0
		self.contempt = 0
		self.disgust = 0
		self.fear = 0
		self.happiness = 0
		self.sadness = 0
		self.surprise = 0
		# blablalba


class StudentStatus:
	# int number from 0 to 100, or -1 means not graded (first round)
	# grade
	# negative...neutral...positive continous or discrete
	# emotion
	# int number from a predefined set
	# knowladgeLevel
	# represents the maximum posible increasement of knowladge level
	# earningAbility

	def __init__(self, grade = -1, emotion = Emotion(), knowladgeLevel = 0, learningAbility = 0):
		self.grade = grade
		self.emotion = emotion
		self.knowladgeLevel = knowladgeLevel
		self.learningAbility = learningAbility

# the instructor's input at time t
class InstructorInput:
	# encourage, reward, punish, criticize, etc.
	behavior
	# level of knowladge the instructor provide
	teachingLevel

	def __init__(self, behavior = 0, teachingLevel = 0):
		self.behavior = behavior
		self.teachingLevel = teachingLevel

# independent variable that affects the student's status transfer
class StudentCharacter:
	# Big five 0-100
	# extroversion
	# neuroticism
	# openness
	# agreeableness
	# conscientiousness

	# result
	grit # ln(51 + 0.07E - 0.14N + 0.07A + 0.25C)
	expressive # ln(51 + 0.4E -0.2N)
	learning # ln(51 + 0.1A + 0.14O + 0.26C)
	def __init__(self, E=random.randint(0,100), N=random.randint(0,100), \
		O=random.randint(0,100), A=random.randint(0,100), C=random.randint(0,100)):

		self.extroversion = E
		self.neuroticism = N
		self.openness = O
		self.agreeableness = A
		self.conscientiousness = C

		self.grit = math.log(51 + 0.07*E - 0.14*N + 0.07*A + 0.25*C)
		self.expressive = math.log(51 + 0.4*E - 0.2*N)
		self.learning = math.log(51 + 0.1*A + 0.14*O + 0.26*C)

# records an entire teaching session
class Session:
	maximumRounds
	currentRound
	# student's turn or instructor's turn, 0 for instructor, 1 for student
	currentTurn
	# the number of statuses
	statusMemory
	# array of StudentStatus
	studentStatus = []
	# array of InstructorInput
	instructorInput = []
	# StudentCharacter
	studentCharacter

	def __init__(self, studentCharacter = StudentCharacter(), maximumRounds = 10, statusMemory = 0):
		self.maximumRounds = maximumRounds
		self.currentRound = 0
		self.currentTurn = 0
		self.studentCharacter = studentCharacter
		self.statusMemory = statusMemory

	def next(self, behavior, teachingLevel):
		instructorMove(behavior, teachingLevel)
		studentMove()
		if len(studentStatus) > 0:
			return studentStatus[-1].emotion

	def report(self):
		# blablabla

		######################################################################
		#		functions under this should be regarded as private			 #
		######################################################################

	def instructorMove(self, behavior, teachingLevel):
		if currentRound >= maximumRounds or currentTurn != 0:
			return
		instructorInput.append(InstructorInput(behavior, teachingLevel))
		currentTurn = 1

	def studentMove(self):
		if currentRound >= maximumRounds or currentTurn != 1:
			return
		studentStatus.append(getNextStudentStatus())
		currentTurn = 0
		currentRound += 1

	def getNextStudentStatus(self):
		# take the privious status, instructor input and character as input and generate the new status
		grade = updateGrade()
		emotion = updateEmotion()
		knowladgeLevel = updateKnowladge()
		learningAbility = updateAbility()

		return StudentStatus(grade, emotion, knowladgeLevel, learningAbility)

	def updateGrade(self):
		grade = -1
		if currentRound != 0:
			# TODO: add some logic that changes the grade
			# will be based on hard coded simple logic
		return grade

	def updateEmotion(self):
		emotion = Emotion()
		# TODO: add logic here to generate the current emotion
		# will be based on EMA
		return emotion

	def updateKnowladge(self):
		knowladgeLevel = 0
		# TODO: ...

		diff = self.instructorInput[self.currentTurn].teachingLevel - self.studentStatus[self.currentTurn].knowladgeLevel
		if diff <= 0:
			knowladgeLevel = self.studentStatus[self.currentTurn].knowladgeLevel
		else:
			knowladgeLevel += diff * self.studentStatus[self.currentTurn].learningAbility

		return knowladgeLevel

	def updateAbility(self):
		learningAbility = 0
		# TODO: ...
		return learningAbility