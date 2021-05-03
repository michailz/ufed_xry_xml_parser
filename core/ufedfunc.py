#!/usr/bin/python
# -*- coding: utf-8 -*-

from .myfunc import clean_string
import datetime

def ufed_update_basic_information(conn, cur, soup, file_id):
    try:
        case_examiner_name = soup.select('project caseInformation field[fieldType="ExaminerName"]')[0].text
    except IndexError:
        case_examiner_name = 'N/A'
    try:
        case_number = soup.select('project caseInformation field[fieldType="CaseNumber"]')[0].text
    except IndexError:
        case_number = 'N/A'
    try:
        device_info_creation_time = soup.select('project metadata item[name="DeviceInfoCreationTime"]')[0].text
        device_info_creation_time = datetime.datetime.strptime(device_info_creation_time, '%d-%m-%Y %H:%M:%S')
        device_info_creation_time = device_info_creation_time.strftime('%Y-%m-%d %H:%M:%S')
    except IndexError:
        device_info_creation_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    except ValueError:
        try:
            device_info_creation_time = datetime.datetime.strptime(device_info_creation_time, '%d/%m/%Y %H:%M:%S')
            device_info_creation_time = device_info_creation_time.strftime('%Y-%m-%d %H:%M:%S')
        except ValueError:
            device_info_creation_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cur.execute('UPDATE files SET device_info_creation_time=%s, case_number=%s, case_examiner_name=%s \
        WHERE id = %s', (device_info_creation_time, case_number, case_examiner_name, file_id))
    conn.commit()


def ufed_insert_general_information(conn, cur, soup, file_id, information_id):
    try:
        section = soup.select('project metadata[section="Extraction Data"]')[0]
        items = section.find_all('item')
        key = []
        value = []
        for item in items:
            key.append(item.get('name'))
            value.append(item.text)
        for i in range(len(key)):
            cur.execute('INSERT INTO devices(file_id, information_id, key, value) values (%s, %s, %s, %s)',
                        (file_id, information_id, key[i], value[i]))
        conn.commit()
    except IndexError:
        print('General information File_id:', file_id, 'is not available')


def ufed_insert_contact_information(conn, cur, soup, file_id, information_id):
    try:
        items = soup.select('model[type="Contact"]')
        for item in items:
            keys = []
            values = []
            if item.get('deleted_state') == 'Intact':
                fields = item.findAll('field')
                for field in fields:
                    key = field.get('name')
                    value = field.findAll('value')
                    if len(value) > 0 and key not in ['UserMapping']:
                        keys.append(clean_string(key))
                        values.append(clean_string(value[0].text))
                multifields = item.findAll('multiField')
                for multifield in multifields:
                    key = multifield.get('name')
                    value = multifield.findAll('value')
                    if len(value) > 0:
                        keys.append(clean_string(key))
                        values.append(clean_string(value[0].text))

            if 'Source' in keys:
                related_application = values[keys.index('Source')]
            else:
                related_application = 'UFED Contact'
            if 'Account' in keys:
                ind = keys.index('Account')
                account = values[ind]
                del keys[ind]
                del values[ind]
                cur.execute('INSERT INTO accounts(related_application, file_id, information_id) \
                            values(%s, %s, %s) returning id',
                            (related_application, file_id, information_id))
                conn.commit()
                contact_account_id = cur.fetchone()
                cur.execute('INSERT INTO relations(information_id, file_id, source_account_id) values(%s, %s, %s)',
                            (information_id, file_id, contact_account_id[0]))
                cur.execute('INSERT INTO fields(type, value, account_id, related_application) values (%s, %s, %s, %s)',
                            ('UFED Account', account, contact_account_id[0], related_application))

            cur.execute('INSERT INTO accounts(related_application, file_id, information_id) \
                            values(%s, %s, %s) returning id',
                        (related_application, file_id, information_id))
            conn.commit()
            contact_account_id = cur.fetchone()
            cur.execute('INSERT INTO relations(information_id, file_id, contact_account_id) values(%s, %s, %s)',
                        (information_id, file_id, contact_account_id[0]))
            for i in range(len(keys)):
                cur.execute('INSERT INTO fields(type, value, account_id, related_application) values (%s, %s, %s, %s)',
                            (
                            clean_string(keys[i]), clean_string(values[i]), contact_account_id[0], related_application))
            conn.commit()

    except IndexError:
        print("0 Contacts Warning! %s" % information_id)
