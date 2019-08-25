from easygui import *
import pandas as pd
from datetime import date
import datetime
import sys
import argparse


arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('-d', '--database', help='the directory of database csv file', required=True)
args = arg_parser.parse_args()

database = args.database

weekday = datetime.datetime.today().weekday()
timenow = datetime.datetime.now().time()

#read in menu from csv database
menu = pd.read_csv(database)
for index, row in menu.iterrows():
    row['start_time']=datetime.time(row['start_hour'],row['start_min'])
    menu['start_time']=row['start_time']
    row['end_time']=datetime.time(row['end_hour'],row['end_min'])
    menu['end_time']=row['end_time']

#set role for log in
msg = """Please select a role to log in:

admin -> For store owners to set menu
user -> For customers to view menu"""
role = buttonbox(msg, choices=['admin','user'])

while role=="admin":
    password = passwordbox(title='Admin login',msg="please enter admin password(hint:admin)")
    while not(password=="admin"):
        password = passwordbox(title='Admin login',msg="Your password is wrong. Please enter again. (hint:admin)")
    while password=="admin":
        action = buttonbox("Welcome Admin! Would you like to add/delete menu?", choices=['add menu','delete menu'])


        while action =="delete menu":
            msg = """           Enter details for the dish that you would like to delete:
                    (Dish Name use _ to replace space : eg. chicken_rice)"""
            title = "Menu Deleting"
            fieldNames = ["Canteen Name","Store Name","Dish Name"]
            fieldValues = []  # we start with blanks for the values
            fieldValues = multenterbox(msg,title, fieldNames)
            cn = str(fieldValues[0])
            cs = str(fieldValues[1])
            food = str(fieldValues[2])
            menu_drop = menu.loc[menu['canteen_name']==cn]
            menu_drop = menu.loc[menu['canteen_store']==cs]
            menu_drop = menu.loc[menu['food']==food]
            if menu_drop.empty:
                next_step = buttonbox("The dish in not found. Would you like to enter details again?",choices=['enter again','exit'])
                if next_step =='enter again':
                    continue
                else:
                    sys.quit()
            else:
                menu.append(menu_drop).drop_duplicates(keep=False).to_csv(database,index=False)

                mmm = """your dish setting has been successfully deleted. Would you like to delete another dish?"""
                next_step = buttonbox(mmm, choices=['delete another dish','exit'])
                if next_step =="exit":
                    sys.quit()


        while action =="add menu":
            msg = """           Set your dish timing:
            (Dish Name use _ to replace space : eg. chicken_rice/french_fries...)
            (Availble Day Format : eg. monday/tuesday/wedneday...)
            (Timing Format : eg. 10:00/22:30...)"""
            title = "Menu Setting"
            fieldNames = ["Canteen Name","Store Name","Dish Name","Availble Day","Start time","End time"]
            fieldValues = []  # we start with blanks for the values
            fieldValues = multenterbox(msg,title, fieldNames)
            fieldValues
            daydict = {"monday":0,"tuesday":1,"wednesday":2,"thursday":3,"friday":4,"saturday":5,"sunday":6}
            start = fieldValues[4].split(":")
            start_hour = int(start[0])
            start_min = int(start[1])
            end = fieldValues[5].split(":")
            end_hour = int(end[0])
            end_min = int(end[1])
            menu = menu.append(pd.Series([fieldValues[0], fieldValues[1], fieldValues[2], daydict.get(fieldValues[3]),start_hour,start_min,end_hour,end_min,'',''], index=menu.columns), ignore_index=True)
            menu = menu.drop_duplicates(subset ={'canteen_name', 'canteen_store', 'food', 'day'},keep='last')
            menu.to_csv(database,index=False)

            mm = """your dish setting has been successfully set. Would you like to set another dish?"""
            next_step = buttonbox(mm, choices=['set another dish','exit'])
            if next_step =="exit":
                sys.quit()


while role=="user":
#choose a canteen
    can_choices = list(set(menu.canteen_name.tolist()))
    canteen = choicebox("Please select a canteen","select canteen",can_choices)
    df_canteen = menu.loc[menu['canteen_name']==canteen]
    #choose a store from the canteen
    store_choices = list(set(df_canteen.canteen_store.tolist()))
    store = choicebox('Please select a store in '+canteen,'select store',store_choices)
    df_store = df_canteen.loc[df_canteen['canteen_store']==store]

#show availble courses
    df_available = df_store.loc[df_store['day']==weekday]
    df_available=df_available.loc[df_available['start_time']<timenow]
    df_available=df_available.loc[df_available['end_time']>timenow]
    df_available

    s = ''
    for record in df_available['food']:
        s = s+record+'\r\n'

    if not(s==''):
        msgbox(msg = s,title ="These are availble dishes @"+store,ok_button = "back")
    else:
        msgbox(msg = "Sorry, there is no availble dishes in " + store,ok_button = "back")
