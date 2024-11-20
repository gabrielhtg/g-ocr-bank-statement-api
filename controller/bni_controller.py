from io import BytesIO
import os
import uuid
from flask import jsonify, request
from pypdf import PdfReader

from services.bni_services.bni_ocr_service import doOcrBni
from services.bni_services.bni_ocr_service_pdf import doOcrBniPdf
from services.utils.check_is_pdf import checkIsPdf
from services.utils.check_is_zip import checkIsZip
from services.utils.get_file_list_from_zip import getFileListFromZip
from services.utils.get_images_from_pdf import getImagesFromPdf
from services.utils.is_pdf_changed import isPdfChanged
from services.utils.return_fail_message import returnFailMessage

def bniController(app) :
    uploadedFiles = request.files.getlist('files')
    zipPassword = ''
    
    if request.form.get('zip-password') :
        zipPassword = request.form.get('zip-password')
    
    isZip = False
    isPdf = False
    isPdfModified = None
    
    # cek apakah file yang diupload adalah zip
    if len(uploadedFiles) == 1 :
        isZip = checkIsZip(uploadedFiles)
        isPdf = checkIsPdf(uploadedFiles)
        
    if isZip:
        fileList = getFileListFromZip(uploadedFiles[0], app, zipPassword)
            
        if fileList == 400 :
            return returnFailMessage(False, 'Gagal mengekstrak zip! Password salah!')

        else :
            statusCode, data = doOcrBni(fileList, app, isZip, isPdf)

            if statusCode != 200 :
                return returnFailMessage(data, statusCode)
            
    elif isPdf:
        fileList = getImagesFromPdf(uploadedFiles[0], app)
        
        unique_filename = f"{uuid.uuid4().hex}_{uploadedFiles[0].filename}"
        destination_path = os.path.join(app.config['PDF_EXTRACT_FOLDER'], unique_filename)
        uploadedFiles[0].save(destination_path)
        stat = os.stat(destination_path)
        
        if stat.st_mtime == stat.st_ctime :
            isPdfModified = False
            
        else :
            isPdfModified = True
            
        os.remove(destination_path)
        
        statusCode, data = doOcrBniPdf(fileList, app, isZip, isPdf)

        if statusCode != 200 :
            return returnFailMessage(data, statusCode)
            
    else :
        sortedData = sorted(uploadedFiles, key=lambda x: x.filename)
        
        statusCode, data = doOcrBni(sortedData, app, isZip, isPdf)
        
        if statusCode != 200 :
            return returnFailMessage(data, statusCode)

    return jsonify({
        'message' : 'ok',
        'data' : {
            'akun_rekening' : data['akun_rekening'],
            'nomor_rekening' : data['nomor_rekening'],
            'tipe_akun' : data['tipe_akun'],
            'periode_rekening' : data['periode_rekening'],
            'pemilik_rekening' : data['pemilik_rekening'],
            'alamat' : data['alamat'],
            'transaction_data' : data['transaction_data'],
            'total_debet_by_ocr' : data['total_debet_by_ocr'],
            'total_kredit_by_ocr' : data['total_kredit_by_ocr'],
            'ending_balance' : data['ending_balance'],
            'total_debet' : data['total_debet'],
            'total_credit' : data['total_credit'],
            'total_debet_amount' : data['total_debet_amount'],
            'total_credit_amount' : data['total_credit_amount'],
            'analytics_data': data['analytics_data'],
            'is_pdf_modified' : isPdfModified   
        }
    })