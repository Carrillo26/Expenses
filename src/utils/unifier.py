import pandas as pd

def unify_dataframes(*dataframes):
    """
    Unify multiples Json into a DataFrame.
    :param dataframes: DataFrames list to unify.
    :return: Unify DataFrame.
    """
    return pd.concat(dataframes, ignore_index=True)



def save_to_excel(df, output_path):
    """
    .
    :param df: 
    :param output_path: 
    """
    df.to_excel(output_path, index=False)
    print(f'DataFrame saved in {output_path}')