import os
import uuid
from matplotlib.dviread import Page
from werkzeug.utils import secure_filename

from services.mandiri_services.get_analysis_data import mandiriAnalysisData
from services.mandiri_services.get_total_debit import getTotalDebit
from services.mandiri_services.get_total_kredit import getTotalKredit
from services.mandiri_services.get_transaction_data import mandiriGetTransactionData
from services.utils.correct_perspective import correctPerspective
from services.utils.delete_image import deleteImage
from services.utils.do_orc_easyocr import doEasyOcr
from services.utils.exception_handler import exceptionHandler
from services.utils.get_image_height import getImageHeight
from services.utils.get_image_width import getImageWidth

def doOcrMandiri (imageArray, app, isZip, isPdf, logger, username) :
    periodeLaporan = None
    nomorRekening = None
    pemilikRekening = None
    currency = None
    branch = None

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

    thrPeriodeLaporan = None
    thbPeriodeLaporan = None
    thtPeriodeLaporan = None
    thlPeriodeLaporan = None

    thrNomorRekening = None
    thbNomorRekening = None
    thtNomorRekening = None
    thlNomorRekening = None

    thrPemilikRekening = None
    thbPemilikRekening = None
    thtPemilikRekening = None
    thlPemilikRekening = None

    thrCurrency = None
    thbCurrency = None
    thtCurrency = None
    thlCurrency = None

    thrBranch = None
    thbBranch = None
    thtBranch = None
    thlBranch = None
    
    currentRow = 0
    countText = 0
    
    for e in imageArray:
        page += 1
        textData.clear()
        
        if isZip == True :
            filename = secure_filename(e)
            file_path = os.path.join(app.config['EXTRACT_FOLDER'], filename)
            perspectiveCorrectedImage = correctPerspective(file_path)
            
        elif isPdf == True :
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
                'bni' in text.lower() or
                'bri' in text.lower() or
                'danamon' in text.lower() or
                'cimb' in text.lower())
                and countText < 15
            ) :
                return exceptionHandler(
                    f'The type of bank statement detected is not the same as in the {filename} image! Please re-upload with the same type of bank statement or a clearer image.',
                    400,
                    None
                )
            
            if page == 1 :
                if 'per' in text.lower() and ch < 0.3 * tinggiGambar :
                    thlPeriodeLaporan = rb + int(0.18 * lebarGambar)
                    thrPeriodeLaporan = thlPeriodeLaporan + int(0.3 * lebarGambar)
                    thbPeriodeLaporan = bb + int(0.019 * tinggiGambar)
                    thtPeriodeLaporan = tb - int(0.005 * tinggiGambar)
                    
                if 'count' in text.lower() and ch < 0.3 * tinggiGambar :
                    thlNomorRekening = rb + int(0.14 * lebarGambar)
                    thrNomorRekening = thlPeriodeLaporan + int(0.3 * lebarGambar)
                    thbNomorRekening = bb + int(0.005 * tinggiGambar)
                    thtNomorRekening = tb - int(0.005 * tinggiGambar)
                    
                if 'ency' in text.lower() and ch < 0.3 * tinggiGambar :
                    thlCurrency = rb + int(0.14 * lebarGambar)
                    thrCurrency = thlPeriodeLaporan + int(0.3 * lebarGambar)
                    thbCurrency = bb + int(0.005 * tinggiGambar)
                    thtCurrency = tb - int(0.005 * tinggiGambar)
                    
                if 'anch' in text.lower() and ch < 0.35 * tinggiGambar :
                    thlBranch = rb + int(0.14 * lebarGambar)
                    thrBranch = thlPeriodeLaporan + int(0.3 * lebarGambar)
                    thbBranch = bb + int(0.005 * tinggiGambar)
                    thtBranch = tb - int(0.005 * tinggiGambar)

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
                            periodeLaporan = periodeLaporan + ' ' + text
                                
                if thrNomorRekening != None:
                    if (
                        (cw < thrNomorRekening) 
                        and (ch <= thbNomorRekening) 
                        and (ch >= thtNomorRekening)
                        and (cw > thlNomorRekening)
                    ) :
                        if nomorRekening == None :
                            nomorRekening = text
                            
                        else :
                            pemilikRekening = text.strip()
                                
                if thrCurrency != None:
                    if (
                        (cw < thrCurrency) 
                        and (ch <= thbCurrency) 
                        and (ch >= thtCurrency)
                        and (cw > thlCurrency)
                    ) :
                        if currency == None :
                            currency = text
                            
                if thrBranch != None:
                    if (
                        (cw < thrBranch) 
                        and (ch <= thbBranch) 
                        and (ch >= thtBranch)
                        and (cw > thlBranch)
                    ) :
                        if branch == None :
                            branch = text
                
            
            try :
                if 'description' in text.lower() and ch < 0.4 * tinggiGambar and currentRow == 0:
                    thbHeaderTable = tb + int(0.021 * tinggiGambar)
                    thbTable = tb + int(0.575 * tinggiGambar)
                    thrTableCol1 = rb - int(0.18 * tinggiGambar)
                    thrTableCol2 = thrTableCol1 + int(0.064 * tinggiGambar)
                    thrTableCol3 = thrTableCol2 + int(0.153 * tinggiGambar)
                    thrTableCol4 = thrTableCol3 + int(0.092 * tinggiGambar)
                    thrTableCol5 = thrTableCol4 + int(0.078 * tinggiGambar)
                    thrTableCol6 = thrTableCol5 + int(0.065 * tinggiGambar)
                    
                if thbHeaderTable != None and ch > thbHeaderTable and ch < thbTable :
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
                    
            except ValueError as e:
                return exceptionHandler(
                    f'An error occurred with image {filename}. Try rephotographing this image more clearly!',
                    400,
                    e
                ) 
                
            except TypeError as e:
                return exceptionHandler(
                    f'An error occurred with image {filename}. Try rephotographing this image more clearly!',
                    400,
                    e
                )
        # if not isBankStatementCorrect :
        #     return 400
        
        transactionData.extend(mandiriGetTransactionData(textData, filename))
        deleteImage(file_path)
    
    data['period'] = periodeLaporan
    data['nomor_rekening'] = nomorRekening
    data['pemilik_rekening'] = pemilikRekening
    data['currency'] = currency
    data['branch'] = branch
    data['transaction_data'] = transactionData
    data['total_debet'] = getTotalDebit(transactionData)
    data['total_kredit'] = getTotalKredit(transactionData)
    data['analytics_data'] = mandiriAnalysisData(data['transaction_data'])
    data['banyak_halaman'] = len(imageArray)
    return 200, data