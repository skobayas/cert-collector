import mysql.connector as mydb
import mysql
import datetime
import json

from get_cert_client import get_cert

def insert_pem(connection,cursor,results):

    # 要ou追加             : app_main => Done this script => Done
    # 要serialnumber追加   : app_main => Done this script => Done
    # 要l追加              : app_main => Done this script => Done
    # 要st追加             : app_main => Done this script => not yet
    # 要c追加              : app_main => Done this script => not yet

    # upsertするように変更すべき => Done

    cursor.execute("SELECT fqdn FROM certs WHERE fqdn=%s", (fqdn,))
    result = cursor.fetchone()

    if result == None:
        cursor.execute(
            "INSERT INTO certs (fqdn,cn,sans,o,ou,l,st,c,not_before,not_after,serial_number,issuer_cn,issuer_o,issuer_ou,last_update,cert_pem) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            (results['fqdn'], results['cn'], results['sans'], results['o'], results['ou'], results['l'], results['st'],
             results['c'],
             results['notBefore'], results['notAfter'], results['serialnumber'], results['issuer_cn'],
             results['issuer_o'], results['issuer_ou'], datetime.date.today(), results['cert_pem']
             ))
    else:
        cursor.execute("DELETE from certs WHERE fqdn=%s", (fqdn,))
        cursor.execute(
            "INSERT INTO certs (fqdn,cn,sans,o,ou,l,st,c,not_before,not_after,serial_number,issuer_cn,issuer_o,issuer_ou,last_update,cert_pem) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            (results['fqdn'], results['cn'], results['sans'], results['o'], results['ou'], results['l'], results['st'],
             results['c'],
             results['notBefore'], results['notAfter'], results['serialnumber'], results['issuer_cn'],
             results['issuer_o'], results['issuer_ou'], datetime.date.today(), results['cert_pem']
             ))

    # cursor.execute(
    #     "INSERT INTO certs (fqdn,cn,sans,o,ou,l,st,c,not_before,not_after,serial_number,issuer_cn,issuer_o,issuer_ou,last_update,cert_pem) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
    #     (results['fqdn'],results['cn'],results['sans'],results['o'],results['ou'],results['l'],results['st'],results['c'],
    #       results['notBefore'],results['notAfter'],results['serialnumber'],results['issuer_cn'],
    #      results['issuer_o'],results['issuer_ou'],datetime.date.today(), results['cert_pem']
    # ))

    connection.commit()

    # cursor.execute("select * from real_certs.certs")
    # rows = cursor.fetchall()
    # for item in rows:
    #     print (item)

def insert_err(connection,cursor,results):

    # upsertするように変更すべき

    #
    # cursor.execute("SELECT last_update FROM domain_update WHERE domain=%s", (domain,))
    # result = cursor.fetchone()
    #
    # if result == None:
    #     cursor.execute("INSERT INTO certs.domain_update VALUE (%s, %s)", (domain, datetime.date.today()))
    # else:
    #     cursor.execute("UPDATE domain_update SET last_update=%s WHERE domain=%s", (datetime.date.today(), domain))
    #




    cursor.execute("SELECT fqdn FROM error WHERE fqdn=%s", (fqdn,))
    result = cursor.fetchone()

    if result == None:
        cursor.execute(
            "INSERT INTO error (fqdn,err,last_update) VALUES (%s,%s,%s)", (results['fqdn'],results['err'],datetime.date.today()))

    else:
        cursor.execute("DELETE from error WHERE fqdn=%s", (fqdn,))
        cursor.execute(
            "INSERT INTO error (fqdn,err,last_update) VALUES (%s,%s,%s)", (results['fqdn'],results['err'],datetime.date.today()))

    connection.commit()

    # cursor.execute("select * from real_certs.error")
    # rows = cursor.fetchall()
    # for item in rows:
    #     print(item)

def test_insert_certs(results):
    #    入力：results
    #    出力：OK/NG   （将来対応）

    #   table:
    #         real_certsまたはerr

    connection = mydb.connect(
        host='127.0.0.1',
        port='3306',
        user='root',
        password='mysql',
        database='real_certs'
    )

    connection.ping(reconnect=True)
    # https: // stackoverflow.com / questions / 29772337 / python - mysql - connector - unread - result - found - when - using - fetchone
    cursor = connection.cursor(buffered=True)

    if results.get('err'):
        print (results['err'])
        insert_err(connection,cursor,results)
    else:
        print(results)
        insert_pem(connection,cursor,results)

#     # errのあるなしでtableを分けるか
#     # 特段に指定しないとNullになるっぽいので、現時点で確定していない項目は指定なしでいいでしょう

    connection.close()
    cursor.close()

fqdns=['untrusted-root.badssl.com','revoked.badssl.com','wrong.host.badssl.com','www.facebook.com']

    # print (get_cert('rc4-md5.badssl.com'))
    # print(get_cert('rc4.badssl.com'))
    # print(get_cert('3des.badssl.com'))
    # print(get_cert('null.badssl.com'))
    # print(get_cert('expired.badssl.com'))]

for fqdn in fqdns:
    fqdn_result = get_cert(fqdn)
    test_insert_certs(fqdn_result)

# fqdns=['untrusted-root.badssl.com','revoked.badssl.com','wrong.host.badssl.com']

# fqdn_result = get_cert('revoked.badssl.com')
# test_insert_certs(fqdn_result)
