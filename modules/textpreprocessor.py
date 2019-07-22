
import pandas as pd

import gensim
from gensim.parsing.preprocessing import remove_stopwords

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer

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


    def clean_text(self, df, corpus_col):
        '''Call preprocessor generator object'''

        corpus = df.loc[:, corpus_col].tolist()

        return list(self.preprocess_text(corpus))


    def preprocess_text(self, docs):
        '''
        Process docs

        Returns:
        --------
        tokenized list of docs
        '''
        #docs = docs.values
        method='lemmatizer'
        if method == 'lemmatizer':
            lemma = nltk.stem.WordNetLemmatizer()
            root = lemma.lemmatize
        elif method == 'stemmer':
            stemmer = nltk.stem.snowball.SnowballStemmer("english")
            root = stemmer.stem

        for doc in docs:
            tokens = gensim.utils.simple_preprocess(doc)
            yield(' '.join([root(token) for token in tokens if not token in self.stop_words]))

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
