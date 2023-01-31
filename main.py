import csv
import os
from tkinter import Tk
from tkinter.filedialog import askopenfilename

import xlsxwriter

from AbuseRequest import MakeRequest, writeXlsx


def main():
    Tk().withdraw()
    filename = askopenfilename()

    raw = []
    with open(filename, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            for i in row:
                raw.append(i.split(",")[0])

    Indirizzi = []
    for i in raw[2:]:
        Indirizzi.append(i.strip('\"'))

    print(Indirizzi)

    wb= xlsxwriter.Workbook("reports.xlsx")
    worksheet = wb.add_worksheet()

    bold = wb.add_format({'bold': True})

    worksheet.write('A1', 'Ip Address', bold)
    worksheet.write('B1', 'Confidence of Abuse', bold)
    worksheet.write('C1', 'Total Reports', bold)
    worksheet.write('D1', 'ISP', bold)
    worksheet.write('E1', 'Domain', bold)
    worksheet.write('F1', 'Hostname', bold)
    worksheet.write('G1', 'Country', bold)

    worksheet.set_column(0,7,30)

    data = []
    for ip in Indirizzi:
        data.append(MakeRequest(ip))

    print(data)

    writeXlsx(data,worksheet)

    wb.close()

    #os.startfile(os.path.abspath("reports.xlsx"))

if __name__ == '__main__':
    main()

