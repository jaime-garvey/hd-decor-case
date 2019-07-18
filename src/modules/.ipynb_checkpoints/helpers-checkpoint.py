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