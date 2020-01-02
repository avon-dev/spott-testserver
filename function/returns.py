



class ReturnPattern:

    def error_text(**dict):
        error = {"error":dict}

        return error

    def success_text(message,**dict):
        success = {"payload":dict,"message":message}

        return success
