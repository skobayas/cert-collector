# dummy ?client

import requests
import json

import mysql.connector as mydb
import mysql
import datetime


URL = "http://127.0.0.1:5000/check?fqdn="

def get_cert(fqdn):
    r = requests.get(URL+fqdn)

    # need error handling

    # print (r.json())
    return r.json()

#     mysql insert



if __name__ == "__main__":
    # print (get_cert('not.amazon.co.jp'))
    # print (get_cert('us-free-1.appfw.net'))
    # print (get_cert('www.amazon.co.jp'))
    # print (get_cert('untrusted-root.badssl.com'))
    # print (get_cert('revoked.badssl.com'))
    # print (get_cert('wrong.host.badssl.com'))
    # print (get_cert('rc4-md5.badssl.com'))
    # print(get_cert('rc4.badssl.com'))
    # print(get_cert('3des.badssl.com'))
    # print(get_cert('null.badssl.com'))
    # print(get_cert('expired.badssl.com'))
    print(get_cert('www.facebook.com'))