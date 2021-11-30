import os

from flask import Flask, jsonify, abort, make_response, request,render_template
import requests
import json
import time
import sys
import pandas as pd
import pickle
import numpy as np


app = Flask(__name__)
model = pickle.load(open('Models/Project_RF_no_dummies.pkl','rb'))

@app.route('/')
def home():
    return render_template('index1.html')


@app.route('/predict',methods=['POST'])
def predict():

    data_index_input = [x for x in request.form.values()]

    data = {
        'years': int(data_index_input[0]),
        'chars': data_index_input[1],
        'metalls': data_index_input[2],
        'conditions': data_index_input[3]
    }
    df = pd.DataFrame(data, index=['1'])
    condition_dictionary = {
        'MS64': 'Good',
        'F+F': 'Good',
        'Au/Proof': 'Bad',
        'пресс': 'Perfect',
        'FVF': 'Good',
        'Proof': 'Bad',
        'PROOF': 'Bad',
        'VF': 'Good',
        'VF-': 'Good',
        'VF+': 'Good',
        'F-VF': 'Good',
        'XF-': 'Perfect',
        'XF': 'Perfect',
        'VF-XF': 'Perfect',
        'F': 'Good',
        'F-F+': 'Good',
        'XF+': 'Perfect',
        'F-': 'Bad',
        'AU': 'Perfect',
        'UNC': 'Perfect',
        'F+': 'Good',
        'VG': 'Bad',
        'G': 'Bad',
        'аUNC': 'Perfect',
        'ХF-': 'Perfect',
        'VG-': 'Bad',
        'G-': 'Bad',
        'XF-UNC': 'Perfect',
        'F+F+': 'Good',
        'XF-AU': 'Perfect',
        'G+': 'Bad',
        'MS-62 BN': '',
        'Unc': 'Perfect',
        'VF-VF+': 'Good',
        'XF--': 'Perfect',
        'aUNC': 'Perfect',
        ' ': 'Bad',
        '': 'Bad',
        'AU Details': 'Perfect',
        'XF Details': 'Perfect',
        'VF20': 'Good',
        'MS63': 'Bad',
        'VF det': 'Good',
        'XF details': 'Perfect',
        'MS60': 'Bad',
        'MS61': 'Bad',
        'AU-55': 'Perfect',
        'AU53': 'Perfect',
        'AU 58': 'Perfect',
        'AU 55': 'Perfect',
        'AU55': 'Perfect',
        'AU58': 'Perfect',
        'XF-40': 'Perfect',
        'AU-58': 'Perfect',
        'XF45': 'Perfect',
        'EF40': 'Perfect',
        'EF40 Details': 'Perfect',
        'VG10': 'Bad',
        'PF61': 'Perfect',
        'VG8': 'Bad',
        'VF25': 'Perfect',
        'F12': 'Good'

    }
    char_dictionary = {
        'Коронация Николая II': 'юбилей',
        'В честь коронации Императора Николая II': 'юбилей',
        'O': 'OK',
        'О': 'OK',
        '': 'Без_букв',
        '*': '**',
        '300-летие дома Романовых': 'юбилей',
        'МW': 'MW',
        'МД': 'ММД',
        'Коронация_Н2': 'юбилей',
        'Коронация Александра III': 'юбилей',
        '300 лет дому Романовых': 'юбилей',
        'OK': 'ОК',
        '(^^)': '**',
        '\tна коронацию Александра III': 'юбилей',
        '?': 'Без_букв',
        'б/б': 'Без_букв',
        'В память': 'юбилей',
        'OK ILL': 'OK',
        'OK': 'ОК',
        'Портрет работы Дмитриева': 'юбилей',
        'Московский тип. Портрет Л. Дмитриева': 'юбилей'
    }
    metalls_dictionary = {
        'б/м': 'bad_metall',
        'бм': 'bad_metall',
        'Br': 'bad_metall',
        '': 'bad_metall'
    }

    df.conditions = df.conditions.replace(condition_dictionary)
    df.chars = df.chars.replace(char_dictionary)
    df.metalls = df.metalls.replace(metalls_dictionary)

    df['chars'] = df['chars'].map({
        'СПБ': 0,
        'АГ': 1,
        '**': 2,
        'Без_букв': 3,
        'На': 4,
        'ФЗ': 5,
        '(ЭБ)': 6,
        'ММД': 7,
        'СМ': 8,
        'MW': 9,
        'юбилей': 4,
        'ОК': 10,
        '(АР)': 11,
        'ВС': 12,
        'К': 13,
        'OK': 10})
    df['metalls'] = df['metalls'].map({
        'Ag': 0,
        'bad_metall': 1,
        'Au': 1})
    df['conditions'] = df['conditions'].map({
        'Perfect': 0,
        'Good': 1,
        'Bad': 2})

    prediction = model.predict(df)
    output = round(prediction[0], 2)

    return render_template('index1.html',prediction_text ='Предсказанная стоимость монеты : {}'.format(output))



@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'code':'PAGE_NOT_FOUND'},404))


@app.errorhandler(500)
def server_error(error):
    return make_response(jsonify({'code': 'INTERNAL_SERVER_ERROR'}), 500)


if __name__ == '__main__':
    app.run(debug=True)
