import spacy
from sklearn.feature_extraction.text import TfidfVectorizer

# Define List of Stop Words
new_stop_words = ['in', 'sq','ft', 'yd', 'cm', 'mm','gal','lb' ,'lbs','qt','oz', 'h', 'w', 'ii', 'x']

stop_words = set(stopwords.words('english') + new_stop_words)

nlp = spacy.load('en', disable=['parser', 'tagger', 'ner'])

def preprocess(doc):
    '''
    Process docs 
    '''
    
    doc = nlp(doc)
    
    lemma_doc = [token.lemma_ for token in doc if not token.is_stop]
    
    return ' '.join(lemma_doc).lower()

def vectorize(corpus):
    
    vectorizer = TfidfVectorizer(stop_words='english')
    matrix = vectorizer.fit_transform(preprocess(doc) for doc in corpus)
    
    return vectorizer, matrix
    