from io import StringIO
import pandas as pd


def Validation():
    print "validating"
    return True


def MainProcess(request):
    print "data processing"
    for key in request.form.keys():
        tmpFile = request.form.get(key)
        strIo = StringIO(tmpFile)
        df = pd.read_csv(strIo, header=None)
        # df.to_csv("E:/" + key + ".csv", index=False, header=False)
    if not Validation():
        return "Not Valid"
    return "processed data"