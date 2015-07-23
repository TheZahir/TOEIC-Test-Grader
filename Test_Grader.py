# Test Grader takes a .py file with a TOEIC test answer key 
# and the answers from an arbitrary number of students and 
# scores the answers and plots the results according to Q type.
from decimal import *
from pylab import *
getcontext().prec = 2

# this line imports the TOEIC answer key and test scores as a module.
# change this for different tests.
import TOEIC_Practice_Test_1 as test

students = {}
studentAnswers = {}
studentPercentage = {}
classScore = {}
answerKey = {}

# defining the 4 different sections of the TOEIC test
photoQs = {'title' : 'Photo Questions', 'nums' : range(1, 10+1), 'corr' : [], 'incorr' : [], 'classPct' : 0}
responseQs = {'title' : 'Response Questions', 'nums' : range(11, 40+1), 'corr' : [], 'incorr' : [], 'classPct' : 0}
convQs = {'title' : 'Conversation Questions', 'nums' : range(41, 70+1), 'corr' : [], 'incorr' : [], 'classPct' : 0}
singleSpeakerQs = {'title' : 'Single Speaker Questions', 'nums' : range(71, 100+1), 'corr' : [], 'incorr' : [], 'classPct' : 0}

# this is for the plotter function to reference
totalQs = [photoQs, responseQs, convQs, singleSpeakerQs]

def answers_to_dict(name, answerList):
	answerListLen = len(answerList)
	name = {i+1 : answerList[i] for i in range(answerListLen)}
	return name

def get_answer_key_and_answers():
	#correctAnswers = input("First, the answer key: \nEnter the correct answers. \n")
	correctAnswers = test.correctanswers
	correctAnswers = list(''.join(correctAnswers.upper().split()))
	
	global answerKey
	answerKey = answers_to_dict("answerKey", correctAnswers)
	
	for student in test.studentList:
		name = student
		lowerName = "".join(name.lower())
		
		answers = test.studentList[student]
		answers = ''.join(answers.upper().split())
		
		students[lowerName] = name
		studentAnswers[lowerName] = answers_to_dict(lowerName, answers)
	
	"""
	addStudents = True
	
	while addStudents:
		name = input('Enter the student\'s name. Type \'none\' to finish. \n')
		lowerName = "".join(name.lower())
		if lowerName == 'none':
			addStudents = False
			break
		else:
			answers = input('Enter the student\'s answers. \n')
			answers = ''.join(answers.upper().split())
			students[lowerName] = name
			studentAnswers[lowerName] = answers_to_dict(lowerName, answers)
	"""
			
def print_scores(student):
	name = students[student]
	print('%s\'s score is:' % name, studentPercentage[student], '%')
	print('%s\'s answers were: ' % name)
	count = 1
	for answer in studentAnswers[student]:
		if count < 10:
			print('   ', count, ': ', studentAnswers[student][answer])
		elif count <100:
			print('  ', count, ': ', studentAnswers[student][answer])
		else:
			print(' ', count, ': ', studentAnswers[student][answer])
		count += 1

def grade_answers(student):
	studentScore = 0
	for n in range(1, totalAnswers+1):
		if studentAnswers[student][n] == answerKey[n]:
			classScore[n]['corr'] += 1
			studentScore += 1
		else:
			classScore[n]['incorr'] += 1
			studentAnswers[student][n] = studentAnswers[student][n] + ' X'
	studentPercentage[student] = int((studentScore / len(answerKey)) * 100)
	
def arrange_scores_by_Q_type():	
	for category in totalQs:
		classCorr = 0
		for num in category['nums']:
			category['corr'].append(classScore[num]['corr'])
			category['incorr'].append(classScore[num]['incorr'])
			classCorr += classScore[num]['corr']
		category['classPct'] = (classCorr/(len(category['nums'])*len(students)))*100

def plot_by_question_type(qType):
    fig = figure()
    ax = fig.add_axes([0.5,0.5,1.2,1])
    n = len(qType['nums'])
    X = np.arange(n)
    correct = np.array(qType['corr'])
    incorrect = np.array(qType['incorr'])

    ax.bar(X, +correct, facecolor='#00FF6A', edgecolor='#00FF6A')
    ax.bar(X, -incorrect, facecolor='#FF4F38', edgecolor='#FF4F38')

    for x,y in zip(X,correct):
        ax.text(x+0.4, y+0.25, '%i' % y, ha='center', va='bottom')
    
    for x,y in zip(X,incorrect):
        ax.text(x+0.4, -y-0.25, '%i' % y, ha='center', va='top')
    
    count = 0
    for num in qType['nums']:
        ax.text(count+0.4, -13.5, '%i' % num, ha='center', va='top')
        count += 1
    
    title(qType['title'] + ' (%.2f' % qType['classPct'] + '%)', fontsize=22)
    xlabel('Question Numbers', fontsize=16)
    ylabel('Incorrect |   Correct', fontsize=16)
    
    xlim(-.25,n), xticks([])
    ylim(-15,+15), yticks([])
    savefig(qType['title'] + ' barchart.png', dpi=500, bbox_inches='tight')
        
    show()		
	
get_answer_key_and_answers()

totalAnswers = len(answerKey)

# set up the dictionary to track total correct and incorrect answers for the class
for n in range(1, totalAnswers+1):
	classScore[n] = {'corr': 0, 'incorr': 0}

# grade each student's test and send scores to the class score dict
for student in students:
	grade_answers(student)

arrange_scores_by_Q_type()

for category in totalQs:
    plot_by_question_type(category)
	
for student in students:
	print_scores(student)
	print()