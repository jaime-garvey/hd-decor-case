import pandas as pd
import numpy as np

from sklearn import preprocessing

class Tree:
    '''
    Build parent, child dictionary 
    '''
    def __init__(self, data, num_levels):
        '''
        
        Keyword Arguments:
        ------------------
        
        '''
        self.data= data
        self.num_levels = num_levels
        self.level_cols = data.columns[-self.num_levels]
        self.was_fit=False
        
    def fit(self):
        # get notes
        self.nodes = pd.unique(self.data.iloc[:,-self.num_levels].values.ravel())
        
        #encode nodes
        le = preprocessing.LabelEncoder()
        le.fit(list(self.nodes))
        
        #save mapping
        self.node2id = dict(zip(le.classes_, le.transform(le.classes_)))
        self.id2node = dict(zip(le.transform(le.classes_),le.classes_))
        
        return self
        
    def get_mappings(self, map_direction='encode'):
        '''
        Get mapping for nodes and ids
        '''
        if map_direction == 'encode':
            return self.node2id
        elif map_direct == 'decode':
            return self.id2node
        else: 
            return self.node2id, self.id2node
        
        
    def transform(self):
        '''
        '''
        if not self.was_fit:
            raise Error("Need to fit data first")
            
        data_new = self.data
        for col in self.cols:
            data_new[col] = pd.Series(le.transform(data_new[col].to_list()))
            
        return self.data_new
            
        
    def fit_transform(self):
        '''
        '''
        return self.fit().transform()
        
    
    def get_parent_child_dict(self):
        '''
        '''
        def parent_child_dict(col_lst):
            for i in range(len(col_lst)-1):
                j=i+1
                yield(self.data_new.groupby(col_lst[i])[col_lst[j]].apply(set).to_dict())
            
        level_dicts = list(parent_child_dict(self.level_cols))
        
        # Add dictionaries together
        for i in range(1, len(level_dicts)):
            level_dicts[0].update(level_dicts[i])
    
        self.prod_map = level_dicts[0]
        
        return self.prod_map
        
        
        
            
