def exceptionHandler(message: str, errorCode: int, errorDesc: str) :
    print('-' * 150)
    print(message)
    print(errorDesc)
    print('-' * 150)
    print()
    return errorCode, message