# -*- coding: utf-8 -*-
##############################################################################
#
#   远程调用实例
#
##############################################################################

import xmlrpclib

username = 'admin'
pwd = 'admin'
dbname = 'db_app_train'
model = 'amos.text'

sock_common = xmlrpclib.ServerProxy('http://localhost:8069/xmlrpc/common')
uid = sock_common.login(dbname, username, pwd)
print uid

sock = xmlrpclib.ServerProxy('http://localhost:8069/xmlrpc/object')

# search
args = []
ids = sock.execute(dbname, uid, pwd, 'amos.text', 'search', args)
print ids

# # read
# fields = ['name', 'user_id']
# res = sock.execute(dbname, uid, pwd, 'amos.text', 'read', ids, fields)
# print res

# # write
# values = {'street': '111111'}
# results = sock.execute(dbname, uid, pwd, 'amos.text', 'write', ids, values)

# # unlink
# id = [15]
# res = sock.execute(dbname, uid, pwd, 'amos.text', 'unlink', id)
# print ids

# search_read   未跑通
domain = [('name', '=', '666')]
fields = ['name', 'user_id']
res = sock.execute(dbname, uid, pwd, 'amos.text', 'search_read', domain, fields)
print res
