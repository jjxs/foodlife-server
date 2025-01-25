
# return saas id
def group_name(saas_id, gname):
    name = "{0}.{1}".format(saas_id, gname)
    print("--------group_name--------", name)
    return name


def id(data):
    saas_id = ""
    request_host = ""

    if type(data)==dict:
        headers = data["headers"]
        for k, v in headers:
            if k.decode()=="host":
                request_host = v.decode()
                break
    else:
        request_host = data.META["HTTP_HOST"]

    if request_host!="":
        id = request_host.split('.')
        if id[0]!="null":
            saas_id = id[0]
    if saas_id=="192":
        saas_id = "foodlife01"
    print(saas_id)
    return saas_id
