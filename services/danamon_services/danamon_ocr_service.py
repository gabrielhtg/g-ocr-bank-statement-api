import os
from matplotlib.dviread import Page
from werkzeug.utils import secure_filename

from services.danamon_services.get_analysis_data import danamonAnalysisData
from services.danamon_services.get_total_debit import getTotalDebit
from services.danamon_services.get_total_kredit import getTotalKredit
from services.danamon_services.get_transaction_data import danamonGetTransactionData
from services.utils.correct_perspective import correctPerspective
from services.utils.do_orc_easyocr import doEasyOcr
from services.utils.get_image_height import getImageHeight
from services.utils.get_image_width import getImageWidth

def doOcrDanamon (imageArray, app, bankStatementType) :
    nomorNasabah = None
    cabang = None
    pemilikRekening = None
    alamat = None

    page = 0
    
    data = {}
    thbHeaderTable = None
    thbTable = None
    thrTableCol1 = None
    thrTableCol2 = None
    thrTableCol3 = None
    thrTableCol4 = None
    thrTableCol5 = None
    thrTableCol6 = None

    currentRow = 0
    textData = []
    textWithCol = {}
    transactionData = []
    
    periodeLaporan = None
    nomorNasabah = None
    cabang = None
    pemilikRekening = None
    alamat = None

    thrPeriodeLaporan = None
    thbPeriodeLaporan = None
    thtPeriodeLaporan = None
    thlPeriodeLaporan = None

    thrNomorNasabah = None
    thbNomorNasabah = None
    thtNomorNasabah = None
    thlNomorNasabah = None

    thrCabang = None
    thbCabang = None
    thtCabang = None
    thlCabang = None

    thrPemilikRekening = None
    thbPemilikRekening = None
    thtPemilikRekening = None
    thlPemilikRekening = None

    thrAlamat = None
    thbAlamat = None
    thtAlamat = None
    thlAlamat = None
    
    currentRow = 0
    
    for e in imageArray:
        page += 1
        textData.clear()
        
        if isinstance(e, str) :
            filename = secure_filename(e)
            file_path = os.path.join(app.config['EXTRACT_FOLDER'], filename)
            perspectiveCorrectedImage = correctPerspective(file_path)
            
        else :
            file = e
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            perspectiveCorrectedImage = correctPerspective(file_path)
        
        print('Processing', filename)
        
        lebarGambar = getImageWidth(perspectiveCorrectedImage)
        tinggiGambar = getImageHeight(perspectiveCorrectedImage)

        # text_ merupakan semua teks hasil ocr dari gambar
        # tapi masih bukan hasil akhir
        text_ = doEasyOcr(perspectiveCorrectedImage)

        for e in text_ :
            bbox, text, score = e
    
            bbox = [[int(coord[0]), int(coord[1])] for coord in bbox]
                    
            rb = bbox[1][0]
            lb = bbox[0][0]
            tb = bbox[1][1]
            bb = bbox[2][1]
            cw = lb + int(abs(rb - lb) / 2)
            ch = tb + int(abs(bb - tb) / 2)
            
            if page == 1 :
                if 'per' in text.lower() :
                    thrPeriodeLaporan = lb + int(0.3 * lebarGambar)
                    thlPeriodeLaporan = rb + int(0.005 * lebarGambar)
                    thbPeriodeLaporan = bb + int(0.005 * tinggiGambar)
                    thtPeriodeLaporan = tb - int(0.005 * tinggiGambar)
                    
                if (
                    ('no' in text.lower() and 'aba' in text.lower()) or
                    ('no' in text.lower() and 'bah' in text.lower())
                ) :
                    thrNomorNasabah = lb + int(0.3 * lebarGambar)
                    thlNomorNasabah = rb + int(0.005 * lebarGambar)
                    thbNomorNasabah = bb + int(0.005 * tinggiGambar)
                    thtNomorNasabah = tb - int(0.005 * tinggiGambar)
                    
                if (
                    'cab' in text.lower() and 'ng' in text.lower()
                ) :
                    thrCabang = lb + int(0.4 * lebarGambar)
                    thlCabang = rb + int(0.005 * lebarGambar)
                    thbCabang = bb + int(0.005 * tinggiGambar)
                    thtCabang = tb - int(0.005 * tinggiGambar)
                    
                    thrPemilikRekening = thrCabang
                    thrAlamat = thrCabang
                    thbAlamat = thbCabang + int(0.12 * tinggiGambar)
                    
                if thrPeriodeLaporan != None:
                    if (
                        (cw < thrPeriodeLaporan) 
                        and (ch <= thbPeriodeLaporan) 
                        and (ch >= thtPeriodeLaporan)
                        and (cw > thlPeriodeLaporan)
                    ) :
                        if periodeLaporan == None :
                            periodeLaporan = text
                            
                        else :
                            if periodeLaporan == None:
                                periodeLaporan = text
                            
                            else :
                                periodeLaporan = periodeLaporan + ' - ' + text
                                
                if thrNomorNasabah != None:
                    if (
                        (cw < thrNomorNasabah) 
                        and (ch <= thbNomorNasabah) 
                        and (ch >= thtNomorNasabah)
                        and (cw > thlNomorNasabah)
                    ) :
                        if nomorNasabah == None :
                            nomorNasabah = text
                            
                if thrCabang != None and cabang == None:
                    if (
                        (cw < thrCabang) 
                        and (ch <= thbCabang) 
                        and (ch >= thtCabang)
                        and (cw > thlCabang)
                    ) :
                        if cabang == None  :
                            cabang = text
                            
                if cabang != None:
                    if pemilikRekening == None:
                        if cw < thrPemilikRekening and ch > thbCabang:
                            pemilikRekening = text
                            
                    else :
                        if cw < thrAlamat and ch < thbAlamat :
                            if alamat == None:
                                    alamat = text
                                    
                            else :
                                alamat = alamat + ' ' + text
                
            if ('efektif' in text.lower() and ch > int(0.5 * tinggiGambar)) :
                break
            
            if ('akhir' in text.lower() and 'aporan' in text.lower()) :
                break
            
            if 'ket' in text.lower() and 'rang' in text.lower() and currentRow == 0:
                thbHeaderTable = tb + int(0.021 * tinggiGambar)
                thbTable = tb + int(0.575 * tinggiGambar)
                thrTableCol1 = rb - int(0.115 * tinggiGambar)
                thrTableCol2 = thrTableCol1 + int(0.029 * tinggiGambar)
                thrTableCol3 = thrTableCol2 + int(0.13 * tinggiGambar)
                thrTableCol4 = thrTableCol3 + int(0.12 * tinggiGambar)
                thrTableCol5 = thrTableCol4 + int(0.094 * tinggiGambar)
                thrTableCol6 = thrTableCol5 + int(0.1 * tinggiGambar)
                
            if thbHeaderTable != None and tb > thbHeaderTable and ch < thbTable :
                if currentRow == 0 :
                    currentRow += 1

                textWithCol['text'] = text
                
                if (cw < thrTableCol1) :
                    currentRow += 1    
                    textWithCol['col'] = 1
                    textWithCol['row'] = currentRow
                
                if (cw > thrTableCol1 and cw < thrTableCol2) :
                    textWithCol['col'] = 2
                    textWithCol['row'] = currentRow
                    
                if (cw > thrTableCol2 and cw < thrTableCol3) :
                    textWithCol['col'] = 3
                    textWithCol['row'] = currentRow
                    
                if (cw > thrTableCol3 and cw < thrTableCol4) :
                    textWithCol['col'] = 4
                    textWithCol['row'] = currentRow
                    
                if (cw > thrTableCol4 and cw < thrTableCol5) :
                    textWithCol['col'] = 5
                    textWithCol['row'] = currentRow
                    
                if (cw > thrTableCol5 and cw < thrTableCol6) :
                    textWithCol['col'] = 6
                    textWithCol['row'] = currentRow
                    
                if (cw > thrTableCol6) :
                    textWithCol['col'] = 7
                    textWithCol['row'] = currentRow
                    
                textData.append(textWithCol.copy())
        # if not isBankStatementCorrect :
        #     return 400
        
        transactionData.extend(danamonGetTransactionData(textData, filename))
    
    data['pemilik_rekening'] = pemilikRekening
    data['nomor_nasabah'] = nomorNasabah
    data['cabang'] = cabang
    data['pemilik_rekening'] = pemilikRekening
    data['alamat'] = alamat
    data['periode_laporan'] = periodeLaporan
    data['transaction_data'] = transactionData
    data['total_debet'] = getTotalDebit(transactionData)
    data['total_kredit'] = getTotalKredit(transactionData)
    data['analytics_data'] = danamonAnalysisData(data['transaction_data'])
    return data