import csv
import os

import requests
import json

def MakeRequest(ip):
    url='https://api.abuseipdb.com/api/v2/check'

    querystring= {
        "ipAddress": ip,
        "maxAgeInDays": "90"
    }

    headers = {
        "Accept" : "application/json",
        "Key" : "2ec1026d83d8937d95a967dd5d1fdcc63b56b1264214977a0b383e8b92a4a122379c7706c033fbcd" #cambiare con la propria chiave privata di AbuseIp
    }


    response = requests.request(method="GET", url=url, headers=headers, params=querystring)
    decoderesponse= json.loads(response.text)
    #print(decoderesponse)
    return decoderesponse

def writeXlsx(decoderesponse,file):

    for index, entry in enumerate(decoderesponse):
            print(entry["data"]["ipAddress"])
            file.write(index + 1, 0, entry["data"]["ipAddress"])
            file.write(index + 1, 1, entry["data"]["abuseConfidenceScore"])
            file.write(index + 1, 2, entry["data"]["totalReports"])
            file.write(index + 1, 3, entry["data"]["isp"])
            file.write(index + 1, 4, entry["data"]["domain"])
            if entry["data"]["hostnames"]:
                file.write(index + 1, 5, ' '.join(entry["data"]["hostnames"]))
            else:
                file.write(index + 1, 5, "sconosciuto")
            file.write(index + 1, 6, entry["data"]["countryCode"])

    '''
    if decoderesponse["data"]["hostnames"]:

        writer.writerow([decoderesponse["data"]["ipAddress"], str(decoderesponse["data"]["abuseConfidenceScore"]), str(decoderesponse["data"]["totalReports"]),
              decoderesponse["data"]["isp"],decoderesponse["data"]["domain"], ' '.join(decoderesponse["data"]["hostnames"]),decoderesponse["data"]["countryCode"],"\n-------------\n"])
    else:
        writer.writerow(["Ip Address: " + decoderesponse["data"]["ipAddress"], "\n",
              "Confidence of Abuse: " + str(decoderesponse["data"]["abuseConfidenceScore"]) + "%","\n","Total Reports: " + str(decoderesponse["data"]["totalReports"]) , "\n" , "ISP: " +
              decoderesponse["data"]["isp"] + "\n" + "Domain: " + decoderesponse["data"]["domain"] , "\n" ,
              "Hostname: Sconosciuto","\n", "Country: "+decoderesponse["data"]["countryCode"],"\n-------------\n"])
    '''

    return file
    #print(json.dumps(decoderesponse, sort_keys=True, indent=4))

if __name__ == '__main__':
    MakeRequest("176.45.165.243")
