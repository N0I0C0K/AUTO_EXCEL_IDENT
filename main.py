import requests
import base64
import json

APP_KEY = ''
SEC_KEY = ''

def getToken() -> str:
    host = f'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={APP_KEY}&client_secret={SEC_KEY}'
    response = requests.get(host)
    if response.status_code == 200:
        return response.json()['access_token']

def ide_excel(file:str, token:str) -> json:
    request_url = "https://aip.baidubce.com/rest/2.0/solution/v1/form_ocr/request"
    with open(file, 'rb') as f:
        img = base64.b64encode(f.read())
    params = {'image':img}
    request_url = request_url + "?access_token=" + token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    temp = response.json()
    request_url = f'https://aip.baidubce.com/rest/2.0/solution/v1/form_ocr/get_request_result?access_token={token}'
    for item in temp['result']:
        id = item['request_id']
        params = {'request_id':id}
        res = requests.post(request_url, data=params, headers=headers)
        temp = res.json()
        while temp['result']['ret_code'] != 3:
            res = requests.post(request_url, data=params, headers=headers)
            temp = res.json()
        print(temp['result']['result_data'])
        url = temp['result']['result_data']
        with open(file.split('.')[0]+'.xls', 'wb') as f:
            f.write(requests.get(url).content)


def main():
    token = '24.240b519ced6fb82bb1515f1519c6c88d.2592000.1614607832.282335-23615925'
    print(token)
    ide_excel('4.jpg', token)
    return

if __name__ == "__main__":
    main()