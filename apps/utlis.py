



def get_response_handler(pk,res):

    if pk:
        if res and len(res):
            return res[0]
        else:
            return {}
    else:
        return res