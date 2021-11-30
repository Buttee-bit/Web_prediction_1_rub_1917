import pickle
import pandas as pd


PATH_TO_MODELS = 'Model/'
filename = 'model.py'

model = PATH_TO_MODELS + filename

def load_model():
    load_model = pickle.load(open(model,'rb'))
    return load_model


# model = load_model()

target = []

def get_prediction(name,year,char,metall,condition):
    all_columns = ['name','year','metall','condition']
    lst = [name,year,char,metall,condition]
    df = pd.DataFrame([lst],columns=all_columns)


    # df = df.astype(float)
    # Работа с данными преоброзование их к
    # years	 prices	 names_1 рубль	chars_(АР)	chars_(ЭБ)	chars_**	chars_MW	chars_АГ	chars_Без_букв	chars_ВС	...	chars_СМ	chars_СПБ	chars_ФЗ	chars_юбилей	metalls_Ag	metalls_Au	metalls_bad_metall	conditions_Bad	conditions_Good	conditions_Perfect
    #
    pass

def launch_task(name,year,char,metall,condition):
    
    pred_model = get_prediction(name,year,char,metall,condition)

    pass

