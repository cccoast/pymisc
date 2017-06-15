# -*- coding: utf-8 -*-
__author__ = 'luchanghong'
import rsa
import base64

(pubkey, privkey) = rsa.newkeys(1024)
pub = pubkey.save_pkcs1("DER")
pub = base64.encodestring(pub)
pubfile = open('pub.txt','w+')
pubfile.write(pub)
pubfile.close()
     
pri = privkey.save_pkcs1("DER")
pri = base64.encodestring(pri)
prifile = open('pri.txt','w+')
prifile.write(pri)
prifile.close()

message = 'hello'
with open('pub.txt') as publickfile:
    p = publickfile.read()
#     p = base64.decodestring(p)
    pubkey = rsa.PublicKey.load_pkcs1(p)

with open('pri.txt') as privatefile:
    p = privatefile.read()
#     p = base64.decodestring(p)
    privkey = rsa.PrivateKey.load_pkcs1(p)

crypto = rsa.encrypt(message, pubkey)
crypto = base64.encodestring(crypto)
print crypto
crypto = base64.decodestring(crypto)
message = rsa.decrypt(crypto, privkey)
print message

# signature = rsa.sign(message, privkey, 'SHA-1')
# rsa.verify('hello', signature, pubkey)