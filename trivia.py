import requests, json, html
import sopel.module
'''
question = ''
correct_answer = ''
answers = []
data = ''
'''
def q_and_a():

	response = requests.get("https://opentdb.com/api.php?amount=1&difficulty=medium&type=multiple")
	data = response.json()
	#question and answer
	question = (html.unescape(data['results'][0]['question']))
	correct_answer = (html.unescape(data['results'][0]['correct_answer']))
	answers = html.unescape(data['results'][0]['incorrect_answers'])
	answers.append((str(correct_answer)))
	#print(question)
	an = ''
	for i in range(1,5):
		an = an + ' ' + str(i) + '.' +  answers[i-1]
	#print(answers)
	#print(an)
	#print(str(correct_answer))
	ans = {}
	for i in range(0,len(answers)):
		ans[i+1] = answers[i]
	return ans,correct_answer,question
#def play():
	#ans,correct_answer = q_and_a()
	#user_answer = int(input('Enter Answer : '))
	#if ans[user_answer] == correct_answer:
	#	print('Correct')
	#else:
	#	print('Wrong')
	#	print('Correct Answer is '+correct_answer)
		#correct_answer ---->
	#answers ----------->

#play()

active = False

@sopel.module.commands('start')
def start(bot,trigger):
	global active
	ans,correct_answer,question = q_and_a()
	bot.say(question)
	bot.say(str(ans))
	bot.say(correct_answer)
	active = True

@sopel.module.rule('[1-4]')
def an(bot, trigger):
	global active
	if active == True:
		bot.say("number")
		active = False
	#	if ans[int(trigger)] == correct_answer:
	#		bot.say("Correct")

@sopel.module.rule('hello!?')
def hi(bot, trigger):
    bot.say('Hi, ' + trigger.nick + trigger)
