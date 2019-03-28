#!/usr/bin/env python
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
import pandas as pd
import argparse
import xlrd
from collections import OrderedDict
import simplejson as json


parser = argparse.ArgumentParser(description="Filter user between files")
parser.add_argument("-s", "--source", required=True, help="Target file to be filtered")
#parser.add_argument("-d", "--destination", required=True, help="Population to be used")

args = vars(parser.parse_args())

source_file = args["source"]
#destination_file = args["destination"]

def excel_to_json(f1):
    # Open the workbook and select the first worksheet
    wb = xlrd.open_workbook(f1)
    sh = wb.sheet_by_index(0)
    # List to hold dictionaries
    users_list = []

    # Iterate through each row in worksheet and fetch values into dict
    for rownum in range(1, sh.nrows):
        users = OrderedDict()
        row_values = sh.row_values(rownum)
        users["User"] = row_values[0]
        users["Email"] = row_values[1]
        users["Data Source"] = row_values[2]
        users["Profile"] = row_values[3]
        users["Client Version"] = row_values[4]
        users["Client OS"] = row_values[5]
        users["Data Source Status"] = row_values[6]
        users["Backup Start Time"] = row_values[7]
        users["Backup End Time"] = row_values[8]
        users["Last Successful Backup Time"] = row_values[9]
        users["Files Backed Up"] = row_values[10]
        users["Files Missed"] = row_values[11]
        users["Bytes Transferred (MB)"] = row_values[12]
        users["Status"] = row_values[13]
        users["Backup Details"] = row_values[14]
        users["Backup Data (MB)"] = row_values[15]
        users["Allocated Quota (MB)"] = row_values[16]
        users["Total Backup Data (MB)"] = row_values[17]
        users["Storage Name"] = row_values[18]
        users["Last Connected"] = row_values[19]
        users_list.append(users)


    # Serialize the list of dicts to JSON
    j = json.dumps(users_list)
    '''
    # Write to file
    with open('data.json', 'w') as f:
        f.write(j)
    '''

    return j

def write_json(file):
    with open('data.json', 'w') as f:
        f.write(file)

def locate_users(f1, f2):
    df = pd.read_excel(f2)
    emails = df["Email"].values
    users = json.loads(f1)
    result = []

    for email in emails:
        for user in users:
            if email == user["Email"]:
                result.append(user)
    return result

def list_profile(profile):
    users = json.loads(profile)
    result = []

    for user in users:
        if user["Profile"] == "SH-SC2":
            result.append(user)

    return result

def main():
    #result = excel_to_json(source_file)
    #write_json(result)
    #result = locate_users(excel_to_json(source_file), destination_file)
    result = list_profile(excel_to_json(source_file))
    #print (result)
    df = pd.DataFrame(result)
    writer = pd.ExcelWriter("output.xlsx", engine="xlsxwriter")
    df.to_excel(writer, index=False)
    writer.save()




if __name__=="__main__":
    main()
