def check_is_zip(data):
    if data[0].content_type == 'application/zip':
        return True

    return False