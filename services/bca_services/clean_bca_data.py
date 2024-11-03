import statistics

def cleanBcaData (array) :
    arr_temp = []
    count_db = 0
    count_cr = 0
    sum_db = 0.0
    sum_cr = 0.0
    list_cr = []
    list_db = []
    
    for e in array:
        col_zero = ''
        col_one = ''
        col_two = ''
        col_three = ''
        col_four = ''
        current_filename = None
        current_page = None
        
        for e_ in e:
            if e_['col'] == 0:
                col_zero = col_zero + ' ' +  e_['text']

            if e_['col'] == 1:
                col_one = col_one + ' ' + e_['text']

            if e_['col'] == 2:
                col_two = col_two + ' ' + e_['text']

            if e_['col'] == 3:
                col_three = col_three + ' ' + e_['text']

            if e_['col'] == 4:
                col_four = col_four + ' ' + e_['text']

            current_filename = e_['filename']
            current_page = e_['page']

        # print('Col three :', col_three)
        # print('Halaman   :', current_filename)
        # print()

        if col_three != '' :
            col_three = (col_three
                        .strip()
                        .replace(' ', '')
                        .replace(',', '')
                        .replace('o', '0')
                        .replace('O', '0')
                        .replace('u', 'D')
                        .replace('.', ''))

            if 'D' in col_three or 'B' in col_three:
                if col_three[-1] == '2':
                    col_three = col_three[:-1] + 'B'

                col_three = col_three[:-2]
                col_three = col_three[:-2] + '.' + col_three[-2:]

                try :
                    sum_db += float(col_three)
                except ValueError:
                    return 400
                    
                list_db.append(float(col_three))

                try:
                    col_three = "{:,.2f}".format(float(col_three)) + ' DB'
                except ValueError:
                    col_three = col_three + ' !!'

            else:
                col_three = col_three[:-2] + '.' + col_three[-2:]
                sum_cr += float(col_three)
                list_cr.append(float(col_three))

                try:
                    col_three = "{:,.2f}".format(float(col_three))
                except ValueError:
                    col_three = col_three + ' !!'

        if col_four != '' :
            col_four = (col_four.replace(' ', '')
                         .replace(',', '')
                         .replace('o', '0')
                         .replace('O', '0')
                         .replace('.', ''))

            col_four = col_four[:-2] + '.' + col_four[-2:]
            col_four = "{:,.2f}".format(float(col_four))

        if 'DB' in col_three:
            count_db += 1

        if ' CR ' in col_one or 'CR ' in col_one or ' CR' in col_one or 'KR ' in col_one or 'KR ' in col_one or ' KR' in col_one :
            count_cr += 1

        arr_temp.append(
            [
                col_zero.strip(),
                col_one.strip(),
                col_two.strip(),
                col_three,
                col_four,
                current_filename.strip(),
                current_page
            ]
        )

    return {
        'data_transaction' : arr_temp,
        'analitics_data' : {
            'count_db' : count_db,
            'count_cr' : count_cr,
            'sum_cr' : "{:,.2f}".format(sum_cr),
            'raw_sum_cr' : sum_cr,
            'raw_sum_db' : sum_db,
            'sum_db' : "{:,.2f}".format(sum_db),
            'avg_cr' : "{:,.2f}".format(statistics.mean(list_cr)),
            'avg_db' : "{:,.2f}".format(statistics.mean(list_db)),
            'min_db' : "{:,.2f}".format(min(list_db)),
            'min_cr' : "{:,.2f}".format(min(list_cr)),
            'max_db' : "{:,.2f}".format(max(list_db)),
            'max_cr' : "{:,.2f}".format(max(list_cr)),
            'net_balance' : "{:,.2f}".format(sum_cr - sum_db)
        }
    }