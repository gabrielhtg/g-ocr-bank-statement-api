def isCurrentPageTheRightBankStatementType (bank_statement_type, ocr_text) :
    # melakukan pengecekan terhadap bank BCA Corporate
    if int(bank_statement_type) == 1 :
        if 'rekening giro' in ocr_text.lower() :
            return True

        return False

    # melakukan pengecekan terhadap bank BCA Personal
    if int(bank_statement_type) == 2 :
        if 'rekening tahapan' in ocr_text.lower() :
            return True
        
        return False
        
    # melakukan pengecekan terhadap bank BRI
    if int(bank_statement_type) == 3 :
        if 'bri' in ocr_text.lower() :
            return True

        return False