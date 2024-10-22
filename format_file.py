import pandas as pd
import geopandas as gpd


#----------
#Formats unemployment DataFrame to get rid of unwanted data
#----------
#Parameters:
#   og_df: pd.DataFrame
#     That is the DataFrame is going to get formated
#Returns:
#   formated_df: pd.DataFrame
#     The DataFrame, only with the needed data
#----------
def format_df(og_df: pd.DataFrame) -> pd.DataFrame:
    #Obtain only the unemployment rate data
    formated_df = og_df[og_df['Nombre'].str.contains(r'^Tasa de paro de la población\. .*\. Ambos sexos\. Total\. $', regex=True)]

    #Create a 'Provincia' column for easy map creating
    formated_df['Provincia'] = formated_df['MetaData'].apply(get_province)

    unwanted_cols = ['COD','Nombre','T3_Unidad','T3_Escala','MetaData']
    for col in unwanted_cols:
        formated_df.pop(col)

    #Get rid of unwanted data on 'Data' column
    formated_df['Data'] = formated_df['Data'].apply(filter_data)
   
    #Puts 'Provincia' as the first column, just for esthetic porpuses
    col = formated_df.pop('Provincia')
    formated_df.insert(0,'Provincia',col)
    
    #Uncoment the print instructions for visual understanding of the following

    #Creates a row for each dictionari on Data column. 
    #So now we have a different row for each year-quarter and province
    df_exploded = formated_df.explode('Data').reset_index(drop=True)
    #print(df_exploded)

    #Creates a column for each key on 'Data' column.
    #So now we have 'T3_Periodo', 'Anyo', 'Valor' columns instead of 'Data' column containing them all
    df_normalized = pd.concat([df_exploded.drop(columns=['Data']), pd.json_normalize(df_exploded['Data'])], axis=1)
    #print(df_normalized)

    #Calculates the mean of all four quarters unemployment value of each year.
    formated_df = df_normalized.groupby(['Provincia', 'Anyo'], as_index=False)['Valor'].mean()
    #print(formated_df)

    return formated_df


#----------
#Gets the province name off of the 'MetaData' column
#----------
#Parameters:
#   meta_data: list[dict]
#     A list of dictionaries where each province name is located
#Returns:
#   data.get('Nombre'): str
#     The province name of each 'MetaData' column
#----------
def get_province(meta_data: list[dict]) -> str:
    for data in meta_data:
        if data.get('T3_Variable') == 'Provincias':
            return data.get('Nombre')

    return None


#----------
#Creates a new 'Data' column with only the needed data
#----------
#Parameters:
#   data_list: list[dict]
#     A list of dictionaries with diferent type of data, some of them we don't need
#Returns:
#   new list[dict]
#     Returns a new list of dictionaries but filtered with only the data we want
#----------
def filter_data(data_list: list[dict]) -> list[dict]:
    return [{key: record[key] for key in ['T3_Periodo','Anyo','Valor']} for record in data_list]
