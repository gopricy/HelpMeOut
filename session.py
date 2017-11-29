import math
import random

feedback_map = ["Punishment", "Nothing", "Praise"]
# the student's status at time t
class Emotion:
    # 0 - 1 elemental
    def __init__(self):
        self.anger = 0
        self.contempt = 0
        self.disgust = 0
        self.fear = 0
        self.happiness = 0
        self.sadness = 0
        self.surprise = 0



class StudentStatus:
    # int number from 0 to 100, or -1 means not graded (first round)
    # grade
    # negative...neutral...positive continous or discrete
    # emotion
    # int number from a predefined set
    # knowledgeLevel
    # represents the maximum posible increasement of knowledge level
    # earningAbility

    def __init__(self, grade = -1, emotion = Emotion(), knowledgeLevel = 0, learningAbility = 0):
        self.grade = grade
        self.emotion = emotion
        self.knowledgeLevel = knowledgeLevel
        self.learningAbility = learningAbility

# the instructor's input at time t
class InstructorInput:
    # encourage, reward, punish, criticize, etc.
    # feedback
    # level of knowledge the instructor provide
    # teachingLevel

    def __init__(self, feedback = 0, teachingLevel = 0):
        self.feedback = feedback
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
    # grit # ln(51 + 0.07E - 0.14N + 0.07A + 0.25C)
    # expressive # ln(51 + 0.4E -0.2N)
    # learning # ln(51 + 0.1A + 0.14O + 0.26C)
    def __init__(self, E=random.randint(0,100), N=random.randint(0,100), \
        O=random.randint(0,100), A=random.randint(0,100), C=random.randint(0,100)):

        self.extroversion = E
        self.neuroticism = N
        self.openness = O
        self.agreeableness = A
        self.conscientiousness = C

        self.grit = math.log(51 + 0.07*E - 0.14*N + 0.07*A + 0.25*C)
        self.grit = (self.grit - math.log(51-14))/(math.log(51+7+7+25) - math.log(51-14))
        self.expressive = math.log(51 + 0.4*E - 0.2*N)
        self.expressive = (self.expressive - math.log(51-20))/(math.log(51+40) - math.log(51-20))
        self.learning = math.log(51 + 0.1*A + 0.14*O + 0.26*C)
        self.learning = (self.learning - math.log(51))/(math.log(51+10+14+26) - math.log(51))

# records an entire teaching session
class Session:
    # maximumRounds
    # currentRound
    # student's turn or instructor's turn, 0 for instructor, 1 for student
    # currentTurn
    # the number of statuses
    # statusMemory
    # array of StudentStatus
    # studentStatus = []
    # array of InstructorInput
    # instructorInput = []
    # StudentCharacter
    # studentCharacter

    def __init__(self, studentCharacter = StudentCharacter(), maximumRounds = 10, statusMemory = 0):
        self.maximumRounds = maximumRounds
        self.currentRound = 0
        self.currentTurn = 0
        self.studentCharacter = studentCharacter
        self.statusMemory = statusMemory
        self.instructorInput = []
        self.studentStatus = []
        self.randomFactor = 0

    def next(self, feedback, teachingLevel):
        self.instructorMove(feedback, teachingLevel)
        self.studentMove()
        self.randomFactor = random.randint(0, 10)
        if len(self.studentStatus) > 0:
            return self.studentStatus[-1].emotion

    def report(self):
        print '========================================================'
        print 'The character of the student is:'
        print 'extroversion: {}'.format(self.studentCharacter.extroversion)
        print 'neuroticism: {}'.format(self.studentCharacter.neuroticism)
        print 'openness: {}'.format(self.studentCharacter.openness)
        print 'agreeableness: {}'.format(self.studentCharacter.agreeableness)
        print 'conscientiousness: {}'.format(self.studentCharacter.conscientiousness)
        print '========================================================\n'

        print '========================================================'
        print 'The history of the teaching is:'
        for i in range(self.currentRound):
            print '--------------------------------------------------------'
            t_status = self.studentStatus[i]
            t_instruct = self.instructorInput[i]
            print 'Round: {}'.format(i)
            print 'Emotion: happiness: {}, sadness: {}, surprise: {}'.format(t_status.emotion.happiness,
                                                                             t_status.emotion.sadness,
                                                                             t_status.emotion.surprise)
            print 'Knowledge level: {}, ability: {}'.format(t_status.knowledgeLevel, t_status.learningAbility)
            print 'Grade: {}'.format(t_status.grade)
            print 'Your feedback: {}, your choice of difficulty: {}'.format(feedback_map[t_instruct.feedback],
                                                                            t_instruct.teachingLevel)
        print '========================================================\n'

        ######################################################################
        #		functions under this should be regarded as private			 #
        ######################################################################

    def instructorMove(self, feedback, teachingLevel):
        if self.currentRound >= self.maximumRounds or self.currentTurn != 0:
            return
        self.instructorInput.append(InstructorInput(feedback, teachingLevel))
        self.currentTurn = 1

    def studentMove(self):
        if self.currentRound >= self.maximumRounds or self.currentTurn != 1:
            return
        self.studentStatus.append(self.getNextStudentStatus())
        self.currentTurn = 0
        self.currentRound += 1

    def getNextStudentStatus(self):
        # take the privious status, instructor input and character as input and generate the new status
        grade = self.updateGrade()
        emotion = self.updateEmotion()
        knowledgeLevel = self.updateKnowledge()
        learningAbility = self.updateAbility()
        return StudentStatus(grade, emotion, knowledgeLevel, learningAbility)


    def updateGrade(self):
        t_grade = -1
        if self.currentRound != 0:
            # TODO: add some logic that changes the grade
            # will be based on hard coded simple logic
            diff = self.instructorInput[-1].teachingLevel - self.studentStatus[-1].knowledgeLevel
            if diff < 0:
                t_grade = 90
            elif diff <= 10:
                t_grade = 90 - (diff) * 4
            else:
                t_grade = 50 - (diff - 10) / 90.0 * 50
            if random.randint(0, 1):
                t_grade -= self.randomFactor
            else:
                t_grade += self.randomFactor
        else:
            return t_grade
        if t_grade > 100:
            t_grade = 100
        elif t_grade < 0:
            t_grade = 0
        return t_grade

    def updateEmotion(self):
        emotion = Emotion()
        if self.currentRound != 0:
            if self.studentStatus[-1].grade == -1:
                return emotion
            likelyhood = 1 - math.fabs(self.randomFactor) / 10.0
            desirabilityA = (self.studentStatus[-1].grade - 50) / 50.0
            desirabilityB = self.instructorInput[-1].feedback - 1
            desirability = desirabilityA * 0.5 + desirabilityB * 0.5

            if desirability >= 0:
                emotion.happiness = desirability
            else:
                emotion.sadness = -desirability

            if likelyhood < 0.2:
                emotion.surprise = 1 - likelyhood / 0.2
            else:
                emotion.surprise = 0

            emotion.happiness = emotion.happiness / (emotion.happiness + emotion.sadness + emotion.surprise)
            emotion.sadness = emotion.sadness / (emotion.happiness + emotion.sadness + emotion.surprise)
            emotion.surprise = emotion.surprise / (emotion.happiness + emotion.sadness + emotion.surprise)

            emotion.happiness *= self.studentCharacter.expressive
            emotion.sadness *= self.studentCharacter.expressive
            emotion.surprise *= self.studentCharacter.expressive

        return emotion


    def updateKnowledge(self):
        knowledgeLevel = 0
        # TODO: ...
        if self.currentRound != 0:
            diff = self.instructorInput[-1].teachingLevel - self.studentStatus[-1].knowledgeLevel
            if diff <= 0:
                knowledgeLevel = self.studentStatus[-1].knowledgeLevel
            else:
                knowledgeLevel += min(diff, self.studentStatus[-1].learningAbility)
        return knowledgeLevel

    def updateAbility(self):
        learningAbility = math.floor(self.studentCharacter.learning * 5 + 0.5)
        G = self.studentCharacter.grit
        # lAscalefact = 0
        if self.currentRound:
            if(self.studentStatus[-1].emotion.happiness > 0):
                x = self.studentStatus[-1].emotion.happiness
                bar = 0.5 + 0.5 * G
                if x <= bar:
                    lAscalefact = x/bar * G
                else:
                    lAscalefact = x/(bar-1) + G - bar/(bar-1)
            else:
                x = self.studentStatus[-1].emotion.sadness
                bar = 0.5 * G
                if x <= bar:
                    lAscalefact = x/(2*bar) * G
                else:
                    lAscalefact = x * (1 - G / 2) / (bar - 1) + G - 1 + (G / 2 - 1) / (bar - 1)
            learningAbility *= (1 + lAscalefact)

        return learningAbility
