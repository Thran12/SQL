import tkinter as tk
from tkinter import *
from tkinter import filedialog
import pyodbc
import regex as re
import pandas as pd

window=tk.Tk()
window.geometry("620x350")
window.title("Ein Matching Tool")
window['background']='light blue'

server='ALI'
database_name = 'EIN_Master' 
cnxn=pyodbc.connect(driver='{ODBC Driver 17 for SQL Server}',server='(local)',database=database_name,trusted_connection='yes')
cursor=cnxn.cursor()
#select a universal font for our matching tool

def browse_file():
    global file_path
    file_path=filedialog.askopenfilename()
    selected_file_text.delete(1.0, tk.END)
    selected_file_text.insert(tk.END, file_path)
label2 = Label(window,font=('Calibri Bold',9),bg='light blue')
label2.place(x=248,y=110)


#smar
#drop unnecessary tables from tables from file.So there should be certain details
def clean_junk():
    pass

def Upload_to_database():
    label2.config(text="Uploading File to database")
    with open(file_path,'r+',encoding='cp437') as f:
        text=f.readline()
    columns_name=[re.sub('/','',i3) for i3 in [re.sub("-"," ",i2) for i2 in [re.sub('"','',i1).strip()  for i1 in text.split(',')]]]
    global new_columns_name,table_name
    new_columns_name=['_'.join(i1.split(' ')) if ' ' in i1 else i1 for i1 in columns_name]
    old_string=''
    for i1 in new_columns_name:
        old_string+=str(f'{i1} nvarchar(max), '.strip())
    new_string=old_string[:-1]
    table_name=file_path.split('/')[-1].split('.')[0]
    table_name=table_name.split(' ') if ' ' in table_name else table_name
    if type(table_name)==list:
        table_name='_'.join(table_name)
    sql_query_creation=f'create table {table_name} ( {new_string} )'    
    cursor.execute(sql_query_creation)
    cursor.commit()
    add_table_data=f"Bulk insert {table_name} from '{file_path}' with ( FIRSTROW=2, FIELDTERMINATOR = ',' , ROWTERMINATOR = '\n')"
    cursor.execute(add_table_data)
    cursor.commit()
    label2.config(text="File Uploaded.")

def lose_match():
    label_join_query.config(text="Doing Join Query")
    join_query=f'select * from ein_database ed inner join {table_name} t1 on len(ed.Company,1,8) = len(t1.Company_name,1,8) \
                    and ed.State=t1.State'
    cursor.execute(join_query)
    list_=cursor.fetchall()
    column_names=[column[0] for column in cursor.description]
    dataframe=pd.DataFrame(list_,columns=column_names)
    dataframe.to_csv('C://Users//kk//OneDrive//Desktop//Ein Matching Tool//lose_match_result.csv')
    delete_junk=f'drop table if exists {table_name}'
    cursor.execute(delete_junk)
    cursor.commit()
    label_join_query.config(text="Join Query Successful")

def mid_match():
    label_join_query.config(text="Doing Join Query")
    join_query=f'select * from ein_database ed inner join {table_name} t1 on substring(ed.Company,1,12) =  \
                    substring(t1.Company_name,1,12) \
                    and ed.State=t1.State and ed.City=t1.City'
    cursor.execute(join_query)
    list_=cursor.fetchall()
    column_names=[column[0] for column in cursor.description]
    dataframe=pd.DataFrame(list_,columns=column_names)
    dataframe.to_csv('C://Users//kk//OneDrive//Desktop//Ein Matching Tool//mid_match_result.csv')
    #columns name needed to be taken care to get the result
    delete_junk=f'drop table if exists {table_name}'
    cursor.execute(delete_junk)
    cursor.commit()
    label_join_query.config(text="Join Query Successful")

def tight_match():
    label_join_query.config(text="Doing Join Query")
    join_query=f'selet * from ein_database ed inner join {table_name} t1 on substring(ed.Company,1,15) = substring(t1.Company_name,1,15) and ed.City \
                =t1.City and ed.State=t1.State'
    cursor.execute(join_query)
    list_=cursor.fetchall()
    column_names=[column[0] for column in cursor.description]
    dataframe=pd.DataFrame(list_,columns=column_names)
    dataframe.to_csv('C://Users//kk//OneDrive//Desktop//Ein Matching Tool//tight_match_result.csv')
    delete_junk=f'drop table if exists {table_name}'
    cursor.execute(delete_junk)
    cursor.commit()
    label_join_query.config(text="Join Query Successful")

def Dynamic_match():
    label_join_query.config(text="Doing Join Query")
    join_query=f"select distinct * from ein_database ed inner join {table_name} \
        t1 on ed.Company=substring(t1.Company_name,1,len(ed.Company)) \
            where FEIN not in ('0','NULL')"
    cursor.execute(join_query)
    list_=cursor.fetchall()
    column_names=[column[0] for column in cursor.description]
    dataframe=pd.DataFrame(list_,columns=column_names)
    delete_junk=f'drop table if exists {table_name}'
    cursor.execute(delete_junk)
    cursor.commit()
    dataframe.to_csv('C://Users//kk//OneDrive//Desktop//Ein Matching Tool//dynamic_match_result.csv')
    label_join_query.config(text="Join Query Successful")

selected_file_text = tk.Text(window, height=1.3, width=60,font=('Calibri',12))
selected_file_text.place(x=40,y=25)
#button place
browse_button=tk.Button(window,text="Browse",command=browse_file)
browse_button.place(x=512,y=23)

# browse and select button are decided to be here

button1 = tk.Button(window, text="Upload to Database",height=2,width=20,command=Upload_to_database)
button1.place(x=240,y=60)

button2 = tk.Button(window, text="Lose Match",height=2,width=20)
button2.place(x=120,y=150)
button3 = tk.Button(window, text="Mid Match",height=2,width=20)
button3.place(x=120,y=230)
button4 = tk.Button(window, text="Tight Match",height=2,width=20)
button4.place(x=320,y=150)
button5 = tk.Button(window, text="Dynamic Match",height=2,width=20,command=Dynamic_match)
button5.place(x=320,y=230)

def open_popup():
    top=Toplevel(window)
    top.geometry("400x200")
    top.title("Read me Instructions")
    Label(top, text= "Join Keys should be named in a specific order like", font=('Calibri',10)).place(x=75,y=80)
    Label(top, text= "    Company Name ,  City , State   ", font=('Calibri',10)).place(x=80,y=105)
    
button6=tk.Button(window,text="Read Instructions",command=open_popup,font=('Calibri',8))
button6.place(x=490,y=180)
label_join_query = Label(window,font=('Calibri Bold',16),bg="light blue")
label_join_query.place(x=245,y=300)
window.mainloop()