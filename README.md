# The Home Depot - Visual Navigation

Case study [Python]

The goal of this case is to recommend product subcategories or attribute to customer to narrow search queries, faciliate easier navigation, and improve customer experience for HomeDepot.com. 

My scope ranging from further defining the scope of the problem, exploratory data analysis, and defining a benchmark model. 


### Install

This project requires Python 3 and the following Python libraries installed:

- [NumPy](http://www.numpy.org/)
- [Pandas](http://pandas.pydata.org)
- [Plotly](http://matplotlib.org/)
- [scikit-learn](http://scikit-learn.org/stable/)
- [nltk](https://www.nltk.org/)
- [gensim](https://radimrehurek.com/gensim/)


You will also need to have software installed to run and execute an [iPython Notebook](http://ipython.org/notebook.html)


### Organization

```
├── README.md          
├── data      
│   ├── processed      preprocessed data, pickle files
│   └── raw (removed)           original, immutable data
├── notebooks
│   ├── 00.Getting Started 
│   ├── 01.Data Exploration
│   ├── 02. Preprocessing
│   └── 03. Benchmark Model 
```


### Data

* ```Data_dictionary.xlsx``` – data field descriptions
* ```Visual_navigations.csv``` – recommendations for 363 unique Décor search queries. Each query has at least
2 recommendations. The data can be used for offline evaluation of your algorithms (required) and
training (optional)
* ```Décor_catalog.csv``` – all the Décor products and categories
* ```Product_name_description.csv``` – Product name and descriptions
* ```Search_impression.csv``` – Top 24 products returned by the search engine
* ```Product_engagement.csv``` – clicked products after the search and associated visits in the past 6 months;
a minimum threshold of 5 has been applied.

