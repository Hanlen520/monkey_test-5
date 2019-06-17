import requests


class Login(object):
    def login(self):
        url = "http://www3.ddwallet.net/ddwallet-app/user/login"
        data = {"password":"123456","mobile":"13600136126"}
        headers = {'Content-Type': 'application/json'}
        return requests.post(url=url, headers=headers, json=data)


if __name__ == '__main__':
    login = Login()
    response = login.login()
    print(response)
    actual_rsp_code = response.json()['code']
    print(response.json())
