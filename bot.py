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
#nltk.download('stopwords')
#nltk.download('wordnet')
from gensim import corpora
from gensim.matutils import softcossim
warnings.filterwarnings('ignore')

bot = telebot.TeleBot('825081032:AAF-dN9NmT2BgKkL29mTB3BEnLTUr9mj9uQ')


stop_words = stopwords.words('english')
w2v_model = api.load("glove-wiki-gigaword-50")

faq=['What is the preparatory course?',
		'What is an invitation letter?',
		'What does registration mean?',
		'Is it possible to study and work at the same time?',
		'How long does the academic year last?',
		'What documents are required for admission?',
		'What are the tuition fees?',
		'Should I insure my life?',
		'In which cases can a student be expelled from the university?',
		'How to get a bank or a credit card?',
		'How to get a social card?',
		'What if I have a problem or other questions?']

answers = ['''The preparatory course is a special educational program 
		lasting one academic year — that is, between seven
		and 10 months. Students taking this course study
		Russian, mathematics, and physics. The course
		ends with an exam, and the passing students receive a certificate of completion.''',

		'''An invitation is an official document prepared by the Ministry of Internal Affairs of the Russian Federation.
		It confirms that the student to whom the invitation is addressed has been admitted to the university.
		The invitation contains the student’s passport data and specifies the full designation of the university.
		This document needs to be submitted to the Russian Embassy in order to receive a visa.
			
		The internal affairs ministry usually issues the invitation letter within 45 days.''',

		'''Registration grants a foreign citizen the legal right to stay on the territory of Russia.
		It is usually provided for a period of one year and needs to be renewed annually.
		To prolong your registration, submit an application about three weeks before it expires.
		Upon arrival at the university, a student needs to register at the International Department of MIPT within three days, including the day of arrival.
		The registration stamp is put on the migration card.

		It is recommended that the passport be renewed before a trip to Russia for the full period of study.''',

		'''Russia offers great opportunities for getting a high-quality fundamental education.
		An MIPT degree enables you to find a well-paid job and start climbing the career ladder right after completing the university program.

		Students at Russian universities are required to attend all lectures as only the knowledge
		gained during classroom instruction enables one to become a skilled and knowledgeable professional.
		This means that side job opportunities are limited to working after classes, on weekends, or during vacations.
		However, even that should probably be reserved for when you have gotten to know the country and the language better.
		Usually, it is during the junior year that getting a job really becomes an option, but only if you study well and attend all mandatory classes.''',

		'''The academic year lasts 10 months — from Sept. 1 to June 30 — and consists of two semesters.
		The first semester begins Sept. 1 and ends Jan. 25, and the second is between Feb. 9 and June 30.

		Between the semesters, the students are on vacations.
		The brief winter break lasts two weeks, from Jan. 25 to Feb. 9, and the summer vacations are two months long, from July 1 to Aug. 30.
		During that time, some students stay in Russia, while others go back home to spend time with their families.''',

		'''The papers you need are:
				1. Passport.
				2. Documents certifying prior education, with transcripts.
				3. Medical certificate confirming your good health.
		The submitted documents have to be translated into Russian.''',

		'''A program taught in Russian will cost you 250,000 rubles per year. The fees on English-taught programs are higher, at 400,000 rubles per year.''',
		'''Life and health insurance are obligatory for any foreign citizen arriving in Russia to study. The cost of life and health insurance is 8,200 rubles per year.
		A student needs to carry the insurance policy specifying the phone number of the insurance company and the emergency health service at all times.

		All Russian universities have medical offices for first aid and general medical care.''',

		'''You can be expelled:
				Of your own free will.
				For health reasons.
				For poor academic progress.

		In the latter case, the grounds for expelling a student are:
				Not passing the exams in multiple subjects in the allotted time at the end of a semester.
				Repeatedly failing an exam or not turning up for it in the designated time.
				Failing an exam in front of the board of examiners, which usually convenes after three failed attempts.
				Violating rules of conduct or other regulations.''',

		'''Visit the social service on the second floor of the building housing the dining hall. The social service is next to local internal affairs office.

				Get an application form for card issue and fill it in, submitting it along with the accompanying documents:
				Copy of the page with the photo from your passport.
				Migration card.
				Notarized translation of the passport.
				Consent to personal data processing.
				Residence permit, if you have one.

		You can submit the documents personally on weekdays between 10:30 a.m. and 5:30 p.m.''',

		'''To issue a social card, you need to visit a multifunctional center in Moscow.
		Fill in the application provided at the multifunctional center.
		You need to have a notarized copy of your passport and your student ID with you.
		The latter refers to the credential you use daily to gain access to university buildings.

		A list of multifunctional centers is available online, so you can choose the one that is more convenient.''',

		'''If you have any further inquiries, you can address them to the International Students Office, which is located in the Auditorium Building, Room 315. The phone number is (7-495) 408-7043.
		Here are the people who can help you:

				Polina Golubkova
				English-taught master’s programs manager
				Phone: (7-498) 744-6592
				Email: golubkova.p@gmail.com

				Albert Baryshev
				International students officer
				Phone: (7-495) 408-7043
				Email: baryshev.aa@mipt.ru

				Kseniya Nikitina
				Internship programs manager
				Phone: (7-495) 408-6592
				Email: kv.nikitina@yandex.ru'''] 


@bot.message_handler(commands=['start'])
def start_message(message):
	bot.send_message(message.chat.id,
	 'Hi! I am designed to help with FAQ at mipt.ru/english/edu/faqs/')


@bot.message_handler(commands=['help'])
def help(message):
	bot.send_message(message.chat.id,
	 'You can simply type your question and I will show the most similar one. Also you can type "/display_faq" and display the whole FAQ to choose the question')

@bot.message_handler(commands=['display_faq'])
def display_faq(message):
	markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
	btn1 = types.KeyboardButton('What is the preparatory course?')
	btn2 = types.KeyboardButton('What is an invitation letter?')
	btn3 = types.KeyboardButton('Is it possible to study and work at the same time?')
	btn4 = types.KeyboardButton('How long does the academic year last?')
	btn5 = types.KeyboardButton('What documents are required for admission?')
	btn6 = types.KeyboardButton('What are the tuition fees?')
	btn7 = types.KeyboardButton('Should I insure my life?')
	btn8 = types.KeyboardButton('In which cases can a student be expelled from the university?')
	btn9 = types.KeyboardButton('How to get a bank card?')
	btn10 = types.KeyboardButton('How to get a social card?')
	btn11 = types.KeyboardButton('What if I have a problem or other questions?')
	btn12 = types.KeyboardButton('What does registration mean?')
	markup.add(btn1,btn2)
	markup.add(btn3,btn4)
	markup.add(btn5,btn6)
	markup.add(btn7,btn8)
	markup.add(btn9,btn10)
	markup.add(btn11,btn12)
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