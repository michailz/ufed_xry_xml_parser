#!/usr/bin/python
# -*- coding: utf-8 -*-

import hashlib


def clean_string(string):
    return ' '.join(string.replace('\n', ' ').replace('"', ' ').replace('„', ' ').replace('<U+0085>', ' ').
                    replace('“', ' ').replace('"', ' ').split())


def generate_file_md5(filename, blocksize=2 ** 20):
    m = hashlib.md5()
    with open(filename, "rb") as f:
        while True:
            buf = f.read(blocksize)
            if not buf:
                break
            m.update(buf)
    return m.hexdigest()


def check_if_file_exists(cur, md5):
    cur.execute('SELECT * FROM files WHERE "md5" = %s', [md5])
    result = cur.fetchone()
    return result


def append_file_into_db(conn, cur, md5, file):
    cur.execute('INSERT INTO files (md5, file_name, parsing_time) values (%s, %s, now()) returning id', (md5, file))
    conn.commit()
    result = cur.fetchone()
    return result[0]


def create_information_about_file(conn, cur, message, file_id):
    cur.execute(
        "INSERT INTO information (description, file_id, information_timestamp) values (%s, %s, now()) returning id",
        (message, file_id))
    conn.commit()
    result = cur.fetchone()
    return result[0]
