import pandas as pd
import re
from addPrefixToColumn import addPrefixToColumn

def encodeProductionCompany(df, filter=False, threshold=0.0005):
    """
    MultipleHotEncode column production_companies
    Json loads does not work here
    Regex to extract needed values
    Seperate them with | for MultipleHotEncoding
    :param df: DataFrame
    :param filter: boolean if set should be filtered by threshold
    :param threshold: threshold for filter
    :return: encoded DataFrame
    """

    new_values = []
    indices = []
    for index, row in df.iterrows():
        new_value = row["production_companies"].replace("[", "").replace("]", "").replace("{\'name\': ", "").replace("}", "").replace("\'", "")
        new_value = re.sub(", id: \d+", "", new_value)
        new_value = new_value.replace(", ", "|")
        new_values.append(new_value)
        indices.append(index)
    new_values_encoded = pd.Series(new_values,index=indices).str.get_dummies()
    if(filter):
        new_values_encoded = filterWithThreshold(new_values_encoded, threshold)
    new_values_encoded = addPrefixToColumn(new_values_encoded, "company")
    return new_values_encoded


def encodeProductionCompanyToOne(df, filter=False, threshold=0.0005):
    """
    OneHotEncode column production_compnaies
    Json loads does not work here
    Regex to extract first value
    :param df: DataFrame
    :param filter: boolean if set should be filtered by threshold
    :param threshold: threshold for filter
    :return: encoded DataFrame
    """
    new_values = []
    for index, row in df.iterrows():
        new_value = row["production_companies"].replace("[", "").replace("]", "").replace("{\'name\': ", "").replace(
            "}", "").replace("\'", "")
        new_value = re.sub(", id: \d+", "", new_value)
        new_value = new_value.split(", ")[0]
        new_values.append(new_value)
    new_values_encoded = pd.get_dummies(new_values)
    if(filter):
        new_values_encoded = filterWithThreshold(new_values_encoded, threshold)
    new_values_encoded = addPrefixToColumn(new_values_encoded, "company")
    return new_values_encoded

def filterWithThreshold(df, threshold):
    """
    Filters encoded columns.
    Takes only columns that have at least the threshold % ones
    :param df: oneHotEncoded DataFrame
    :param threshold: Percentage of ones in column
    :return: filtered DataFrame
    """
    size = len(df)
    for column in df:
        if not (df[column].value_counts()[1]/size >= threshold):
            df.drop(column, axis=1, inplace = True)