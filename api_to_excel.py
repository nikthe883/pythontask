import pandas as pd
import requests
from datetime import date
import os.path
from dependencies import *


def api_call():
    # request for the data
    data = requests.get(API)
    json_data = data.json()
    return json_data



def data_cleaning():
    '''
    Gets data from Api, clears the data as per requirements and stores it to pickle file
    The file is named vehicles.pkl
    '''

    # calls the api_call function
    json_data = api_call()

    # data to df, sorts the values by column, removes all None values in hu columns and
    # stores the cleared data to pickle file on script directory as vehicles.pkl
    df = pd.DataFrame(json_data)
    df.sort_values(by=['gruppe'], inplace=True)
    df = df[df['hu'].notna()]
    df.to_pickle('vehicles.pkl')


def get_current_date():
    '''
    Returns the current date in ISO format.
    '''
    current_date = date.today()
    current_date.isoformat()

    return current_date


def vehicles_api_to_excel(*args):
    '''
    Takes string arguments as column names and returns an excel file in script directory.
    '''

    for item in args:
        if type(item) is not str:
            raise Exception(f"Only strings are allowed. You have provided {type(item)}")


    # check if pickle file exist
    if os.path.isfile("vehicles.pkl"):
        current_date = get_current_date()
        df = pd.read_pickle("vehicles.pkl")

        # gets columns names to a list
        columns_list = df.columns.tolist()

        # checks if any arguments are column names and appends them to a list of all desired columns
        mandatory_columns = ['rnr']
        [mandatory_columns.append(column_name) for column_name in args if column_name in columns_list]

        # gets the desired columns and outputs excel file
        df = df[[x for x in mandatory_columns]]
        df.to_excel(f'vehicles_{current_date}.xlsx')

    else:
        data_cleaning()
        vehicles_api_to_excel(*args)
