import os
from matplotlib.dviread import Page
from werkzeug.utils import secure_filename

from services.bni_controller.get_analysis_data import bniAnalysisData
from services.bni_controller.get_total_debit import getTotalDebit
from services.bni_controller.get_total_kredit import getTotalKredit
from services.bni_controller.get_transaction_data import bniGetTransactionData
from services.utils.correct_perspective import correctPerspective
from services.utils.do_orc_easyocr import doEasyOcr
from services.utils.get_image_height import getImageHeight
from services.utils.get_image_width import getImageWidth

def doOcrBni (imageArray, app, bankStatementType) :
    page = 0
    
    pemilikRekening = None
    alamat = None
    nomorRekening = None
    akunRekening = None
    tipeAkun = None
    periodeRekening = None

    thrPemilikRekening = None
    thtPemilikRekening = None
    thbPemilikRekening = None
    thlPemilikRekening = None

    thrAlamat = None
    thtAlamat = None
    thbAlamat = None
    thlAlamat = None

    thrAccountNo = None
    thtAccountNo = None
    thbAccountNo = None
    thlAccountNo = None

    thrAccountType = None
    thtAccountType = None
    thbAccountType = None
    thlAccountType = None

    thrPeriod = None
    thtPeriod = None
    thbPeriod = None
    thlPeriod = None
    
    thbHeaderTable = None
    thbTable = None
    thrTableCol1 = None
    thrTableCol2 = None
    thrTableCol3 = None
    thrTableCol4 = None
    thrTableCol5 = None
    thrTableCol6 = None
    thrTableCol7 = None
    thrTableCol8 = None

    currentRow = 0
    textData = []
    textWithCol = {}

    postingData = None
    effectiveDate = None
    branch = None
    journal = None
    transactionDescription = None
    amount = None
    debitCredit = None
    balance = None
    
    transactionData = []
    data = {}
   
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
            
            if 'count' in text.lower() and 'eme' in text.lower() :
                thrPemilikRekening = lb - int(0.2 * lebarGambar)
                thtPemilikRekening = bb
                thbPemilikRekening = bb + int(0.02 * tinggiGambar)
                thrAlamat = lb - int(0.07 * lebarGambar)
                thlAlamat = lb - int(0.2 * lebarGambar)
                thbAlamat = bb + int (0.08 * tinggiGambar)
                
            if 'no' in text.lower() and 'cou' in text.lower() :
                thrAccountNo = rb + int(0.25 * lebarGambar)
                thbAccountNo = bb + int(0.001 * tinggiGambar)
                thtAccountNo = tb - int(0.004 * tinggiGambar)
                thlAccountNo = rb + int(0.008 * tinggiGambar)
                
            if 'cou' in text.lower() and 'pe' in text.lower() :
                thrAccountType = rb + int(0.25 * lebarGambar)
                thbAccountType = bb + int(0.0005 * tinggiGambar)
                thtAccountType = tb - int(0.001 * tinggiGambar)
                thlAccountType = rb + int(0.008 * tinggiGambar)
                
            if 'rio' in text.lower() :
                thrPeriod = rb + int(0.25 * lebarGambar)
                thbPeriod = bb + int(0.0005 * tinggiGambar)
                thtPeriod = tb - int(0.004 * tinggiGambar)
                thlPeriod = rb + int(0.008 * tinggiGambar)
                
            if thrAlamat != None:
                if (
                    bb < thbPemilikRekening and 
                    tb > thtPemilikRekening and 
                    rb < thrAlamat
                    ) :
                    if pemilikRekening == None:
                        pemilikRekening = text
                        
                if pemilikRekening != None :
                    if (
                        tb > thbPemilikRekening and 
                        bb < thbAlamat and 
                        rb < thrAlamat
                        ) :
                        if alamat == None:
                            alamat = text
                            
                        else :
                            alamat = alamat + ' ' + text
                
            if thbAccountNo != None:
                if (
                    (lb > thlAccountNo) 
                    and (bb <= thbAccountNo) 
                    and (tb >= thtAccountNo)
                ) :
                    if nomorRekening == None :
                        nomorRekening = text
                        
                    else :
                        akunRekening = text
                        
            if thrAccountType != None:
                if (
                    (lb > thlAccountType) 
                    and (bb <= thbAccountType) 
                    and (tb >= thtAccountType)
                ) :
                    if tipeAkun == None :
                        tipeAkun = text
                        
            if thrPeriod != None:
                if (
                    (lb > thlPeriod) 
                    and (bb <= thbPeriod) 
                    and (tb >= thtPeriod)
                ) :
                    if periodeRekening == None :
                        periodeRekening = text
                        
                    else :
                        periodeRekening = periodeRekening + ' ' + text
                
            if 'ting' in text.lower() and 'te' in text.lower() and currentRow == 0:
                thbHeaderTable = tb + int(0.015 * tinggiGambar)
                thbTable = tb + int(0.575 * tinggiGambar)
                thrTableCol1 = rb + int(0.03 * lebarGambar)
                thrTableCol2 = thrTableCol1 + int(0.148 * lebarGambar)
                thrTableCol3 = thrTableCol2 + int(0.079 * lebarGambar)
                thrTableCol4 = thrTableCol3 + int(0.058 * lebarGambar)
                thrTableCol5 = thrTableCol4 + int(0.219 * lebarGambar)
                thrTableCol6 = thrTableCol5 + int(0.11 * lebarGambar)
                thrTableCol7 = thrTableCol6 + int(0.045 * lebarGambar)
                
                # cv.line(
                #         img,
                #         (thrTableCol1, thbHeaderTable),
                #         (thrTableCol1, tinggiGambar),
                #         (0, 255, 0),
                #         2
                #     )

            if thbHeaderTable != None and ch > thbHeaderTable :
                textWithCol['text'] = text
                
                if (cw > thrTableCol1 and 
                    cw < thrTableCol6 and 
                    'edge' in text.lower() and 
                    'alan' in text.lower()):
                    currentRow += 1
                    textWithCol['col'] = 5
                    textWithCol['row'] = currentRow
                    
                if cw > thrTableCol7 :
                    textWithCol['col'] = 8
                    textWithCol['row'] = currentRow
                        
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
                    
                if (cw > thrTableCol6 and cw < thrTableCol7) :
                    textWithCol['col'] = 7
                    textWithCol['row'] = currentRow
                    
                if (cw > thrTableCol7) :
                    textWithCol['col'] = 8
                    textWithCol['row'] = currentRow
                
                textData.append(textWithCol.copy())
        
        # if not isBankStatementCorrect :
        #     return 400
        
        transactionData.extend(bniGetTransactionData(textData))
    
    data['akun_rekening'] = akunRekening
    data['nomor_rekening'] = nomorRekening
    data['tipe_akun'] = tipeAkun
    data['periode_rekening'] = periodeRekening
    data['pemilik_rekening'] = pemilikRekening
    data['alamat'] = alamat
    data['transaction_data'] = transactionData
    data['total_debet'] = getTotalDebit(transactionData)
    data['total_kredit'] = getTotalKredit(transactionData)
    data['analytics_data'] = bniAnalysisData(data['transaction_data'])
    return data