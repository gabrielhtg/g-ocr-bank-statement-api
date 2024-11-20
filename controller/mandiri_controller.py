from flask import jsonify, request

from services.mandiri_services.mandiri_ocr_service import doOcrMandiri
from services.mandiri_services.mandiri_ocr_service_pdf import doOcrMandiriPdf
from services.utils.check_is_pdf import checkIsPdf
from services.utils.check_is_zip import checkIsZip
from services.utils.get_file_list_from_zip import getFileListFromZip
from services.utils.get_images_from_pdf import getImagesFromPdf
from services.utils.return_fail_message import returnFailMessage

def mandiriController(app) :
    uploadedFiles = request.files.getlist('files')
    zipPassword = ''
    bankStatementType = request.form.get('bank-statement-type')
    
    if request.form.get('zip-password') :
        zipPassword = request.form.get('zip-password')
    
    # variable ini menyimpan apakah file yang diupload adalah 
    # file zip atau bukan. 
    isZip = False
    isPdf = False
    
    # cek apakah file yang diupload adalah zip
    if len(uploadedFiles) == 1 :
        isZip = checkIsZip(uploadedFiles)
        isPdf = checkIsPdf(uploadedFiles)
        
    if isZip:
        fileList = getFileListFromZip(uploadedFiles[0], app, zipPassword)
            
        if fileList == 400 :
            return returnFailMessage(False, 'Gagal mengekstrak zip! Password salah!')

        else :
            statusCode, data = doOcrMandiri(fileList, app, isZip, isPdf)

            if statusCode != 200 :
                return returnFailMessage(data, statusCode)
            
    if isPdf:
        fileList = getImagesFromPdf(uploadedFiles[0], app)
            
        statusCode, data = doOcrMandiriPdf(fileList, app, isZip, isPdf)

        if statusCode != 200 :
            return returnFailMessage(data, statusCode)
            
    else :
        sortedData = sorted(uploadedFiles, key=lambda x: x.filename)
        
        statusCode, data = doOcrMandiri(sortedData, app, isZip, isPdf)
        
        if statusCode != 200 :
            return returnFailMessage(data, statusCode)

    return jsonify({
        'message' : 'ok',
        'data' : {
            'period' : data['period'],
            'nomor_rekening' : data['nomor_rekening'],
            'pemilik_rekening' : data['pemilik_rekening'],
            'currency' : data['currency'],
            'branch' : data['branch'],
            'transaction_data' : data['transaction_data'],
            'total_debet' : data['total_debet'],
            'total_kredit' : data['total_kredit'],
            'analytics_data': data['analytics_data']    
        }
    })