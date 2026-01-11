from typing import List
import sys
import pandas as pd
import numpy as np

from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import OneHotEncoder


class WeekdayImputer(BaseEstimator, TransformerMixin):
    """ Impute missing values in 'weekday' column by extracting dayname from 'dteday' column """

    def __init__(self, variable: str, date_var:str):

        if not isinstance(variable, str):
            raise ValueError("variable name should be a string")
        if not isinstance(date_var, str):
            raise ValueError("date variable name should be a string")

        self.variable = variable
        self.date_var = date_var
    
    def fit(self, X: pd.DataFrame, y: pd.Series = None):
        # we need the fit statement to accomodate the sklearn pipeline
        return self
    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        X = X.copy()
        # convert 'dteday' column to Datetime datatype
        X[self.date_var] = pd.to_datetime(X[self.date_var], format='%Y-%m-%d')
        # only compute day names where date is present and weekday is missing
        wkday_null_mask = X[self.variable].isnull() & X[self.date_var].notna()
        if wkday_null_mask.any():
            X.loc[wkday_null_mask, self.variable] = (
                X.loc[wkday_null_mask, self.date_var].dt.day_name().str[:3]
            )

        # drop 'dteday' column after imputation
        X.drop(self.date_var, axis=1, inplace=True)

        return X


class WeathersitImputer(BaseEstimator, TransformerMixin):
    """ Impute missing values in 'weathersit' column by replacing them with the most frequent category value """

    def __init__(self, variable: str):

        if not isinstance(variable, str):
            raise ValueError("variable name should be a string")

        self.variable = variable

    def fit(self, X: pd.DataFrame, y: pd.Series = None):
        # we need the fit statement to accomodate the sklearn pipeline 
        X = X.copy()
        self.fill_value = X[self.variable].mode()[0]

        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        X = X.copy()
        X[self.variable] = X[self.variable].fillna(self.fill_value)

        return X    


class Mapper(BaseEstimator, TransformerMixin):
    """
    Ordinal categorical variable mapper:
    Treat column as Ordinal categorical variable, and assign values accordingly
    """

    def __init__(self, variable:str, mappings:dict):

        if not isinstance(variable, str):
            raise ValueError("variable name should be a string")

        self.variable = variable
        self.mappings = mappings

    def fit(self, X: pd.DataFrame, y: pd.Series = None):
        # we need the fit statement to accomodate the sklearn pipeline
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        X = X.copy()
        # map values; keep NA as NaN by casting to float so integer
        # missing values don't raise during astype conversion
        X[self.variable] = X[self.variable].map(self.mappings).astype(float)

        return X


class OutlierHandler(BaseEstimator, TransformerMixin):
    """
    Change the outlier values: 
        - to upper-bound, if the value is higher than upper-bound, or
        - to lower-bound, if the value is lower than lower-bound respectively.
    """

    def __init__(self, variable:str):

        if not isinstance(variable, str):
            raise ValueError("variable name should be a string")

        self.variable = variable

    def fit(self, X: pd.DataFrame, y: pd.Series = None):
        # we need the fit statement to accomodate the sklearn pipeline
        X = X.copy()
        q1 = X.describe()[self.variable].loc['25%']
        q3 = X.describe()[self.variable].loc['75%']
        iqr = q3 - q1
        self.lower_bound = q1 - (1.5 * iqr)
        self.upper_bound = q3 + (1.5 * iqr)
        
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        X = X.copy()
        
        for i in X.index:
            if X.loc[i, self.variable] > self.upper_bound:
                X.loc[i, self.variable]= self.upper_bound
            if X.loc[i, self.variable] < self.lower_bound:
                X.loc[i, self.variable]= self.lower_bound

        return X


class age_col_tfr(BaseEstimator, TransformerMixin):
    """Transformer to fill missing age values using the median of the column.

    This class is named to match test expectations (`age_col_tfr`) and
    implements sklearn's `fit`/`transform` interface.
    """

    def __init__(self, variables: str):
        if not isinstance(variables, str):
            raise ValueError("`variables` should be a string naming the age column")
        self.variables = variables

    def fit(self, X: pd.DataFrame, y: pd.Series = None):
        X = X.copy()
        # compute median ignoring NaNs
        self.fill_value_ = X[self.variables].median()
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        X = X.copy()
        X[self.variables] = X[self.variables].fillna(self.fill_value_)
        return X


class WeekdayOneHotEncoder(BaseEstimator, TransformerMixin):
    """ One-hot encode weekday column """

    def __init__(self, variable:str):

        if not isinstance(variable, str):
            raise ValueError("variable name should be a string")

        self.variable = variable
        self.encoder = OneHotEncoder(sparse_output=False)

    def fit(self, X: pd.DataFrame, y: pd.Series = None):
        # we need the fit statement to accomodate the sklearn pipeline
        X = X.copy()
        self.encoder.fit(X[[self.variable]])
        # Get encoded feature names
        self.encoded_features_names = self.encoder.get_feature_names_out([self.variable])
        
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        X = X.copy()
        # ensure dtype is object so encoder handles string categories and NaNs
        X[self.variable] = X[self.variable].astype(object)
        if X[self.variable].isna().all():
            # no valid values to encode; produce zero columns to match
            # encoder output shape
            encoded_weekdays = np.zeros((X.shape[0], len(self.encoded_features_names)))
        else:
            encoded_weekdays = self.encoder.transform(X[[self.variable]])
        # Append encoded weekday features to X
        X[self.encoded_features_names] = encoded_weekdays

        # drop 'weekday' column after encoding
        X.drop(self.variable, axis=1, inplace=True)        

        return X

