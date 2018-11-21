import requests, json, html
import sopel.module
def q_and_a():

	response = requests.get("https://opentdb.com/api.php?amount=1&difficulty=easy&type=multiple")
	data = response.json()
	#question and answer
	question = (html.unescape(data['results'][0]['question']))
	correct_answer = (html.unescape(data['results'][0]['correct_answer']))
	answers = html.unescape(data['results'][0]['incorrect_answers'])
	answers.append((str(correct_answer)))
	an = ''
	for i in range(1,5):
		an = an + ' ' + str(i) + '.' +  answers[i-1]

	pr_ans = ''
	for i in range(0,len(answers)):
		pr_ans = pr_ans + " " + str(i+1) + " :" + str(answers[i]) + " ,"

	ans = {}
	for i in range(0,len(answers)):
		ans[i+1] = answers[i]

	return ans,correct_answer,question,pr_ans

isActive = False
question_count = 0
@sopel.module.commands('start')
def start(bot,trigger):
	#  trigger.group(2) = args

	global question_count,isActive,ans,correct_answer
	if not isActive:

		if question_count < 5:
			ans,correct_answer,question,pr_ans = q_and_a()
			bot.say(question)
			bot.say(str(pr_ans))
			#bot.say(str(ans))
			#bot.say(ans[1])
			#bot.say(correct_answer)
			isActive = True
		else:
			isActive = False
	else:
		bot.say("Quiz Already running")


#@sopel.module.rule('^[^\.\.]')
@sopel.module.rule('[1-4]')

def an(bot, trigger):
	global isActive,question_count,ans

#	if (isActive == True) and (str(trigger) == correct_answer):

	if (isActive == True) and (ans[int(trigger)] == correct_answer):
		bot.say("Congratulations " + str(trigger.nick) + " You win")
		isActive = False
		question_count += 1
		if question_count < 5:
			start(bot,trigger)
		else:
			bot.say("Game Over")
			question_count = 0
	#	if ans[int(trigger)] == correct_answer:
	#		bot.say("Correct")


@sopel.module.commands('skip')
def skip(bot,trigger):
	global question_count,correct_answer,isActive

	if isActive == True:

		bot.say("Question Skipped, The answer was " + correct_answer)
		question_count += 1

		isActive = False
		if question_count == 5:
			bot.say("Game Over")
		start(bot, trigger)
	else:
		bot.say("Quiz Not Running, Can't Skip")



@sopel.module.rule('hello!?')
def hi(bot, trigger):
    bot.say('Hi, ' + trigger.nick + trigger)
