
import pandas as pd

class Evaluator:

    def __init__(self, eval_data_file=None, metric=None):
        self.eval_data_file = eval_data_file
        self.metric=metric
        self.run()

    def load_data(self, data_folder='raw', data_type='csv'):
        if data_type == 'csv':
            df = pd.read_csv('../data/{}/{}'.format(data_folder, self.eval_data_file))
        self.eval_data = df

    def get_xy(self):
        self.eval_target = self.eval_data.groupby('Search_term')['Display_name'].apply(list)

    def hit_rate(self, top_n_pred, top_n_act:

        hits = len(set(top_n_pred,top_n_act))
        total = len(top_n_pred) + len(top_n_act) - hits

        hit_score = hits/total


    def run(self):
        self.load_data()
        self.get_xy()
