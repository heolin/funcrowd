import pandas as pd
from modules.aggregation.models.aggregations.base import BaseAggregation, AggregationResult


class VotingAggregation(BaseAggregation):

    def _logic(self, df):
        columns = [c for c in list(df) if c not in ['user', 'item']]
        df_results = pd.DataFrame()
        for index, group in df.groupby('item'):
            for column in columns:
                counts = group[column].value_counts()
                answer = counts.index[0]
                probability = counts.iloc[0] / counts.sum()
                df_results.loc[index, column] = answer
                df_results.loc[index, column + '_prob'] = probability
                df_results.loc[index, column + '_support'] = len(counts)

        results = []
        for item_id, row in df_results.iterrows():
            data = dict(row)
            results.append(AggregationResult(item_id, data))
        return results
