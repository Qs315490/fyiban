#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Sricor
# @Date: 2021-10-20
# 易班用到的加密


from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5, AES
from base64 import b64encode, b64decode

AES_KEY = '2knV5VGRTScU7pOq'
AES_IV = 'UmNWaNtM0PUdtFCs'
RSA_KEY = '''-----BEGIN PUBLIC KEY-----
        MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEA6aTDM8BhCS8O0wlx2KzA
        Ajffez4G4A/QSnn1ZDuvLRbKBHm0vVBtBhD03QUnnHXvqigsOOwr4onUeNljegIC
        XC9h5exLFidQVB58MBjItMA81YVlZKBY9zth1neHeRTWlFTCx+WasvbS0HuYpF8+
        KPl7LJPjtI4XAAOLBntQGnPwCX2Ff/LgwqkZbOrHHkN444iLmViCXxNUDUMUR9bP
        A9/I5kwfyZ/mM5m8+IPhSXZ0f2uw1WLov1P4aeKkaaKCf5eL3n7/2vgq7kw2qSmR
        AGBZzW45PsjOEvygXFOy2n7AXL9nHogDiMdbe4aY2VT70sl0ccc4uvVOvVBMinOp
        d2rEpX0/8YE0dRXxukrM7i+r6lWy1lSKbP+0tQxQHNa/Cjg5W3uU+W9YmNUFc1w/
        7QT4SZrnRBEo++Xf9D3YNaOCFZXhy63IpY4eTQCJFQcXdnRbTXEdC3CtWNd7SV/h
        mfJYekb3GEV+10xLOvpe/+tCTeCDpFDJP6UuzLXBBADL2oV3D56hYlOlscjBokNU
        AYYlWgfwA91NjDsWW9mwapm/eLs4FNyH0JcMFTWH9dnl8B7PCUra/Lg/IVv6HkFE
        uCL7hVXGMbw2BZuCIC2VG1ZQ6QD64X8g5zL+HDsusQDbEJV2ZtojalTIjpxMksbR
        ZRsH+P3+NNOZOEwUdjJUAx8CAwEAAQ==
        -----END PUBLIC KEY-----
        '''

def rsa_encrypt(rsa_key, data):
    """
    rsa_key: 密钥
    登录密码加密
    """
    data = bytes(data, encoding="utf8")
    encrypt = PKCS1_v1_5.new(RSA.importKey(rsa_key))
    Sencrypt = b64encode(encrypt.encrypt(data))
    return Sencrypt.decode("utf-8")

def aes_encrypt(aes_key, aes_iv, data):
    """
    aes_key: 密钥
    aes_iv: iv
    提交表单加密
    """
    aes_key = bytes(aes_key, 'utf-8')
    aes_iv = bytes(aes_iv, 'utf-8')
    data = bytes(data, 'utf-8')
    data = aes_pkcs7padding(data)
    cipher = AES.new(aes_key, AES.MODE_CBC, aes_iv)
    encrypted = b64encode(cipher.encrypt(data))
    return b64encode(encrypted)

def aes_decrypt(aes_key, aes_iv, data):
    """
    aes_key: 密钥
    aes_iv: iv
    提交表单解密
    """
    aes_key = bytes(aes_key, 'utf-8')
    aes_iv = bytes(aes_iv, 'utf-8')
    data = b64decode(b64decode(data))
    cipher = AES.new(aes_key, AES.MODE_CBC, aes_iv)
    decrypted = cipher.decrypt(data)
    #decrypted = aes_pkcs7unpadding(decrypted)
    return decrypted.decode('utf-8')

def aes_pkcs7padding(data):
    bs = AES.block_size
    padding = bs - len(data) % bs
    padding_text = bytes(chr(padding) * padding, 'utf-8')
    return data + padding_text

def aes_pkcs7unpadding(data):
    lengt = len(data)
    unpadding = ord(data[lengt - 1])
    return data[0:lengt-unpadding]


if __name__ == '__main__':
    aes_key = '2knV5VGRTScU7pOq'
    aes_iv = 'UmNWaNtM0PUdtFCs'
    data = '' # 加密提交表单
    decrypt_data = aes_decrypt(aes_key, aes_iv, data)
    print(decrypt_data)