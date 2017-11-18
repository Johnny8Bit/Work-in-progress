'''
REST API script - for testing and development, does nothing specific

Script for interacting with REST APIs, specifically Cisco PI/APIC-EM/CMX
Requests library is licensed under Apache License

netpacket.net
'''
import sys, os, csv, json, requests

__author__ = 'Michal Kowalik'
__version__= '0.1'
__status__ = 'Prototype'

requests.packages.urllib3.disable_warnings()        # Silence security warning from self-signed certififatess

GET_ApiHealthRecords = '/webacs/api/v3/data/ApiHealthRecords.json?.full=true'
GET_ClientTraffics = '/webacs/api/v3/data/ClientTraffics'
GET_HistoricalClientTraffics = '/webacs/api/v3/data/HistoricalClientTraffics.json?.full=true'

def get_data(url):
    try:
        response = requests.get(GET_url, auth=(username, password), headers=headers, verify=False)
        #response = requests.get(GET_url, headers=headers, verify=False)
    except requests.exceptions.ConnectionError:
        print('API connection failed')
        sys.exit()
    if response.status_code == 401:
        print('HTTP 401 (Unauthorized), check credentials.')
        sys.exit()
    return response

def create_file():
    file_path = 'C:\\Users\\Home\\Dropbox\\Python\\API\\'
    file_name = 'api.txt'
    file_object = open(file_path + file_name, 'w')
    return file_object

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: <script_name>.py <IpAddress> <UserName> <Password>')
        sys.exit()
    else:
        host, username, password = sys.argv[1], sys.argv[2], sys.argv[3]
    #host = 'jsonplaceholder.typicode.com'

    headers = {
        'Connection' : 'close',          # Close TCP session after each request to not trigger request rate limit
        'timeout' : '5'                  # Seconds to wait for server response
        }

    api_call = GET_HistoricalClientTraffics
    GET_url = 'https://' + host + api_call
    response = get_data(GET_url)

    if response.status_code == 200:
        file_object = create_file()

        myjson = response.json()
        if type(myjson) == list:
            pass
        elif type(myjson) == dict:
            pass
            #for item in myjson['queryResponse']['entity']:
            #    print(item['apiHealthRecordsDTO']['clientIp']['address'])
            #print(str(myjson['queryResponse']['@count']) + ' entries')


        file_object.write(response.text)
        file_object.close()
    else:
        print('HTTP response code <> 200')
        sys.exit()
