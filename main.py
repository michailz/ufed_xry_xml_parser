#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import datetime
import glob
import sys
from core.myfunc import *
import psycopg2
from core.ufedfunc import *
from core.xryfunc import *
from bs4 import BeautifulSoup
import io


try:
    conn = psycopg2.connect("host=localhost dbname=phonebook user=postgres password=root")
    cur = conn.cursor()
except Exception:
    sys.exit('Could not connect to DB!')

file_path = './files/'

job_todo = glob.glob(file_path + "*.xml")
for file in job_todo:
    md5 = generate_file_md5(file, blocksize=2 ** 20)
    if check_if_file_exists(cur, md5) is None:
        message = "File: '%s' with md5: '%s' was added to database." % (file, md5)
        file_id = append_file_into_db(conn, cur, md5, file)
        information_id = create_information_about_file(conn, cur, message, file_id)
        with open(file) as f:
            first_line = f.readline()
            """
            ufed first line: <?xml version="1.0" encoding="utf-8"?>
            xry first line: <?xml version="1.0" encoding="utf-8" standalone="yes"?>
            """
            if 'standalone' not in first_line:
                with open(file) as f:
                    soup = BeautifulSoup(f, 'lxml-xml')
                ufed_update_basic_information(conn, cur, soup, file_id)
                ufed_insert_general_information(conn, cur, soup, file_id, information_id)
                ufed_insert_contact_information(conn, cur, soup, file_id, information_id)
            else:
                """
                    XRY uses UTF-8 with BOM encoding
                """
                with io.open(file, encoding='utf-8-sig') as f:
                    soup = BeautifulSoup(f, 'lxml-xml')
                xry_update_basic_information(conn, cur, soup, file_id)
                xry_insert_general_information(conn, cur, soup, file_id, information_id)
                xry_insert_account_information(conn, cur, soup, file_id, information_id)
                xry_insert_contact_information(conn, cur, soup, file_id, information_id)
        print('File: ', file, ' with MD5: ', md5, ' completed!')
    else:
        print('Warning! File: ', file, ' with MD5: ', md5, ' already exists in DB')
        pass

cur.close()
conn.close()

