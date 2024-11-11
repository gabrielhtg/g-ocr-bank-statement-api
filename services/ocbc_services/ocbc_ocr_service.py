import os
from matplotlib.dviread import Page
from werkzeug.utils import secure_filename

from services.ocbc_services.get_analysis_data import ocbcAnalysisData
from services.ocbc_services.get_total_debit import getTotalDebit
from services.ocbc_services.get_total_kredit import getTotalKredit
from services.ocbc_services.get_transaction_data import ocbcGetTransactionData
from services.utils.correct_perspective import correctPerspective
from services.utils.do_orc_easyocr import doEasyOcr
from services.utils.get_image_height import getImageHeight
from services.utils.get_image_width import getImageWidth

def doOcrOcbc (imageArray, app, bankStatementType) :
    pemilikRekening = None
    alamat = None
    nomorRekening = None
    cabang = None
    periode = None
    tanggalPercetakan = None
    mataUang = None

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

    thrPemilikRekening = None
    thbPemilikRekening = None
    thtPemilikRekening = None
    thlPemilikRekening = None

    thrAlamat = None
    thbAlamat = None
    thtAlamat = None
    thlAlamat = None

    thrNomorRekening = None
    thbNomorRekening = None
    thtNomorRekening = None
    thlNomorRekening = None

    thrCabang = None
    thbCabang = None
    thtCabang = None
    thlCabang = None

    thrPeriode = None
    thbPeriode = None
    thtPeriode = None
    thlPeriode = None

    thrTanggalPercetakan = None
    thbTanggalPercetakan = None
    thtTanggalPercetakan = None
    thlTanggalPercetakan = None

    thrMataUang = None
    thbMataUang = None
    thtMataUang = None
    thlMataUang = None
    
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
                if 'mor' in text.lower() and 'ning' in text.lower() and ch < (0.5 * tinggiGambar) :
                    thrNomorRekening = lb + int(0.45 * lebarGambar)
                    thlNomorRekening = rb + int(0.05 * lebarGambar)
                    thbNomorRekening = bb + int(0.005 * tinggiGambar)
                    thtNomorRekening = tb - int(0.005 * tinggiGambar)
                    
                if ('cabang' in text.lower() or 'bang' in text.lower()) and ch < (0.5 * tinggiGambar) :
                    thrCabang = lb + int(0.45 * lebarGambar)
                    thlCabang = rb + int(0.113 * lebarGambar)
                    thbCabang = bb + int(0.005 * tinggiGambar)
                    thtCabang = tb - int(0.005 * tinggiGambar)
                    
                if ('periode' in text.lower()) and ch < (0.5 * tinggiGambar) :
                    thrPeriode = lb + int(0.45 * lebarGambar)
                    thlPeriode = rb + int(0.113 * lebarGambar)
                    thbPeriode = bb + int(0.005 * tinggiGambar)
                    thtPeriode = tb - int(0.005 * tinggiGambar)
                    
                if ('gal' in text.lower()) and ('cet' in text.lower()) and ch < (0.5 * tinggiGambar) :
                    thrTanggalPercetakan = lb + int(0.45 * lebarGambar)
                    thlTanggalPercetakan = rb + int(0.018 * lebarGambar)
                    thbTanggalPercetakan = bb + int(0.005 * tinggiGambar)
                    thtTanggalPercetakan = tb - int(0.005 * tinggiGambar)
                    
                if ('mata' in text.lower()) and ('ng' in text.lower()) and ch < (0.5 * tinggiGambar) :
                    thrMataUang = lb + int(0.45 * lebarGambar)
                    thlMataUang = rb + int(0.018 * lebarGambar)
                    thbMataUang = bb + int(0.005 * tinggiGambar)
                    thtMataUang = tb - int(0.005 * tinggiGambar)
                    
                if ('koran' in text.lower() and 'kening' in text.lower() and ch < 0.1 * tinggiGambar) : 
                    thlPemilikRekening = lb - int(0.4 * lebarGambar)
                    thrPemilikRekening = lb - int(0.01 * lebarGambar)
                    thtPemilikRekening = tb + int(0.045 * tinggiGambar)
                    thbPemilikRekening = tb + int(0.067 * tinggiGambar)
                    
                    thtAlamat = thbPemilikRekening
                    thlAlamat = thlPemilikRekening
                    thrAlamat = thrPemilikRekening
                    thbAlamat = thtAlamat + int(0.08 * tinggiGambar)
                    
                if thrMataUang != None:
                    if (
                        (cw < thrMataUang) 
                        and (ch <= thbMataUang) 
                        and (ch >= thtMataUang)
                        and (cw > thlMataUang)
                    ) :
                        if mataUang == None :
                            mataUang = text
                    
                if thrNomorRekening != None:
                    if (
                        (cw < thrNomorRekening) 
                        and (ch <= thbNomorRekening) 
                        and (ch >= thtNomorRekening)
                        and (cw > thlNomorRekening)
                    ) :
                        if nomorRekening == None :
                            nomorRekening = text.strip()
                        
                        else :
                            nomorRekening = nomorRekening + ' - ' + text.strip()
                            
                if thrTanggalPercetakan != None:
                    if (
                        (cw < thrTanggalPercetakan) 
                        and (ch <= thbTanggalPercetakan) 
                        and (ch >= thtTanggalPercetakan)
                        and (cw > thlTanggalPercetakan)
                    ) :
                        if tanggalPercetakan == None :
                            tanggalPercetakan = text
                            
                if thrCabang != None:
                    if (
                        (cw < thrCabang) 
                        and (ch <= thbCabang) 
                        and (ch >= thtCabang)
                        and (cw > thlCabang)
                    ) :
                        if cabang == None :
                            cabang = text.strip()
                            
                        else :
                            cabang = cabang + ' - ' + text.strip()
                            
                if thrPeriode != None:
                    if (
                        (cw < thrPeriode) 
                        and (ch <= thbPeriode) 
                        and (ch >= thtPeriode)
                        and (cw > thlPeriode)
                    ) :
                        if periode == None :
                            periode = text.strip()
                            
                        else :
                            periode = periode + ' - ' + text.strip()
                            
                if thrPemilikRekening != None:
                    if (
                        (cw < thrPemilikRekening) 
                        and (ch <= thbPemilikRekening) 
                        and (ch >= thtPemilikRekening)
                        and (cw > thlPemilikRekening)
                    ) :
                        if pemilikRekening == None :
                            pemilikRekening = text.strip()
                            
                        else :
                            pemilikRekening = pemilikRekening + ' ' + text.strip()
                            
                if thrAlamat != None:
                    if (
                        (cw < thrAlamat) 
                        and (ch <= thbAlamat) 
                        and (ch >= thtAlamat)
                        and (cw > thlAlamat)
                    ) :         
                        if alamat == None :
                            alamat = text.strip()
                            
                        else :
                            alamat = alamat + ' ' + text.strip()    
                            
            if 'uraian' in text.lower() and currentRow == 0:
                thbHeaderTable = tb + int(0.039 * tinggiGambar)
                thbTable = tb + int(0.575 * tinggiGambar)
                thrTableCol1 = rb - int(0.285 * lebarGambar)
                thrTableCol2 = thrTableCol1 + int(0.076 * lebarGambar)
                thrTableCol3 = thrTableCol2 + int(0.345 * lebarGambar)
                thrTableCol4 = thrTableCol3 + int(0.11 * lebarGambar)
                thrTableCol5 = thrTableCol4 + int(0.12 * lebarGambar)
                
            if ch > 0.5 * tinggiGambar and 'mata' in text.lower() and 'uang' in text.lower() :
                thbTable = tb
                continue
                
            if thbHeaderTable != None and ch > thbHeaderTable and ch < thbTable :
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
                    
                if (cw > thrTableCol5) :
                    textWithCol['col'] = 6
                    textWithCol['row'] = currentRow
                    
                textData.append(textWithCol.copy())
        # if not isBankStatementCorrect :
        #     return 400
        
        transactionData.extend(ocbcGetTransactionData(textData, filename))
    
    data['pemilik_rekening'] = pemilikRekening
    data['alamat'] = alamat
    data['nomor_rekening'] = nomorRekening
    data['cabang'] = cabang
    data['periode'] = periode
    data['tanggal_percetakan'] = tanggalPercetakan
    data['mata_uang'] = mataUang
    data['transaction_data'] = transactionData
    data['total_debet'] = getTotalDebit(transactionData)
    data['total_kredit'] = getTotalKredit(transactionData)
    data['analytics_data'] = ocbcAnalysisData(data['transaction_data'])
    return data