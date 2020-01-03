
import json


class ReturnPattern:

    def error_text(**dict):
        error = {"error":dict}

        return str(error)

    def success_text(message,**dict):
        success = {"payload":dict,"message":message}

        return str(success)



def string_to_dict(request):
    re_string = request["sending"]
    result = json.loads(re_string)

    return result
