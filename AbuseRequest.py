import csv
import os

import requests
import json

def MakeRequest(ip, file):
    url='https://api.abuseipdb.com/api/v2/check'

    querystring= {
        "ipAddress": ip,
        "maxAgeInDays": "90"
    }

    headers = {
        "Accept" : "application/json",
        "Key" : "2ec1026d83d8937d95a967dd5d1fdcc63b56b1264214977a0b383e8b92a4a122379c7706c033fbcd" #cambiare con la propria chiave privata di AbuseIp
    }

    CsvHeader = ["Ip Address","Confidence of Abuse","Total Reports","ISP","Domain","Hostname","Country"]

    response = requests.request(method="GET", url=url, headers=headers, params=querystring)
    decoderesponse= json.loads(response.text)
    print(decoderesponse)

    writer = csv.writer(file)

    writer.writerow(CsvHeader)
    if decoderesponse["data"]["hostnames"]:
        writer.writerow([decoderesponse["data"]["ipAddress"], str(decoderesponse["data"]["abuseConfidenceScore"]), str(decoderesponse["data"]["totalReports"]),
              decoderesponse["data"]["isp"],decoderesponse["data"]["domain"], ' '.join(decoderesponse["data"]["hostnames"]),decoderesponse["data"]["countryCode"],"\n-------------\n"])
    else:
        writer.writerow(["Ip Address: " + decoderesponse["data"]["ipAddress"], "\n",
              "Confidence of Abuse: " + str(decoderesponse["data"]["abuseConfidenceScore"]) + "%","\n","Total Reports: " + str(decoderesponse["data"]["totalReports"]) , "\n" , "ISP: " +
              decoderesponse["data"]["isp"] + "\n" + "Domain: " + decoderesponse["data"]["domain"] , "\n" ,
              "Hostname: Sconosciuto","\n", "Country: "+decoderesponse["data"]["countryCode"],"\n-------------\n"])


    return file
    #print(json.dumps(decoderesponse, sort_keys=True, indent=4))

if __name__ == '__main__':
    MakeRequest("176.45.165.243")
