import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import pickle
import holidays
from scipy import stats
import xgboost as xgb
import lightgbm as lgb
import optuna
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import mean_squared_error
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OrdinalEncoder
from sklearn.metrics import precision_score, recall_score, f1_score,accuracy_score, roc_auc_score
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from lightgbm import LGBMClassifier
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split



def load_model(model_path):
    model_final = None

    if os.path.exists(model_path):
        print('Model is already')

        with open(model_path, 'rb') as f:
            model_final = pickle.load(f)

    return model_final

def save_model(model, model_path):
    with open(model_path, "wb") as f:
        pickle.dump(model, f)


def categorical_encoding(df, categorical_variables):
    """
    This function takes a DataFrame and a list of categorical variables and encodes them using one-hot encoding.
    
    Parameters:
    df (DataFrame): The input DataFrame with the categorical variables.
    categorical_variables (list): A list of categorical variables to be encoded.
    
    Returns:
    DataFrame: The DataFrame with the categorical variables encoded.
    """
    # Create a copy of the DataFrame
    df_copy = df.copy()
    
    # Perform one-hot encoding for each categorical variable
    for var in categorical_variables:
        df_copy[var] = df_copy[var].astype('category')
        
    # Perform one-hot encoding
    df_copy = pd.get_dummies(df_copy, columns=categorical_variables)
                
    return df_copy



def encode_all_ordinal(df, times_columns, days_columns, numbers_columns, feelings_columns):
    # Define mappings
    times_mapping = {
        '0 time': 0, 
        '1 time': 1, 
        '2 or 3 times': 2, 
        '4 or 5 times': 3, 
        '6 or 7 times': 4, 
        '8 or 9 times': 5, 
        '10 or 11 times': 6, 
        '12 or more times': 7
    }
    
    days_mapping = {
        '0 days': 0, 
        '1 or 2 days': 1, 
        '3 to 5 days': 2, 
        '6 to 9 days': 3, 
        '10 or more days': 4
    }
    
    numbers_mapping = {
        0: 0, 
        1: 1, 
        2: 2, 
        '3 or more': 3
    }
    
    feelings_mapping = ['Never', 'Rarely', 'Sometimes', 'Most of the time', 'Always']
    
    # Apply mappings
    for col in times_columns:
        df[col] = df[col].map(times_mapping)
    
    for col in days_columns:
        df[col] = df[col].map(days_mapping)
    
    for col in numbers_columns:
        df[col] = df[col].map(numbers_mapping)
    
    categories = [feelings_mapping for _ in feelings_columns]
    encoder = OrdinalEncoder(categories=categories)
    df[feelings_columns] = encoder.fit_transform(df[feelings_columns])
    
    return df


def encode_binary(df, columns):
    mapping = {'Yes': 1, 'No': 0}
    for col in columns:
        df[col] = df[col].map(mapping)
    return df



def extract_age(age_str):
    """
    Extract age from a string.

    Args:
    age_str (str): Age string in the format "XX years old".

    Returns:
    int: Age as an integer.
    """
    return int(age_str.split()[0])

# Pipeline Functions
class DataFrameSelector(BaseEstimator, TransformerMixin):
    def __init__(self, attribute_names):
        self.attribute_names = attribute_names

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        for column in self.attribute_names:
            if column not in X.columns:
                X[column] = np.nan
        return X[self.attribute_names]
    

class AgeExtractor(BaseEstimator, TransformerMixin):
    def __init__(self, column):
        self.column = column

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X[self.column] = X[self.column].apply(extract_age)
        return X

class OrdinalEncoderCustom(BaseEstimator, TransformerMixin):
    def __init__(self, times_columns, days_columns, numbers_columns, feelings_columns):
        self.times_columns = times_columns
        self.days_columns = days_columns
        self.numbers_columns = numbers_columns
        self.feelings_columns = feelings_columns

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return encode_all_ordinal(X, self.times_columns, self.days_columns, self.numbers_columns, self.feelings_columns)

class BinaryEncoderCustom(BaseEstimator, TransformerMixin):
    def __init__(self, columns):
        self.columns = columns

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return encode_binary(X, self.columns)
    
class CategoricalEncoder(BaseEstimator, TransformerMixin):
    def __init__(self, categorical_variables):
        self.categorical_variables = categorical_variables

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return categorical_encoding(X, self.categorical_variables)



# Define the pipeline
def create_pipeline():
    pipeline = Pipeline(steps=[
    ('age_extractor', AgeExtractor('Custom_Age')),
    ('ordinal_encoder', OrdinalEncoderCustom(times_columns=['Physical_fighting','Physically_attacked'], days_columns=['Miss_school_no_permission'], numbers_columns=['Close_friends'], 
                                             feelings_columns=['Felt_lonely','Other_students_kind_and_helpful','Parents_understand_problems'])),
    ('binary_encoder', BinaryEncoderCustom(columns=['Bullied_not_on_school_property_in_past_12_months','Cyber_bullied_in_past_12_months',
                                                    'Most_of_the_time_or_always_felt_lonely','Missed_classes_or_school_without_permission','Were_underweight','Were_overweight','Were_obese'])),
    ('categorical_encoder', CategoricalEncoder(categorical_variables=['Sex'])),
    ('selector', DataFrameSelector(attribute_names=['Bullied_not_on_school_property_in_past_12_months','Cyber_bullied_in_past_12_months',
                                                    'Custom_Age','Physically_attacked','Physical_fighting','Felt_lonely','Close_friends','Miss_school_no_permission','Other_students_kind_and_helpful',
                                                    'Parents_understand_problems','Most_of_the_time_or_always_felt_lonely','Missed_classes_or_school_without_permission','Were_underweight',
                                                    'Were_obese']))
])

    return pipeline

def make_prediction(input_data):
    model = load_model('models/xgboost_model.pkl')
    print(model)


    # Convert the input data to a DataFrame
    df = pd.DataFrame([input_data])
    print(f"Input data: {df}")

    # Create the pipeline
    pipeline = create_pipeline()
    
    if 'Student ID' in df.columns:
        # Use the pipeline to transform the input data
        transformed_df = pipeline.fit_transform(df.drop('Student ID', axis=1))
        
    else:
        # Use the pipeline to transform the input data
        transformed_df = pipeline.fit_transform(df)
        
    print(f"Transformed data: {transformed_df}")

    # Use the model to make predictions
    predictions = model.predict(transformed_df)
    
    df.rename(columns={'Student iD': 'Record'}, inplace=True)
    
    df['Bullied_on_school_property_in_past_12_months'] = predictions
    
    return df


def plot_feature_importance():
    # Get the model
    model = load_model('models/xgboost_model.pkl')

    # Plot feature importance
    ax = xgb.plot_importance(model)
    ax.figure.tight_layout()
    return ax.figure

def plot_gain():
    model = load_model('models/xgboost_model.pkl')
    # Plotting Gain
    fig, ax = plt.subplots(figsize=(10, 8))
    xgb.plot_importance(model, ax=ax, importance_type='gain', title='Feature Gain')
    plt.tight_layout()
    return fig




