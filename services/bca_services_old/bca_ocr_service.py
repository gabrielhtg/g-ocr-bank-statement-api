from werkzeug.utils import secure_filename
import os
import cv2 as cv
import easyocr
import numpy as np

from services.utils.calculate_distance_between_two_points import calculateDistanceBetweenTwoPoints
from services.utils.get_value_percentage import getValuePercentage
from services.utils.is_contain_number import isContainNumber
from services.utils.is_current_page_the_right_bank_statement_type import isCurrentPageTheRightBankStatementType
from services.utils.order_points import orderPoints

def doOcrBca(images_array, app, bank_statement_type, is_zip):
    list_baris = []
    list_sub_data = []
    data_baris = []
    data_baris_temp = []
    most_left_table = None

    most_left_tanggal = None
    most_right_tanggal = None
    threshold_tanggal = None
    percentage_threshold_tanggal = None

    most_left_keterangan = None
    most_right_keterangan = None
    threshold_keterangan = None
    percentage_threshold_keterangan = None

    most_left_cbg = None
    most_right_cbg = None
    threshold_cbg = None
    percentage_threshold_cbg = None

    most_left_mutasi = None
    most_right_mutasi = None
    threshold_mutasi = None
    percentage_threshold_mutasi = None

    most_left_saldo = None
    most_right_saldo = None
    threshold_saldo = None
    percentage_threshold_saldo = None
    page = 0
    is_transaction_data_done = False

    # is_current_page_correct adalah variable yang berisikan nilai kebenaran dari pagi ini sudah sesuai dengan
    # tipe bank statement atau belum
    is_current_page_correct = None
    
    data = {}
    
    '''
        Loop ini berguna untuk move antar halaman. Kalau iterasi bertambah, 
        maka masuk ke halaman selanjutnya
    '''
    for i in images_array:
        # ini adalah case jika file yang diupload adalah file zip
        if is_zip :
            filename = i
            file_path = os.path.join(app.config['EXTRACT_FOLDER'], filename)

        # ini adalah case ketika fila yang diupload adalah gambar
        else:
            file = i
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

        # ini digunakan untuk menentukan page / halaman saat ini dengan menjumlahkannya
        page += 1

        #Setiap masuk ke dalam page baru, maka perlu text count yang sudah dicek direset lagi ke 0
        checked_text_count = 0

        print('Processing {}'.format(filename))

        img = cv.imread(file_path)

        gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

        thres = cv.threshold(gray_img, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)[1]

        contours, hierarchy = cv.findContours(thres, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        image_with_all_contours = img.copy()
        cv.drawContours(image_with_all_contours, contours, -1, (0, 255, 0), 3)

        rectangular_contours = []
        for contour in contours:
            peri = cv.arcLength(contour, True)
            approx = cv.approxPolyDP(contour, 0.02 * peri, True)
            if len(approx) == 4:
                rectangular_contours.append(approx)
        image_with_only_rectangular_contours = img.copy()
        cv.drawContours(image_with_only_rectangular_contours, rectangular_contours, -1, (0, 255, 0), 3)

        max_area = 0
        contour_with_max_area = None
        for contour in rectangular_contours:
            area = cv.contourArea(contour)
            if area > max_area:
                max_area = area
                contour_with_max_area = contour
        gambar_setelah_contour_max = img.copy()
        cv.drawContours(gambar_setelah_contour_max, [contour_with_max_area], -1, (0, 255, 0), 3)

        contour_with_max_area_ordered = orderPoints(contour_with_max_area)

        existing_image_width = None

        image_with_points_plotted = img.copy()
        for point in contour_with_max_area_ordered:
            point_coordinates = (int(point[0]), int(point[1]))
            image_with_points_plotted = cv.circle(image_with_points_plotted, point_coordinates, 10, (0, 0, 255), -1)

            existing_image_width = img.shape[1]

        existing_image_width_reduced_by_10_percent = int(existing_image_width * 0.9)

        distance_between_top_left_and_top_right = calculateDistanceBetweenTwoPoints(contour_with_max_area_ordered[0],
                                                                                      contour_with_max_area_ordered[1])
        distance_between_top_left_and_bottom_left = calculateDistanceBetweenTwoPoints(
            contour_with_max_area_ordered[0],
            contour_with_max_area_ordered[3])
        aspect_ratio = distance_between_top_left_and_bottom_left / distance_between_top_left_and_top_right
        new_image_width = existing_image_width_reduced_by_10_percent
        new_image_height = int(new_image_width * aspect_ratio)

        # logika perspective transform
        pts1 = np.float32(contour_with_max_area_ordered)
        pts2 = np.float32([[0, 0], [new_image_width, 0], [new_image_width, new_image_height], [0, new_image_height]])
        matrix = cv.getPerspectiveTransform(pts1, pts2)
        perspective_corrected_image = cv.warpPerspective(img, matrix, (new_image_width, new_image_height))

        img = cv.cvtColor(perspective_corrected_image, cv.IMREAD_GRAYSCALE)
        _, result = cv.threshold(img, 127, 255, cv.THRESH_BINARY)
        reader = easyocr.Reader(['id', 'en'], gpu=True)
        text_ = reader.readtext(img)

        img_height, img_width, temp = img.shape

        if percentage_threshold_tanggal is not None:
            threshold_tanggal = img_width * percentage_threshold_tanggal

        if percentage_threshold_keterangan is not None:
            threshold_keterangan = img_width * percentage_threshold_keterangan

        if percentage_threshold_cbg is not None:
            threshold_cbg = img_width * percentage_threshold_cbg

        if percentage_threshold_mutasi is not None:
            threshold_mutasi = img_width * percentage_threshold_mutasi

        if percentage_threshold_saldo is not None:
            threshold_saldo = img_width * percentage_threshold_saldo

        # Inisialisasi nilai x yang ekstrem
        min_x = float('inf')
        max_x = float('-inf')
        wait_for_awal = 'false'

        save_data = False
        
        tipeRekening = None
        kcp = None
        pemilikRekening = None
        titikBawahPemilikRekening = None
        nomorRekening = None
        periode = None
        mataUang = None
        
        before = None

        thresholdBawahBoxPertama = None
        thresholdKananBoxPertama = None

        # Iterasi melalui hasil OCR
        for bbox, ocr_text, score in text_:
            
            bbox = [[int(coord[0]), int(coord[1])] for coord in bbox]
            
            current_width = bbox[1][0] - bbox[0][0]
            most_right_box = bbox[0][0] + current_width
            most_left_box = bbox[0][0]
            most_top_box = bbox[1][1]
            most_bottom_box = bbox[2][1]
            
            checked_text_count += 1
            
            if checked_text_count == 2 :
                tipeRekening = ocr_text
            
            if checked_text_count == 3:
                kcp = ocr_text
                thresholdBawahBoxPertama = most_top_box + int(0.10 * img_height)
                thresholdKananBoxPertama = most_left_box + int(0.408 * img_width)
                
            if checked_text_count > 3 :
                if most_left_box < thresholdKananBoxPertama and most_top_box < thresholdBawahBoxPertama :
                    if pemilikRekening == None:
                        titikBawahPemilikRekening = most_bottom_box
                        pemilikRekening = ocr_text
                    
                    else :
                        if most_top_box < titikBawahPemilikRekening:
                            pemilikRekening = pemilikRekening + ' ' + ocr_text
                            
                if most_left_box > thresholdKananBoxPertama and most_top_box < thresholdBawahBoxPertama and mataUang == None :
                    if 'ing' in before.lower():
                        nomorRekening = ocr_text
                    
                    if 'iode' in before.lower() :
                        periode = ocr_text
                        
                    if 'uang' in before.lower() :
                        mataUang = ocr_text                      

            # ini adalah pengecekan terhadap tipe dari bank statement
            # saat ini threshold yang digunakan adalah 5
            # 5 bisa disesuaikan sesuai dengan kondisi
            if not is_current_page_correct:
                if checked_text_count < 10:
                    is_current_page_correct = isCurrentPageTheRightBankStatementType(bank_statement_type,
                                                                                            ocr_text)

            if str(ocr_text).lower() == 'saldo':
                save_data = True
                continue

            if save_data:
                # Ambil koordinat x dari titik pertama pada bbox
                x1, y1 = bbox[0]
                x2, y2 = bbox[2]

                # Cek apakah ini adalah teks paling kiri
                if x1 < min_x:
                    min_x = x1

                # Cek apakah ini adalah teks paling kanan
                if x2 > max_x:
                    max_x = x2
            
            before = ocr_text

        # Hasil akhir
        content_width = max_x - min_x

        save_data = False
        before = ''
        wait_for_saldo = False

        for t in text_:
            bbox, ocr_text, score, *test = t
            
            bbox = [[int(coord[0]), int(coord[1])] for coord in bbox]

            if str(ocr_text).lower() == 'saldo' and len(data_baris) < 1:
                save_data = True
                continue

            current_width = bbox[1][0] - bbox[0][0]
            most_right_box = bbox[0][0] + current_width
            most_left_box = bbox[0][0]
            # most_top_box = bbox[1][1]

            if save_data:
                if is_transaction_data_done:
                    if isContainNumber(ocr_text):
                        list_sub_data.append(ocr_text)
                        continue

                if page == len(images_array) and 'saldo' in str(ocr_text).lower():
                    data_baris_temp = data_baris.copy()
                    wait_for_awal = True

                if page == len(images_array) and 'awal' in str(ocr_text).lower() and wait_for_awal:
                    list_baris.append(data_baris_temp.copy())
                    data_baris_temp.clear()
                    is_transaction_data_done = True

                if ('awal' in str(ocr_text).lower() and before in str(ocr_text).lower()) or 'ber' in str(
                        ocr_text).lower():
                    save_data = False

                    if len(data_baris) > 0:
                        list_baris.append(data_baris.copy())
                        data_baris.clear()
                    continue

                # bagian tanggal
                if threshold_tanggal is None:
                    threshold_tanggal = most_right_box + getValuePercentage(1, content_width)
                    percentage_threshold_tanggal = threshold_tanggal / img_width

                if most_right_box < threshold_tanggal:
                    if wait_for_saldo:
                        wait_for_saldo = False

                    if len(data_baris) > 0:
                        list_baris.append(data_baris.copy())
                        data_baris.clear()

                    # titik_kiri = most_top_box
                    data_baris.append(
                        {
                            'text': ocr_text,
                            'col': 0,
                            'page': page,
                            'filename': filename
                        }
                    )

                if most_left_table is None:
                    most_left_table = most_left_box

                if most_left_tanggal is None:
                    most_left_tanggal = most_left_box
                    most_right_tanggal = most_right_box

                else:
                    if most_left_box < threshold_tanggal:
                        if most_left_box < most_left_tanggal:
                            most_left_tanggal = most_left_box
                            most_left_table = most_left_tanggal

                            if most_right_tanggal < most_right_box < threshold_tanggal:
                                most_right_tanggal = most_right_box

                    else:
                        # bagian keterangan
                        if threshold_keterangan is None:
                            threshold_keterangan = threshold_tanggal + getValuePercentage(42, content_width)
                            percentage_threshold_keterangan = threshold_keterangan / img_width

                        if most_right_box < threshold_keterangan:
                            data_baris.append(
                                {
                                    'text': ocr_text,
                                    'col': 1,
                                    'page': page,
                                    'filename': filename
                                }
                            )

                        if most_left_keterangan is None:
                            most_left_keterangan = most_left_box
                            most_right_keterangan = most_right_box

                        else:
                            if most_left_box < threshold_keterangan:
                                if most_left_box < most_left_keterangan:
                                    most_left_keterangan = most_left_box

                                    if most_right_keterangan < most_right_box < threshold_keterangan:
                                        most_right_keterangan = most_right_box

                                if threshold_keterangan > most_right_box > most_right_keterangan:
                                    most_right_keterangan = most_right_box

                            else:
                                # bagian cbg
                                if threshold_cbg is None:
                                    threshold_cbg = threshold_keterangan + getValuePercentage(8, content_width)
                                    percentage_threshold_cbg = threshold_cbg / img_width

                                if most_right_box < threshold_cbg:
                                    data_baris.append(
                                        {
                                            'text': ocr_text,
                                            'col': 2,
                                            'page': page,
                                            'filename': filename
                                        }
                                    )

                                if most_left_cbg is None and most_left_box < threshold_cbg:
                                    most_left_cbg = most_left_box

                                    if most_right_box < threshold_cbg:
                                        most_right_cbg = most_right_box

                                else:
                                    if most_left_box < threshold_cbg:
                                        if most_left_box < most_left_cbg:
                                            most_left_cbg = most_left_box

                                            if most_right_cbg is not None and most_right_cbg < most_right_box < threshold_cbg:
                                                most_right_cbg = most_right_box

                                    else:
                                        # bagian mutasi
                                        if threshold_mutasi is None:
                                            threshold_mutasi = threshold_cbg + getValuePercentage(27, content_width)
                                            percentage_threshold_mutasi = threshold_mutasi / img_width

                                        if most_right_box < threshold_mutasi:
                                            wait_for_saldo = True
                                            data_baris.append(
                                                {
                                                    'text': ocr_text,
                                                    'col': 3,
                                                    'page': page,
                                                    'filename': filename
                                                }
                                            )

                                        if most_left_mutasi is None and most_left_box < threshold_mutasi:
                                            most_left_mutasi = most_left_box

                                            if most_right_box < threshold_mutasi:
                                                most_right_mutasi = most_right_box

                                        else:
                                            if most_left_box < threshold_mutasi:
                                                if most_left_box < most_left_mutasi:
                                                    most_left_mutasi = most_left_box

                                                if most_right_mutasi is not None and most_right_mutasi < most_right_box < threshold_mutasi:
                                                    most_right_mutasi = most_right_box

                                            else:
                                                # bagian saldo
                                                if threshold_saldo is None:
                                                    threshold_saldo = max_x + getValuePercentage(5, content_width)
                                                    percentage_threshold_saldo = threshold_saldo / img_width

                                                if most_right_box < threshold_saldo:
                                                    wait_for_saldo = False
                                                    data_baris.append(
                                                        {
                                                            'text': ocr_text,
                                                            'col': 4,
                                                            'page': page,
                                                            'filename': filename
                                                        }
                                                    )

                                                if most_left_saldo is None and most_left_box < threshold_saldo:
                                                    most_left_saldo = most_left_box

                                                    if most_right_box < threshold_saldo:
                                                        most_right_saldo = most_right_box

                                                else:
                                                    if most_left_box < threshold_saldo:
                                                        if most_left_box < most_left_saldo:
                                                            most_left_saldo = most_left_box

                                                        if most_right_saldo is not None and most_right_saldo < most_right_box < threshold_saldo:
                                                            most_right_saldo = most_right_box

                before = ocr_text

        if is_current_page_correct is not None:
            if not is_current_page_correct:
                return 400

        is_current_page_correct = False
        # os.remove(file_path)
        
    data['tipe_rekening'] = tipeRekening
    data['list_baris'] = list_baris
    data['list_sub_data'] = list_sub_data
    data['kcp'] = kcp
    data['pemilik_rekening'] = pemilikRekening
    data['nomor_rekening'] = nomorRekening
    data['periode'] = periode
    data['mata_uang'] = mataUang

    return data
