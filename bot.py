import gensim
import nltk
import re
import warnings
import gensim.downloader as api
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk import word_tokenize
nltk.download('stopwords')
nltk.download('wordnet')
from gensim import corpora
from gensim.matutils import softcossim
warnings.filterwarnings('ignore')

stop_words = stopwords.words('english')
w2v_model = api.load("glove-wiki-gigaword-50")
dictionary = corpora.Dictionary(faq_clean)
corpus = [dictionary.doc2bow(q) for q in faq_clean]

faq = ['What is the preparatory course?',
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


def cleaner(faq):
	stem = WordNetLemmatizer()
	faq_clean = []
	for line in faq:
	    line = re.sub('\?','', line) 
	    faq_clean.append([stem.lemmatize(word) for word in line.lower().split() if word not in stop_words])
	 return faq_clean

def cleanq(text):
	stem - WordNetLemmatizer()
	text = re.sub('\?','', text) 
    stem = WordNetLemmatizer()
    text = [stem.lemmatize(word) for word in text.lower().split() if word not in stop_words]
    return text 

faq_ = cleaner(faq)
dictionary = corpora.Dictionary(faq_)
corpus = [dictionary.doc2bow(q) for q in faq_]
similarity_matrix = w2v_model.similarity_matrix(dictionary)

question = cleanq(input())


def similarity(quest, faq=faq):
	similarities = [] 
	for i in range(len(corpus)):
		similarities.append(softcossim(dictionary.doc2bow(quest), corpus[i], similarity_matrix))
	print('Your questions is similar to:',faq[similarities.index(sorted(similarities, reverse=True)[0])])
	pass 