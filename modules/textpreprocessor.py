
import gensim
from gensim.parsing.preprocessing import remove_stopwords

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer

'''
Preprocess text for products descriptions and serch queries
'''

# Define List of Stop Words
new_stop_words = ['in', 'sq','ft', 'yd', 'cm', 'mm','gal','lb' ,'lbs','qt','oz', 'h', 'w', 'ii', 'x']
stop_words = set(stopwords.words('english') + new_stop_words)

class TextPreprocessor:
    def __init__(self, stop_words=stop_words):
        self.stop_words = stop_words


    def preprocess(self, corpus):
        '''
        Process documents

        Keyword Arguments:
        ------------------
        * corpus - list of documents
        * stop_words = set of stopwords

        Returns:
        --------
        Each document as a list of tokens (iterator)

        e.g., clean_corpus = list(preprocess(corpus))
        '''

        lemmatizer = WordNetLemmatizer()

        for doc in corpus:
            tokens = gensim.utils.simple_preprocess(doc, deacc=True)
            yield([lemmatizer.lemmatize(token) for token in tokens if not token in stop_words])


    def trigram_model(self, corpus_tokens, threshholds=(25,15), verbose=False):
        '''
        Build trigram model

        Keyword Arguments:
        ------------------
        * corpus - list of documents (as tokens)
        * stop_words = set of stopwords

        Returns:
        --------
        trigram model tokens
        '''

        bigram = gensim.models.Phrases(corpus_tokens,
                                        min_count=threshholds[0])

        trigram = gensim.models.Phrases(bigram[corpus_tokens],
                                        min_count=threshholds[1])

        # trigram/bigram model
        bigram_model = gensim.models.phrases.Phraser(bigram)
        trigram_model = gensim.models.phrases.Phraser(trigram)

        corpus_new = [trigram_model[bigram_model[doc]] for doc in corpus_tokens]

        if verbose:
            for doc in corpus_new[0:5]:
                print(f'{" ".join(trigram_model[bigram_model[doc]]) } \n')

        return corpus_new

    def vectorize(self, corpus, format='tokens'):
        '''
        TFIDF Vectorizer
        '''
        if format == 'tokens':
            corpus = self.tokens2corpus(corpus)

        vectorizer = TfidfVectorizer(stop_words='english')
        matrix = vectorizer.fit_transform(corpus)

        return vectorizer, matrix


    def tokens2corpus(self, tokenized_docs):
        '''
        Helper fuction to convert from tokens to text
        '''
        for doc in tokenized_docs:
            yield ' '.join([token for token in doc])
