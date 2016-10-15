from gensim import corpora
from gensim import corpora, models, similarities
import pprint


class SentenceMatcher:
	sentences=[]
	def __init__(self,appname):
		self.appname=appname
	# Get default English stopwords and extend with punctuation
	stopwords = nltk.corpus.stopwords.words('english')
	stopwords.extend(string.punctuation)
	stopwords.append('')
	lemmatizer = nltk.stem.wordnet.WordNetLemmatizer()


	def get_group_wise_data(groupsize=0):
		sentences = [
	"What is the official working / business hours / timing?",
	"Is there a Dress Code to be followed?",
	"Is there a specific Bank for Salary accounts? Or can I use my existing bank account be tagged to the corporate salary account?",
	"Where can I can some basic stationary from?",
	"By when can I get my ID / Access card?",
	"Do we have a parking facility ? Do we get parking stickers? ",
	"Do we get personal water Bottles from the company?",
	"Is there transport facility provided? ",
	"Do we have an online Office Directory with all employees contacts? ",
	"How can I get business cards?",
	"Where can I get the Holiday List for this year?",
	"How many leaves do we get? What is the Leave policy on all categories of Leaves? Privilege, Sick, Casual, Maternity, Paternity , Marriage",
	"Where do I view my Leave Balance?",
	"Do we have Flexible working hours and WFH Facility?",
	"Do we have a in-house Library for Technical Books?",
	"Is there any tie-up with Banks or Retails outlets for Corporate offers ?",
	"Is there a New Hire Orientation for new hires?",
	"Does the company sponsor any certifications or is there a education assistance policy ?",
	"Who is the point of contact for Payroll and who can help with Tax Declarations  if help needed? ",
	"I want to initiate my PF transfer? Whom should I reach out to?",
	"Can I claim my mobile phone / data charges used for official purpose?",
	"Insurance - What's the coverage / policy ?",
	"Will I get a mediclaim card or will it be a e card?",
	"Is there any facility for emergency loans or salary advances?",
	"Is there an Intranet Site where I can access all HR policies and Benefits ?",
	"I have friends interested to interview with us, where can I see the current open positions and how do  I refer? Can I get some details on our Referral Policy?",
	"When is the salary paid out / credit date?",
	"How does the Bonus program work, is it linked to my performance? What is the average payout? ",
	"Is there a probation period? ",
	"Is there a Performance Management Program ? Will my Goals / KRA's be set by my manager and discussed with me?",
	"What is the appraisal cycle? I have joined mid year of the cycle, will I be eligible?",
	"What is the process of Expense Reimbursement?",
	"Who is the point of contact for IT? Need help with Login and Password credentials?",
	"Whom should I reach out to, to get storage / cabinet keys?",
	"My parents / family want to visit my office, is there visiting hours to follow or specific days that they can visit office for an office tour?",
	"Is there a Gym Facility ?",
	"Is Lunch facility available and do I have to pay or do we get food coupons?",
	"Is there a creche facility?",
	"Do we have power nap / dormitory rooms?",
	"Is there recreation area? TT, Caroms, Foosball etc.?",
	"Is there a document which explains Career Path for my position which I can refer to?"
	]
		if groupsize==0:
			return sentences
		i=0;
		temp=" "
		data=[]
		for sentence in sentences:
			temp=temp+sentence
			i=i+1
			if (i%groupsize) == 0 :
				data.append(temp)
				temp=" "
		return data

	def get_wordnet_pos(pos_tag):
	    if pos_tag[1].startswith('J'):
	        return (pos_tag[0], wordnet.ADJ)
	    elif pos_tag[1].startswith('V'):
	        return (pos_tag[0], wordnet.VERB)
	    elif pos_tag[1].startswith('N'):
	        return (pos_tag[0], wordnet.NOUN)
	    elif pos_tag[1].startswith('R'):
	        return (pos_tag[0], wordnet.ADV)
	    else:
	        return (pos_tag[0], wordnet.NOUN)

	def lemmatize_remove_stopword(a):
		pos_a = map(get_wordnet_pos, nltk.pos_tag(wordpunct_tokenize(a)))
		lemmae_a = [lemmatizer.lemmatize(token.lower().strip(string.punctuation), pos) for token, pos in pos_a \
	                    if (pos == wordnet.NOUN or pos == wordnet.ADJ or pos == wordnet.VERB ) and token.lower().strip(string.punctuation) not in stopwords]
	    return lemmae_a

	def create_dict_and_save(texts,no_below,no_above):
		self.dictionary = corpora.Dictionary(texts)
		self.dictionary.filter_extremes(no_below=no_below,no_above=no_above)
		dictionary.save(self.appname+'.dict')
		# print(dictionary)
		return dictionary

	def train_model_and_save(no_of_topics,corpus):

		#tfidf to reinforce tokens that are less frequent in doc
		tfidf=models.TfidfModel(corpus,normalize=True)
		corpus_tfidf=tfidf[corpus]

		#build models and indexes with dictionary and corpus and save for future use
		#The topic has to be decided by trial
		lsi = models.LsiModel(corpus_tfidf, id2word=self.dictionary, num_topics=no_of_topics)
		lsi.save(self.appname+'.lsi')

		# pprint.pprint(lsi.print_topics(no_of_topics))
		index = similarities.MatrixSimilarity(lsi[corpus]) # Can be a different corpus alltogether
		index.save(self.appname+'.index')

	def find_matching_sentences(query):
		dictionary = corpora.Dictionary()
		dictionary.load(self.appname+'.dict')
		# print dictionary
		index = similarities.MatrixSimilarity.load(self.appname+'.index')
		lsi = models.LsiModel.load(self.appname+'.lsi')
		doc = query
		# print (lemmatize_remove_stopword(doc))
		vec_bow = dictionary.doc2bow(lemmatize_remove_stopword(doc))
		# print vec_bow
		vec_lsi = lsi[vec_bow]
		# print(vec_lsi)
		sims = index[vec_lsi]
		sims = sorted(enumerate(sims), key=lambda item: -item[1])
		# pprint.pprint( list(enumerate(sentences)))
		print(list(enumerate(sims)))
		if sims[0][1] >= 0.5:
			print str(sims[0][1])
			# print sentences[sims[0][0]] + " and value is " + str(sims[0][1])
		else:
			print "No match found !"

if __name__ == "__main__":
	sentence_matcher=SentenceMatcher('newApp','10')
	sentences=sentence_matcher.get_group_wise_data(0)
	texts=[lemmatize_remove_stopword(sentence) for sentence in sentences]	
	# print texts
	#Create dictionary from corpus, the 2nd and 3rd params will depend on your corpus
	sentence_matcher.create_dict_and_save(texts,no_below=1,no_above=0.1)
	corpus = [sentence_matcher.dictionary.doc2bow(text) for text in texts]
	# corpora.MmCorpus.serialize('deerwester.mm', corpus)
	sentence_matcher.train_model_and_save(6,corpus)
	sentence_matcher.find_matching_sentences("How flexible are the working hours ?")

