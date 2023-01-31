from tkinter import Tk
from tkinter.filedialog import askopenfilename
from AbuseRequest import MakeRequest
import csv
import os

def main():
    #Tk().withdraw()
    #filename = askopenfilename()
    #f = open(filename, "r")
    raw = []
    with open('provacsv.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            for i in row:
                raw.append(i.split(",")[0])

    '''
    result = open("AbuseResults.txt", "a")
    if os.stat(os.path.abspath(result.name)).st_size != 0:
        open("AbuseResults.txt","w").close()
    '''
    Indirizzi = []
    for i in raw[2:]:
        Indirizzi.append(i.strip('\"'))

    print(Indirizzi)

    with open("report.csv","w", encoding="UTF8", newline='') as f:
        for ip in Indirizzi:
           MakeRequest(ip,f)
           print("\n")
        os.startfile(os.path.abspath(f.name))


if __name__ == '__main__':
    main()

