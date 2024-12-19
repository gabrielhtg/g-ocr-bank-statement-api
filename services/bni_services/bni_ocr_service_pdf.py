import os
import uuid
from matplotlib.dviread import Page
from werkzeug.utils import secure_filename

from services.bni_services.get_analysis_data import bniAnalysisData
from services.bni_services.get_total_debit import getTotalDebit
from services.bni_services.get_total_kredit import getTotalKredit
from services.bni_services.get_transaction_data import bniGetTransactionData
from services.utils.correct_perspective import correctPerspective
from services.utils.delete_image import deleteImage
from services.utils.do_orc_easyocr import doEasyOcr
from services.utils.exception_handler import exceptionHandler
from services.utils.get_image_height import getImageHeight
from services.utils.get_image_width import getImageWidth

def doOcrBniPdf (imageArray, app, isZip, isPdf, logger, username) :
    page = 0
    
    pemilikRekening = None
    alamat = None
    nomorRekening = None
    akunRekening = None
    tipeAkun = None
    periodeRekening = None
    endingBalance = None
    totalDebet = None
    totalCredit = None
    totalDebetAmount = None
    totalCreditAmount = None

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

    currentRow = 0
    textData = []
    textWithCol = {}

    thrEndingBalance = None
    thtEndingBalance = None
    thbEndingBalance = None
    thlEndingBalance = None

    thrTotalDebet = None
    thtTotalDebet = None
    thbTotalDebet = None
    thlTotalDebet = None

    thrTotalCredit = None
    thtTotalCredit = None
    thbTotalCredit = None
    thlTotalCredit = None

    thrTotalDebetAmount = None
    thtTotalDebetAmount = None
    thbTotalDebetAmount = None
    thlTotalDebetAmount = None

    thrTotalCreditAmount = None
    thtTotalCreditAmount = None
    thbTotalCreditAmount = None
    thlTotalCreditAmount = None
    
    transactionData = []
    data = {}
    
    countText = 0
   
    for e in imageArray:
        page += 1
        textData.clear()
        
        if isZip :
            filename = secure_filename(e)
            file_path = os.path.join(app.config['EXTRACT_FOLDER'], filename)
            perspectiveCorrectedImage = correctPerspective(file_path)
            
        elif isPdf :
            filename = secure_filename(e)
            file_path = os.path.join(app.config['PDF_EXTRACT_FOLDER'], filename)
            perspectiveCorrectedImage = correctPerspective(file_path)
            
        else :
            file = e
            filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4().hex}_{filename}"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(file_path)
            perspectiveCorrectedImage = correctPerspective(file_path)
        
        logger.info(f"{username} : Processing {filename}")
        print('Processing', filename)
        
        lebarGambar = getImageWidth(perspectiveCorrectedImage)
        tinggiGambar = getImageHeight(perspectiveCorrectedImage)
        
        if int(lebarGambar) > int(tinggiGambar) :
            return exceptionHandler(
                'Image detected landscape. Photo images in Portrait form',
                400,
                e
            )

        # text_ merupakan semua teks hasil ocr dari gambar
        # tapi masih bukan hasil akhir
        text_ = doEasyOcr(perspectiveCorrectedImage)

        for e in text_ :
            countText += 1
            bbox, text, score = e
    
            bbox = [[int(coord[0]), int(coord[1])] for coord in bbox]
                    
            rb = bbox[1][0]
            lb = bbox[0][0]
            tb = bbox[1][1]
            bb = bbox[2][1]
            cw = lb + int(abs(rb - lb) / 2)
            ch = tb + int(abs(bb - tb) / 2)
            
            if (
                ('bca' in text.lower() or
                'ocbc' in text.lower() or
                ('permata' in text.lower() and 'bank' in text.lower()) or
                'bri' in text.lower() or
                'cimb' in text.lower() or
                'mandiri' in text.lower() or
                'danamon' in text.lower())
                and countText < 15
            ) :
                return exceptionHandler(
                    f'The type of bank statement detected is not the same as in the {filename} image! Please re-upload with the same type of bank statement or a clearer image.',
                    400,
                    None
                )
            
            if page == 1 :
                if 'count' in text.lower() and 'eme' in text.lower() :
                    thrPemilikRekening = lb - int(0.2 * lebarGambar)
                    thtPemilikRekening = bb
                    thbPemilikRekening = bb + int(0.02 * tinggiGambar)
                    thrAlamat = lb - int(0.07 * lebarGambar)
                    thlAlamat = lb - int(0.2 * lebarGambar)
                    thbAlamat = bb + int (0.1 * tinggiGambar)
                    thtAlamat = thbPemilikRekening
                    
                if 'no' in text.lower() and 'cou' in text.lower() :
                    thrAccountNo = rb + int(0.25 * lebarGambar)
                    thbAccountNo = bb + int(0.001 * tinggiGambar)
                    thtAccountNo = tb - int(0.004 * tinggiGambar)
                    thlAccountNo = rb + int(0.008 * tinggiGambar)
                    
                if ('type' in text.lower() and
                    ch < 0.3 * tinggiGambar):
                    thrAccountType = rb + int(0.25 * lebarGambar)
                    thbAccountType = bb + int(0.0005 * tinggiGambar)
                    thtAccountType = tb - int(0.001 * tinggiGambar)
                    thlAccountType = rb + int(0.008 * tinggiGambar)
                    
                if 'rio' in text.lower() :
                    thrPeriod = rb + int(0.25 * lebarGambar)
                    thbPeriod = bb + int(0.0005 * tinggiGambar)
                    thtPeriod = tb - int(0.004 * tinggiGambar)
                    thlPeriod = rb + int(0.008 * tinggiGambar)
                
                if thrPemilikRekening != None:
                    if (
                        ch < thbPemilikRekening and 
                        ch > thtPemilikRekening and 
                        cw < thrPemilikRekening
                        ) :
                        if pemilikRekening == None:
                            pemilikRekening = text
                            
                        else :
                            pemilikRekening = pemilikRekening + ' ' + text
                    
                if thrAlamat != None:
                    if (
                        ch < thbAlamat and 
                        ch > thtAlamat and 
                        cw < thrAlamat
                        ) :
                        if alamat == None:
                            alamat = text
                            
                        else :
                            alamat = alamat + ' ' + text
                    
                if thbAccountNo != None:
                    if (
                        (cw > thlAccountNo) 
                        and (ch <= thbAccountNo) 
                        and (ch >= thtAccountNo)
                    ) :
                        if nomorRekening == None :
                            nomorRekening = text
                            
                        else :
                            akunRekening = text
                            
                if thrAccountType != None:
                    if (
                        (cw > thlAccountType) 
                        and (ch <= thbAccountType) 
                        and (ch >= thtAccountType)
                    ) :
                        if tipeAkun == None :
                            tipeAkun = text
                            
                if thrPeriod != None:
                    if (
                        (cw > thlPeriod) 
                        and (ch <= thbPeriod) 
                        and (ch >= thtPeriod)
                    ) :
                        if periodeRekening == None :
                            periodeRekening = text
                            
                        else :
                            periodeRekening = periodeRekening + ' ' + text
            
            # try :
            if 'ting' in text.lower() and 'te' in text.lower() and currentRow == 0:
                thbHeaderTable = tb + int(0.015 * tinggiGambar)
                thbTable = tb + int(0.575 * tinggiGambar)
                thrTableCol1 = rb + int(0.03 * lebarGambar)
                thrTableCol2 = thrTableCol1 + int(0.157 * lebarGambar)
                thrTableCol3 = thrTableCol2 + int(0.084 * lebarGambar)
                thrTableCol4 = thrTableCol3 + int(0.059 * lebarGambar)
                thrTableCol5 = thrTableCol4 + int(0.232 * lebarGambar)
                thrTableCol6 = thrTableCol5 + int(0.112 * lebarGambar)
                thrTableCol7 = thrTableCol6 + int(0.045 * lebarGambar)
                
            if (page == len(imageArray)) :        
                if 'ending' in text.lower() :
                    thbTable = tb - int(0.005 * tinggiGambar)
                    thtEndingBalance = tb
                    thrEndingBalance = lebarGambar - int(0.005 * lebarGambar)
                    thlEndingBalance = rb + int(0.003 * lebarGambar)
                    thbEndingBalance = thtEndingBalance + int(0.02 * tinggiGambar)
                    
                if 'total' in text.lower() and 'debet' in text.lower():
                    thtTotalDebet = tb
                    thrTotalDebet = rb + int(0.1 * lebarGambar)
                    thlTotalDebet = rb + int(0.01 * lebarGambar)
                    thbTotalDebet = bb
                    
                    thtTotalDebetAmount = tb
                    thlTotalDebetAmount = thrTotalDebet
                    thrTotalDebetAmount = rb + int(0.3 * lebarGambar)
                    thbTotalDebetAmount = bb
                    
                if 'total' in text.lower() and 'credit' in text.lower():
                    thtTotalCredit = tb
                    thrTotalCredit = rb + int(0.1 * lebarGambar)
                    thlTotalCredit = rb + int(0.01 * lebarGambar)
                    thbTotalCredit = bb
                    
                    thtTotalCreditAmount = tb
                    thlTotalCreditAmount = thrTotalCredit
                    thrTotalCreditAmount = rb + int(0.3 * lebarGambar)
                    thbTotalCreditAmount = bb
                    
                if thrEndingBalance != None:
                    if (
                        (cw < thrEndingBalance) 
                        and (ch < thbEndingBalance) 
                        and (ch > thtEndingBalance)
                        and (cw > thlEndingBalance)
                    ) :
                        if endingBalance == None :
                            endingBalance = text
                            
                if thrTotalDebet != None:
                    if (
                        (cw < thrTotalDebet) 
                        and (ch <= thbTotalDebet) 
                        and (ch >= thtTotalDebet)
                        and (cw > thlTotalDebet)
                    ) :
                        if totalDebet == None :
                            totalDebet = text
                            
                if thrTotalCredit != None:
                    if (
                        (cw < thrTotalCredit) 
                        and (ch <= thbTotalCredit) 
                        and (ch >= thtTotalCredit)
                        and (cw > thlTotalCredit)
                    ) :
                        if totalCredit == None :
                            totalCredit = text
                            
                if thrTotalCreditAmount != None:
                    if (
                        (cw < thrTotalCreditAmount) 
                        and (ch <= thbTotalCreditAmount) 
                        and (ch >= thtTotalCreditAmount)
                        and (cw > thlTotalCreditAmount)
                    ) :
                        if totalCreditAmount == None :
                            totalCreditAmount = text
                
                if thrTotalDebetAmount != None:
                    if (
                        (cw < thrTotalDebetAmount) 
                        and (ch <= thbTotalDebetAmount) 
                        and (ch >= thtTotalDebetAmount)
                        and (cw > thlTotalDebetAmount)
                    ) :
                        if totalDebetAmount == None :
                            totalDebetAmount = text
                
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
                    
            # except TypeError as e:
            #     return exceptionHandler(
            #         f'An error occurred with image {filename}. Try rephotographing this image more clearly!',
            #         400,
            #         e
            #     )
            
            # except ValueError as e:
            #     return exceptionHandler(
            #         f'An error occurred with image {filename}. Try rephotographing this image more clearly!',
            #         400,
            #         e
            #     ) 
        
        # if not isBankStatementCorrect :
        #     return 400
        
        transactionData.extend(bniGetTransactionData(textData, filename))
        deleteImage(file_path)
    
    data['akun_rekening'] = akunRekening
    data['nomor_rekening'] = nomorRekening
    data['tipe_akun'] = tipeAkun
    data['periode_rekening'] = periodeRekening
    data['pemilik_rekening'] = pemilikRekening
    data['alamat'] = alamat
    data['transaction_data'] = transactionData
    data['ending_balance'] = endingBalance
    data['total_debet'] = totalDebet
    data['total_credit'] = totalCredit
    data['total_debet_amount'] = totalDebetAmount
    data['total_credit_amount'] = totalCreditAmount
    data['total_debet_by_ocr'] = getTotalDebit(transactionData)
    data['total_kredit_by_ocr'] = getTotalKredit(transactionData)
    data['analytics_data'] = bniAnalysisData(data['transaction_data'])
    data['banyak_halaman'] = len(imageArray)
    return 200, data