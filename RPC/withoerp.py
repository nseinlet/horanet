# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-TODAY OpenERP S.A. <http://www.odoo.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import argparse
import sys
import traceback
import os
import xml.etree.ElementTree as ET
import tempfile

from datetime import datetime, timedelta
from ftplib import FTP

import openerplib

def CreateCourses(connection):
    course_model = connection.get_model('openacademy.course')
    session_model = connection.get_model('openacademy.session')
    
    for i in xrange(0, 100):
        course_model.create({'name': 'Course 1/%s' % i})
        for j in xrange(0, 100):
            session_model.create({'name' : 'Session %s for course %s' % (j, i), 'course_id': i})
            
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Demo script')
    parser.add_argument('--host', dest='host', help='name or ip of the server')
    parser.add_argument('--port', dest='port', help='ip port of the server')
    parser.add_argument('--protocol', dest='protocol', help='protocol to use (xmlrpc, jsonrpc, xmlrpcs,...)')
    parser.add_argument('--db', dest='db', help='Database to use')
    parser.add_argument('--user', dest='login', default="admin", help='Login (default=admin)')
    parser.add_argument('--userid', dest='userid', default="0", help='User ID (default=0)')
    parser.add_argument('--password', dest='password', default="admin", help='Password (default=admin)')

    if len(sys.argv) == 1:
        sys.exit(parser.print_help())

    args = parser.parse_args()

    try:
        #Connect by xml-rpc
        user_id = None
        if args.userid and int(args.userid)>0:
            user_id = int(args.userid)
        connection = openerplib.get_connection(hostname=args.host,
                                               port=int(args.port),
                                               database=args.db,
                                               login=args.login,
                                               password=args.password,
                                               protocol=args.protocol)
        connection.check_login(force=False)
        CreateCourses(connection)
            

    except Exception, e:
        tb = traceback.format_exc()
        print e
        print tb
        sys.exit(1)
