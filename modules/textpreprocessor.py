
import pandas as pd

import gensim
from gensim.parsing.preprocessing import remove_stopwords

import nltk
from nltk.corpus import brown
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer

from textblob import TextBlob

'''
Preprocess text for products descriptions and serch queries
'''

# Define List of Stop Words
class TextPreprocessor:

    def __init__(self, search_imp=None, prod_desc=None, catalog=None):
        self.search_imp = search_imp
        self.prod_desc = prod_desc
        self.catalog = catalog

        self.stop_words_lst = ['in', 'sq','ft', 'yd', 'cm', 'mm','gal','lb' ,'lbs','qt','oz', 'h', 'w', 'ii', 'x']
        self.stop_words = list(set(stopwords.words('english') + self.stop_words_lst))


    def read_in_dataset(self, data, data_folder='raw', verbose=False):
        '''
        Read in dataset (csv format) to pandas dataframe

        Keyword Arguments:
        ------------------
        * dataset - string with dataset filename
        * data_folder - string with either raw or processed
        * verbose - True will print intormation about the dataset

        Returns:
        --------
        a pandas dataframe
        '''
        df = pd.read_csv('../data/{}/{}.csv'.format(data_folder, data))

        return df


    def clean_text(self, df, corpus_col, method):
        '''Call preprocessor generator object'''

        corpus = df.loc[:, corpus_col].tolist()
        self.method=method

        return list(self.preprocess_text(corpus))


    def preprocess_text(self, docs):
        '''
        Process docs

        Returns:
        --------
        tokenized list of docs
        '''
        #docs = docs.values

        if self.method == 'lemmatizer':
            lemma = nltk.stem.WordNetLemmatizer()
            root = lemma.lemmatize
        elif self.method == 'stemmer':
            stemmer = nltk.stem.snowball.SnowballStemmer("english")
            root = stemmer.stem

        for doc in docs:
            #b=TextBlob(doc)
            #doc = str(b.correct())
            tokens = gensim.utils.simple_preprocess(doc)
            
            yield(' '.join([root(token) for token in tokens if not token in self.stop_words]))



    def trigram_model(self, corpus_tokens, threshholds=(25,15), verbose=False):
        '''
        Build trigram model

        Keyword Arguments:
        ------------------
        * corpus - list of documents (as tokens)
        * stop_words = set of stopwords

        Returns:
        --------
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


    def vectorize(self, corpus, format='docs'):

        if format == 'tokens':
            corpus = self.tokens2corpus(corpus)

        vectorizer = TfidfVectorizer(stop_words='english')
        matrix = vectorizer.fit_transform(corpus)

        return vectorizer, matrix


    def doc2tokens(corpus):
        return corpus.str.split()


    def tokens2corpus(self, tokenized_docs):
        '''
        Helper fuction to convert from tokens to text
        '''
        for doc in tokenized_docs:
            yield ' '.join([token for token in doc])

    def compare_clean_searches(self, clean_searches, raw_search):
        '''Compare cleaned search queries to raw text'''
        st_compare = pd.DataFrame({'raw_search': raw_search['Search_term'], 'cleaned_search':clean_searches}).sort_values(by='raw_search')
        return st_compare.groupby('cleaned_search')['raw_search'].apply(list)


    def add_stopword(self, new_stopword):
        self.stop_words.append(new_stopword)


    def clean_docs(self, docs):
        return list(self.preprocess_text(docs))


    def correct_spelling(self, query):
        word_list = brown.words()
        word_set = set(word_list)

        if query not in word_set:
            b=TextBlob(query)
            query = str(b.correct())

        return query
