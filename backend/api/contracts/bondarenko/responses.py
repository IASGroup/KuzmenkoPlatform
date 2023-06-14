class MainResponse:
    def __init__(self, isSuccess, errorMessage):
        self.isSuccess = isSuccess
        self.errorMessage = errorMessage

    @staticmethod
    def success ():
        return MainResponse(True, None)

    @staticmethod
    def failure (errorMessage):
        return MainResponse(False, errorMessage)

class ResultResponse:
    def __init__(self, isSuccess, result, errorMessage):
        self.isSuccess = isSuccess
        self.result = result
        self.errorMessage = errorMessage
    
    @staticmethod
    def success (result):
        return ResultResponse(True, result, None)

    @staticmethod
    def failure (errorMessage):
        return ResultResponse(False, None, errorMessage)