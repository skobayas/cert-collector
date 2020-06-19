# -*- coding: utf-8 -*-
# 日本語コメント

#gaeのライブラリをheroku用に転用
# printをpy3用に置き換え

# errorをどう表現するかね？？？

# jsonで
# err:null
# err:err description

# timeout指定が必要だな
# Done

# 現状ではRevokeのチェックはしていない
# CRLをdownloadするか、ocspで確認するかが必要ではあるな
# どちらにせよ、めんどい

import ssl
from ssl import SSLError
import socket

import dateutil.parser
import datetime

TIMEOUT = 5
socket.setdefaulttimeout(TIMEOUT)

context = ssl.create_default_context()

# context = ssl.SSLContext(ssl.PROTOCOL_TLS)
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
context.verify_mode = ssl.CERT_REQUIRED
context.check_hostname = True
context.load_verify_locations("ca-certificates.crt")

class Getcert(object):
    def __init__(self,fqdn):
        self.fqdn = fqdn
        # server_hostnameは小文字で与えるべし
        conn = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=fqdn.lower())
        try:
            conn.connect((fqdn, 443))
        except SSLError as err:
            self.err = {'err':err.strerror}
            # return results

        except socket.gaierror as err:
            # DNS lookup fail
            self.err = {'err':err.strerror}
            # return results

        except socket.error as err:
            # socket timeout?
            self.err = {'err':'May be socket timeout'}
            # return results

        else:
            self.err = {}
            self.cert_dic = conn.getpeercert()
            self.cert = ssl.get_server_certificate((fqdn, 443))
    def get_err(self):
        if self.err != {}:
            return self.err
        else:
            return None
    def get_fqdn(self):
        return self.fqdn

    def get_issuer_cn(self):
        for item in self.cert_dic['issuer']:
            if item[0][0] == 'commonName':
                return item[0][1]
    def get_notbefore(self):
        return self.cert_dic['notBefore']
    def get_notafter(self):
        return self.cert_dic['notAfter']

    def get_jpn_notbefore(self):
        return (dateutil.parser.parse(self.cert_dic['notBefore'])+datetime.timedelta(hours=9)).strftime("%Y/%m/%d %H:%M")

    def get_jpn_notafter(self):
        return (dateutil.parser.parse(self.cert_dic['notAfter'])+datetime.timedelta(hours=9)).strftime("%Y/%m/%d %H:%M")

    def get_cn(self):
        for item in self.cert_dic['subject']:
            if item[0][0]=='commonName':
                return item[0][1]

    def get_serialnumber(self):
        return self.cert_dic['serialNumber']

    def get_sans(self):
        sans = []
        for item in self.cert_dic['subjectAltName']:
            sans.append(item[1])
        return ','.join(sans)

    def get_ou(self):
        for item in self.cert_dic['subject']:
            if item[0][0]=='organizationUnit':
                return item[0][1]
    def get_st(self):
        for item in self.cert_dic['subject']:
            if item[0][0]=='stateOrProvinceName':
                return item[0][1]
    def get_l(self):
        for item in self.cert_dic['subject']:
            if item[0][0]=='localityName':
                return item[0][1]
    def get_c(self):
        for item in self.cert_dic['subject']:
            if item[0][0]=='countryName':
                return item[0][1]
    def get_issuer_o(self):
        for item in self.cert_dic['issuer']:
            if item[0][0]=="organizationName":
                return item[0][1]
    def get_issuer_ou(self):
        for item in self.cert_dic['issuer']:
            if item[0][0] == 'organizationalUnitName':
                    return item[0][1]
    def get_o(self):
        for item in self.cert_dic['subject']:
            if item[0][0] == 'organizationName':
                return item[0][1]
    def get_cert(self):
        return self.cert

if __name__ == '__main__':
    # cert=Getcert('www.amazon.com')
    # cert=Getcert('amazon.co.jp')

    # cert=Getcert('non-amazon.co.jp')
    # cert=Getcert('us-free-1.appfw.net')
    # cert=Getcert('revoked.badssl.com')
    cert=Getcert('www.facebook.com')

    if type(cert.get_err()) != None:
        # print (cert.get_sans())
        print(cert.get_serialnumber())
        # print(cert.get_l())
        # print(cert.get_c())
        # print cert.get_notbefore()
        # print cert.get_notafter()
        # print cert.get_commonname()
        # print (cert.get_cert())
        # print (cert.get_issuer_ou())
        # print (cert.get_cn())
        # print (cert.get_sans())
    else:
        print (cert.get_err())
    # jsonを返させる？？

    # err = Getcert.err()
    # if err:
    #
    # else:


    # print (cert.get_issuer_cn())
    # print cert.get_notbefore()
    # print cert.get_notafter()
    # print cert.get_commonname()
    # print (cert.get_cert())
    # print (cert.get_issuer_ou())
    # print (cert.get_cn())
    # print (cert.get_sans())

