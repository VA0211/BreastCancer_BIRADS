import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

def df_train_test_split(df):
    train_mask = df['split'] == 'training'

    train_df = df[train_mask]
    test_df = df[~train_mask]

    return train_df, test_df

def main(df):
    train_df, test_df = df_train_test_split(df)
    # print(len(train_df))
    # print(len(test_df))
    new_train = train_df.groupby(['breast_density','breast_birads','view_position','laterality']).sample(frac=0.75)
    full_df = pd.concat([new_train,test_df], axis=0)
    new_train.to_csv('./Data/train_df.csv', index=False)
    full_df.to_csv('./Data/full_df.csv', index=False)

if __name__ == "__main__":
    df = pd.read_csv('./Data/breast-level_annotations.csv')
    main(df)