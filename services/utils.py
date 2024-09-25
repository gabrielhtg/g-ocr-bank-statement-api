from flask import json
import numpy as np

def get_value_percentage(percentage, value):
    return int((percentage / 100) * value)

def order_points(pts):
    pts = pts.reshape(4, 2)
    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    return rect

def calculate_distance_between_2_points(p1, p2):
    dis = ((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2) ** 0.5
    return dis

def clean_data (array) :
    temp = []
    
    for e in array:
        col_nol = ''
        col_satu = ''
        col_dua = ''
        col_tiga = ''
        col_empat = ''
        current_filename = None
        current_page = None
        
        for e_ in e:
            if e_['col'] == 0:
                col_nol = col_nol + ' ' +  e_['text']

            if e_['col'] == 1:
                col_satu = col_satu + ' ' + e_['text']

            if e_['col'] == 2:
                col_dua = col_dua + ' ' + e_['text']

            if e_['col'] == 3:
                col_tiga = col_tiga + ' ' + e_['text']

            if e_['col'] == 4:
                col_empat = col_empat + ' ' + e_['text']

            current_filename = e_['filename']
            current_page = e_['page']

        if col_tiga != '' :
            col_tiga = (col_tiga
                        .strip()
                        .replace(' ', '')
                        .replace(',', '')
                        .replace('o', '0')
                        .replace('O', '0')
                        .replace('u', 'D')
                        .replace('.', ''))

            if 'D' in col_tiga or 'B' in col_tiga:
                if col_tiga[-1] == '2':
                    col_tiga = col_tiga[:-1] + 'B'

                col_tiga = col_tiga[:-2]
                col_tiga = col_tiga[:-2] + '.' + col_tiga[-2:]

                try:
                    col_tiga = "{:,.2f}".format(float(col_tiga)) + ' DB'
                except ValueError:
                    col_tiga = col_tiga + ' !!'

            else:
                col_tiga = col_tiga[:-2] + '.' + col_tiga[-2:]
                try:
                    col_tiga = "{:,.2f}".format(float(col_tiga))
                except ValueError:
                    col_tiga = col_tiga + ' !!'

        if col_empat != '' :
            col_empat = (col_empat.replace(' ', '')
                         .replace(',', '')
                         .replace('o', '0')
                         .replace('O', '0')
                         .replace('.', ''))

            col_empat = col_empat[:-2] + '.' + col_empat[-2:]
            col_empat = "{:,.2f}".format(float(col_empat))

        temp.append(
            [
                col_nol.strip(),
                col_satu.strip(),
                col_dua.strip(),
                col_tiga,
                col_empat,
                current_filename.strip(),
                current_page
            ]
        )
        
    return temp

def contains_number(s):
    return any(char.isdigit() for char in s)