import pandas as pd
import numpy as np
from sklearn import preprocessing

'''
Build product hierarchy dictionary.
'''


class Hierarchy:
    '''
    Build parent, child dictionary 
    '''
    
    def __init__(self, data, num_levels):
        '''
        Keyword Arguments:
        ------------------
        * data - flattened pandas dataframe
        * num_levels - number of product category levels
        '''
        
        self.data= data
        self.num_levels = num_levels
        self.level_cols = list(data.columns[-self.num_levels:])
        self.was_fit=False
        
        
    def fit_transform(self):
        '''
        Fit (Encode Notes) and Transform (Categories to Ids in Dataframe)
        '''
        # get notes
        self.nodes = list(pd.unique(self.data.iloc[:,-self.num_levels:].values.ravel()))
        
        #encode nodes
        le = preprocessing.LabelEncoder()
        le.fit(self.nodes)
        
        #save mapping
        self.node2id = dict(zip(le.classes_, le.transform(le.classes_)))
        self.id2node = dict(zip(le.transform(le.classes_),le.classes_))
        
        self.data_encoded = self.data
        
        for col in self.level_cols:
            self.data_encoded[col] = pd.Series(le.transform(self.data_encoded[col].to_list()))
            
        return self
    
        
    def get_mappings(self, map_direction='encode'):
        '''
        Get mapping for nodes and ids (and ids to nodes)
        
        Returns:
        --------
        dictionary
        '''
        
        if map_direction == 'encode':
            return self.node2id
        elif map_direction == 'decode':
            return self.id2node

    
    def get_parent_child_dict(self):
        '''
        Construct encoded parent - child dictionary
        (e.g. {2: [5,9,22]...})
        
        Returns:
        --------
        dictionary
        '''
         
        # Function to group category levels with sliding window 
        def parent_child_dict(col_lst):
            for i in range(len(col_lst)-1):
                j=i+1
                yield(self.data_encoded.groupby(col_lst[i])[col_lst[j]].apply(set).to_dict())
            
        level_dicts = list(parent_child_dict(self.level_cols))
        
        # Add dictionaries together
        for i in range(1, len(level_dicts)):
            level_dicts[0].update(level_dicts[i])
    
        self.prod_map = level_dicts[0]
        
        return self.prod_map