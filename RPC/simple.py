import functools
import xmlrpclib
HOST = "10.1.100.59"
PORT = 8069
DB = 'test'
USER = 'admin'
PASS = 'admin'
ROOT = 'http://%s:%d/xmlrpc/' % (HOST,PORT)

# 1. Login
uid = xmlrpclib.ServerProxy(ROOT + 'common').login(DB,USER,PASS)
print "Logged in as %s (uid:%d)" % (USER,uid)

call = functools.partial(
    xmlrpclib.ServerProxy(ROOT + 'object').execute,
    DB, uid, PASS)

# 2. Read the sessions
sessions = call('openacademy.session','search_read', [('course_id.responsible_id', '!=', False)], ['name', 'seats', 'course_id'])
for session in sessions:
    print session['course_id']
    print "Session %s (%s seats)" % (session['name'], session['seats'])
    print 'Cours ID : %s' % session['course_id'][0]
    print 'Nom cours : %s' % session['course_id'][1]
    cours = call('openacademy.course','read', [session['course_id'][0],], ['responsible_id'])
    print 'Responsable cours : %s' % cours[0]['responsible_id'][1] if cours[0]['responsible_id'] else ''
    