import requests, json, html
import sopel.module
def q_and_a():

	response = requests.get("https://opentdb.com/api.php?amount=1&difficulty=medium&type=multiple")
	data = response.json()
	#question and answer
	question = (html.unescape(data['results'][0]['question']))
	correct_answer = (html.unescape(data['results'][0]['correct_answer']))
	answers = html.unescape(data['results'][0]['incorrect_answers'])
	answers.append((str(correct_answer)))
	an = ''
	for i in range(1,5):
		an = an + ' ' + str(i) + '.' +  answers[i-1]

	ans = {}
	for i in range(0,len(answers)):
		ans[i+1] = answers[i]
	return ans,correct_answer,question

active = False
count = 0
@sopel.module.commands('start')
def start(bot,trigger):
	#  trigger.group(2) = args

	global count
	global active
	global ans
	global correct_answer
	if count < 5:
		ans,correct_answer,question = q_and_a()
		bot.say(question)
		bot.say(str(ans))
		#bot.say(correct_answer)
		active = True


@sopel.module.rule('^[^\.\.]')
def an(bot, trigger):
	global active
	global count
	if (active == True) and (str(trigger) == correct_answer):
		bot.say("Congratulations " + str(trigger.nick) + " You win")
		active = False
		count = count + 1
		start(bot,trigger)

	#	if ans[int(trigger)] == correct_answer:
	#		bot.say("Correct")



@sopel.module.rule('hello!?')
def hi(bot, trigger):
    bot.say('Hi, ' + trigger.nick + trigger)
