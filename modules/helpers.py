import pandas as pd

'''
Object to preprocess data
'''

def read_in_dataset(dataset, data_folder='raw', data_type='csv', verbose=False):
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
    if data_type == 'csv':
        df = pd.read_csv('../data/{}/{}'.format(data_folder, dataset))
    elif data_type == 'excel':
        df = pd.read_excel('../data/{}/{}'.format(data_folder, dataset))

    if verbose:
        print('\n{0:-^80}'.format(' Reading in the following dataset: {0}'.format(dataset)))
        print("\n Shape: {0} rows and {1} columns".format(*df.shape))
        print('\n{0:-^80}\n'.format(' It has the following columns '))
        print(df.columns)
        print('\n{0:-^80}\n'.format(' The first 5 rows look like this '))
        print(df.head())

    return df


def get_num_of_levels(series, sep='>', verbose=False):
    '''
    Get maximum number of category levels
    '''
    max_num_levels = series.str.split(sep).apply(len).max()

    if verbose:
        print("Max Number of Category Levels: {}".format(max_num_levels))

    return max_num_levels


def flatten_categories(category_series, df=None, drop_col=None, sep='>'):
    '''
    Take in Series with categories in string format and flatten into columns

     Keyword Arguments:
    ------------------
    * category_series - series with string of categories
    * df - pandas dataframe
    * drop_col - name of column with nested categories (string)
    * sep - puncuation that separates categories


    Returns:
    --------
    a pandas dataframe
    '''

    num_levels = get_num_of_levels(category_series, sep=sep)

    col_labels = ['L' + str(i) for i in range(1, num_levels+1)]


    category_levels = pd.DataFrame(category_series.str.split(sep).values.tolist(), columns=col_labels)
    category_levels.fillna(value=pd.np.nan, inplace=True)

    if df is not None:
        merged_df = pd.merge(df,category_levels, left_index=True, right_index=True).drop(drop_col, axis=1)

        return merged_df
    else:
        return category_levels


def search_cons_status(cons_searches, raw_searches):
    '''
    Get status on number of unique search terms
    '''

    num_searches = len(raw_searches)
    new_num_searches = len(set(cons_searches))

    num_cons = num_searches - new_num_searches

    per_reduction = round((num_cons/num_searches)*100,1)

    print(f'New Number of Searches: {new_num_searches}')
    print(f'Number of Consolidated Searches: {num_cons}')
    print(f'Percent Reduction: {per_reduction}%')
