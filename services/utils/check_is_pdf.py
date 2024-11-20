def checkIsPdf(uploaded_files):
    if '.pdf' in uploaded_files[0].filename.lower():
        return True
    
    return False