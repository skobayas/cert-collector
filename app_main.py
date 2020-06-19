# -*- coding: utf-8 -*-
# 日本語コメント

# import json
from flask import Flask,request,jsonify
import datetime
#これはローカルやIaasでは動くのだが、gaeに持っていくと動かない
#get_certの使用するライブラリがgaeの制約に該当するため
# gae用のものをheroku用に流用
# さちこさんの出力でよければsslで必要な情報は取れる
# （pyOpenSSLは不要）

from get_cert import Getcert

app = Flask(__name__)

# app.config['DEBUG'] = True

# /check にアクセスしたときの処理
@app.route('/check')
def check():
    results={}
    fqdn=request.args.get('fqdn')
    cert = Getcert(fqdn)

    # ここでエラー処理するか？
    if cert.get_err() != None:
        results['err'] = cert.get_err()['err']
        results['fqdn'] = cert.get_fqdn()
        # print (results)
        response = jsonify(results)
        # response.headers['ContentType'] ='application/json'
        return response
    else:
        # print (request.args.get('cert'))
        # if request.args.get('cert')=='y' or request.args.get('cert')=='Y':
        #     return cert.get_cert().replace('\\n','')
        # else:
        # results['cert_pem']=cert.get_cert().replace('\\n', '')
        results['fqdn']=cert.get_fqdn()
        results['cn']=cert.get_cn()

        results['ou'] = cert.get_ou()
        results['l'] = cert.get_l()

        results['st'] = cert.get_st()
        results['c'] = cert.get_c()

        results['issuer_cn']=cert.get_issuer_cn()
        results['issuer_o'] = cert.get_issuer_o()
        results['issuer_ou'] = cert.get_issuer_ou()
        results['notBefore']=cert.get_jpn_notbefore()
        results['notAfter']=cert.get_jpn_notafter()
        results['serialnumber'] = cert.get_serialnumber()
        results['sans']=cert.get_sans()
        results['o'] = cert.get_o()
        results['cert_pem'] = cert.get_cert().replace('\n', '')

        # results['last_update'] = datetime.date.today()

            # return json.dumps(results)だと日本語が文字化けする
            # ↓が必要
            # encoding = 'utf8', ensure_ascii = False

            # py3でエラーになる？？
            # return json.dumps(results,encoding='utf8',ensure_ascii=False)
        # return json.dumps(results)
        response = jsonify(results)
        # response.headers['ContentType'] ='application/json'
        return response

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)