# coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from io import StringIO
import pandas as pd
import csv

from basic_class import *
from datetime import datetime

def GAVRP_Validation(request):
    print "validating"
    return True


def GAVRP_Process(request):
    if not GAVRP_Validation(request):
        return "Not Valid"
    print "data processing"
    var_dict = {}
    today = datetime.strptime(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S').date()
    order_tmpFile = request.form.get("order_raw")
    strIo = StringIO(order_tmpFile)
    input_file = csv.reader(strIo)
    order_dict = {
    i[0]: order(str(i[0]), int(i[1]), int(i[4]), (today - datetime.strptime(i[11], '%Y-%m-%d %H:%M:%S').date()).days,
                int(i[12]), -1,
                -1, int(i[3]), int(i[7]), int(i[6]), -1, datetime.strptime(i[11], '%Y-%m-%d %H:%M:%S').date(), i[14],
                -1) for i in input_file}
    var_dict['order_dict']=order_dict

    trailer_tmpFile = request.form.get("trailer_raw_truck")
    strIo = StringIO(trailer_tmpFile)
    input_file = csv.reader(strIo)
    trailer_dict = {
    str(i[15]): trailer(str(i[15].strip()), -1, int(i[7]), int(i[9]), int(i[10]), int(i[11]), int(i[12]), int(i[13]),
                        -1, -1, (map(int, ((i[6] + '、' + i[19]).split('、')))), 1,
                        datetime.strptime('2015-06-1', '%Y-%m-%d').date(), -1, -1, -1, -1, -1, -1, int(i[0]), -1, -1,
                        -1)for i in input_file}
    var_dict['trailer_dict'] = trailer_dict

    mixCity_tmpFile = request.form.get("mix_city")
    strIo = StringIO(mixCity_tmpFile)
    mix_city = pd.read_csv(strIo)
    var_dict['mix_city'] = mix_city

    OTD_pinche_tmpFile = request.form.get("OTD_pinche")
    strIo = StringIO(OTD_pinche_tmpFile)
    OTD_pinche = pd.read_csv(strIo)
    var_dict['OTD_pinche'] = OTD_pinche

    # for key in request.form.keys():
    #     tmpFile = request.form.get(key)
    #     strIo = StringIO(tmpFile)
    #     df = pd.read_csv(strIo, header=None)
    #     input_dict[key] = df
    print var_dict

    return var_dict