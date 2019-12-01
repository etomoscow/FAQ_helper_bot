# -*- coding: utf-8 -*-
import gensim
import nltk
import re
import requests
import warnings
import telebot
from telebot import types
import time
import gensim.downloader as api
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk import word_tokenize
nltk.download('stopwords')
nltk.download('wordnet')
from gensim import corpora
from gensim.matutils import softcossim
warnings.filterwarnings('ignore')

bot = telebot.TeleBot('825081032:AAF-dN9NmT2BgKkL29mTB3BEnLTUr9mj9uQ')


stop_words = stopwords.words('russian')
w2v_model = api.load('word2vec-ruscorpora-300')

faq=['С чем связано изменение сроков действия договоров проживания для всех обучающихся?',
		'В течении какого срока теперь будет действовать договор проживания?',
		'Значит ли что студенту бакалавриата теперь нужно будет жить все 4 года в одной комнате?',
		'Если договор действует несколько лет, то значит можно не приходить к коменданту поселяться каждый год в сентябре?',
		'Могут ли меня выселить, если я ухожу в академический отпуск??',
		'А как же тогда оплачивать проживание в общежитии?',
		'Я хотел бы уехать на лето и не оплачивать проживание за летние месяцы. Это возможно?',
		'У меня уже есть почта на @phystech.edu, я ею активно пользуюсь, но в деканате выдали новую, которая мне не нравится. Как заменить новую на старую почту?',
		'Открыл анкету, увидел неправильно написанные ФИО/адрес постоянной регистрации/дату рождения. Как исправить данные?',
		'У меня есть почта на @phystech.edu, но я забыл от нее пароль.',
		'В деканате выдали только почту, без пароля. Где его можно получить?',
		'Я зарегистрировался на сайте mipt.ru, но не могу войти в личный кабинет. Что делать?',
		'Почта, логин и пароль верны, но попасть в личный кабинет не получается.',
		'По какой-то причине у меня нет почты на @phystech.edu. Как мне ее получить?']

answers = ['''Согласно статье 105 жилищного кодекса РФ:
“Договор найма жилого помещения в общежитии заключается на период трудовых отношений, прохождения службы или обучения. Прекращение трудовых отношений, обучения, а также увольнение со службы является основанием прекращения договора найма жилого помещения в общежитии.”''',

		'''Договор будет действовать в течении всего срока обучения на соответствующей ступени образования (в бакалавриате - 4 года, в магистратуре - 2 года и в аспирантуре - 4 года)''',

		'''Изменение договора проживания возможно по обоюдному согласию проживающего и института (в данном случае в лице факультетской комиссии по поселению). Комиссии по поселению будут ежегодно рассматривать пожелания проживающих по переселению и пытаться их удовлетворить в новых условиях. Следите за объявлениями в своем общежитии о начале сбора электронных анкет на переселение.''',

		'''Именно так. Обучающиеся, которые сохраняют свое койко-место на следующий год, будут избавлены от необходимости стояния в очередях на поселение.''',

		'''Студенты, находящиеся в академическом отпуске являются обучающимися МФТИ,  и имеют право на место в общежитии. При уходе в академический отпуск договор о поселении продолжает действовать.''',

		'''Цена проживания в общежитии устанавливается приказом ректора. В настоящий момент прорабатываются возможные процедуры оплаты, но оплата общежития у коменданта в удобное время останется. Оплата за общежитие взимается за каждый месяц независимо от того проживает ли обучающийся физически в нем или нет.''',

		'''В настоящий момент это возможно только при условии расторжения договора и повторного заключения его осенью.''',

		'''Обратитесь в Учебный отдел (413 АК) с просьбой заменить вашу почту в анкете базы 1С.''',

		'''Обратитесь в Учебный отдел (413 АК) с просьбой заменить ваши данные в анкете базы 1С.''',

		'''Необходимо написать письмо с запросом на восстановление почты и/или пароля к ней на helpdesk@mipt.ru. К письму приложите скан (фото) студенческого билета или зачетки.''',

		'''Необходимо написать письмо с запросом на выдачу временного пароля от новой почты на helpdesk@mipt.ru''',
		'''	1) Проверьте, на какой почте вы зарегистрировались. Для регистрации подходит только почта на @phystech.edu, выданная в деканате или уже имеющаяся у вас и замененная в Учебном отделе в базе 1С.
    		2) Если почта верна, проверьте логин и пароль. Они должны совпадать с указанными при регистрации на сайте с использованием почты @phystech.edu.''',
    	'''Если вы действительно перепроверили все данные, но так и не зашли в личный кабинет, то обращайтесь в техническую поддержку 517 кабинет Аудиторного корпуса в рабочее время либо пишите обращение на почтовый адрес helpdesk@mipt.ru.''',
    	'''Порядок получения по ссылке (https://mipt.ru/it/services/#mail) почтовые сервисы.'''] 


@bot.message_handler(commands=['start'])
def start_message(message):
	bot.send_message(message.chat.id,
	 'Привет! Я помогаю с наиболее часто задаваемыми вопросами по поселению в МФТИ (https://mipt.ru/poselenie/students/faq.php)')


@bot.message_handler(commands=['help'])
def help(message):
	bot.send_message(message.chat.id,
	 'Можешь просто ввести вопрос и я выдам наиболее похожий вопрос и соответствующий ответ!')

@bot.message_handler(commands=['display_faq'])
def display_faq(message):
	markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
	btn1 = types.KeyboardButton('С чем связано изменение сроков действия договоров проживания для всех обучающихся?')
	btn2 = types.KeyboardButton('В течении какого срока теперь будет действовать договор проживания?')
	btn3 = types.KeyboardButton('Значит ли что студенту бакалавриата теперь нужно будет жить все 4 года в одной комнате?')
	btn4 = types.KeyboardButton('Если договор действует несколько лет, то значит можно не приходить к коменданту поселяться каждый год в сентябре?')
	btn5 = types.KeyboardButton('Могут ли меня выселить, если я ухожу в академический отпуск?')
	btn6 = types.KeyboardButton('А как же тогда оплачивать проживание в общежитии?')
	btn7 = types.KeyboardButton('Я хотел бы уехать на лето и не оплачивать проживание за летние месяцы. Это возможно?')
	btn8 = types.KeyboardButton('У меня уже есть почта на @phystech.edu, я ею активно пользуюсь, но в деканате выдали новую, которая мне не нравится. Как заменить новую на старую почту?')
	btn9 = types.KeyboardButton('Открыл анкету, увидел неправильно написанные ФИО/адрес постоянной регистрации/дату рождения. Как исправить данные?')
	btn10 = types.KeyboardButton('У меня есть почта на @phystech.edu, но я забыл от нее пароль.')
	btn11 = types.KeyboardButton('В деканате выдали только почту, без пароля. Где его можно получить?')
	btn12 = types.KeyboardButton('Я зарегистрировался на сайте mipt.ru, но не могу войти в личный кабинет. Что делать?')
	btn13 = types.KeyboardButton('Почта, логин и пароль верны, но попасть в личный кабинет не получается.')
	btn14 = types.KeyboardButton('По какой-то причине у меня нет почты на @phystech.edu. Как мне ее получить?')
	markup.add(btn1,btn2)
	markup.add(btn3,btn4)
	markup.add(btn5,btn6)
	markup.add(btn7,btn8)
	markup.add(btn9,btn10)
	markup.add(btn11,btn12)
	markup.add(btn13,btn14)
	bot.send_message(message.chat.id, 'Choose one of the questions below', reply_markup=markup)
	pass


def cleaner(faq):
	stem = WordNetLemmatizer()
	faq_clean = []
	for line in faq:
		line = re.sub('\?','', line) 
		faq_clean.append([stem.lemmatize(word) for word in line.lower().split() if word not in stop_words])
	return faq_clean

def cleanq(text):
	stem = WordNetLemmatizer()
	text = re.sub('\?','', text) 
	stem = WordNetLemmatizer()
	text = [stem.lemmatize(word) for word in text.lower().split() if word not in stop_words]
	return text 

def similarity(quest, faq=faq):
	faq_clean = cleaner(faq)
	dictionary = corpora.Dictionary(faq_clean)
	corpus = [dictionary.doc2bow(q) for q in cleaner(faq)]
	similarities = [] 
	faq_ = cleaner(faq)
	dictionary = corpora.Dictionary(faq_)
	corpus = [dictionary.doc2bow(q) for q in faq_]
	similarity_matrix = w2v_model.similarity_matrix(dictionary)
	question = cleanq(quest)

	for i in range(len(corpus)):
		similarities.append(softcossim(dictionary.doc2bow(question), corpus[i], similarity_matrix))
	return(faq[similarities.index(sorted(similarities, reverse=True)[0])], similarities.index(sorted(similarities, reverse=True)[0])) 


@bot.message_handler(content_types=['text'])
def ans(message):
	if message.text in faq:
			bot.reply_to(message, answers[faq.index(message.text)])
			return 0
	else:
		bot.send_message(message.chat.id, similarity(message.text)[0])
		bot.send_message(message.chat.id, answers[similarity(message.text)[1]])
	pass

bot.polling()