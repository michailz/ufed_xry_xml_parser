#!/usr/bin/python
# -*- coding: utf-8 -*-

from .myfunc import clean_string
import datetime

def xry_insert_general_information(conn, cur, soup, file_id, information_id):
    try:
        general_information = soup.select('xryfile images image views view[type="general_view"]')[0]
        for section in general_information.findAll('properties'):
            properties = section.find_all('property')
            key = []
            value = []
            for general_property in properties:
                if general_property.get('type') == 'field_name':
                    key.append(general_property.text)
                if general_property.get('type') == 'field_data':
                    value.append(general_property.text)
            for i in range(len(key)):
                cur.execute('INSERT INTO devices(file_id, information_id, key, value) values \
                (%s, %s, %s, %s)', (file_id, information_id, key[i], value[i]))
            conn.commit()
    except IndexError:
        print('General information File_id:', file_id, 'is not available')


def xry_update_basic_information(conn, cur, soup, file_id):
    try:
        device_info_creation_time = clean_string(soup.select(
                'xryfile images image views view nodes node properties property[type="field_data"]')[0].text)
    except IndexError:
        device_info_creation_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    except ValueError:
        try:
            device_info_creation_time = datetime.datetime.strptime(device_info_creation_time, '%d/%m/%Y %H:%M:%S')
            device_info_creation_time = device_info_creation_time.strftime('%Y-%m-%d %H:%M:%S')
        except ValueError:
            device_info_creation_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    try:
        case_number = clean_string(soup.select('properties:contains("CASE_REFERENCE")')[0].
                                   select('properties property')[1].text)
    except IndexError:
        case_number = 'N/A'

    try:
        case_examiner_name = soup.select('properties:contains("CASE_OPERATOR")')[0]. \
            select('properties property')[1].text

    except IndexError:
        case_examiner_name = 'N/A'
    cur.execute('UPDATE files SET device_info_creation_time=%s, case_number=%s, case_examiner_name=%s \
    WHERE id = %s', (device_info_creation_time, case_number, case_examiner_name, file_id))
    conn.commit()


def xry_insert_account_information(conn, cur, soup, file_id, information_id):
    try:
        accounts = soup.select('xryfile images image views view[type="accounts_view"]')[0]
        for account in accounts.findAll('properties'):
            properties = account.find_all('property')
            key = []
            value = []
            for account_property in properties:
                key.append(account_property.get('type'))
                value.append(account_property.text)
            try:
                index = key.index('related_application')
                related_application = value[index]
                del key[index]
                del value[index]
            except ValueError:
                related_application = 'Other'
            cur.execute('INSERT INTO accounts(related_application, file_id, information_id) \
                                   values(%s, %s, %s) returning id', (related_application, file_id, information_id))
            conn.commit()
            source_account_id = cur.fetchone()
            cur.execute('INSERT INTO relations(information_id, file_id, source_account_id) values(%s, %s, %s)',
                        (information_id, file_id, source_account_id[0]))
            for i in range(len(key)):
                cur.execute('INSERT INTO fields(type, value, account_id, related_application) values \
                (%s, %s, %s, %s)', (key[i], value[i], source_account_id[0], related_application))
                if i % 100 == 0:
                    conn.commit()
            conn.commit()

    except IndexError:
        print("0 Account Warning!")


def xry_insert_contact_information(conn, cur, soup, file_id, information_id):
    try:
        contacts = soup.select('xryfile images image views view[type="contacts_view"]')[0]
        for contact in contacts.findAll('properties'):
            if contact.select('property[type="deleted"]'):
                continue
            properties = contact.find_all('property')
            key = []
            value = []
            for contact_property in properties:
                key.append(contact_property.get('type'))
                value.append(contact_property.text)
            try:
                index = key.index('related_application')
                related_application = value[index]
                del key[index]
                del value[index]
            except ValueError:
                related_application = 'Trivial PhoneBook'
            cur.execute('INSERT INTO accounts(related_application, file_id, information_id) \
                                   values(%s, %s, %s) returning id', (related_application, file_id, information_id))
            conn.commit()
            contact_account_id = cur.fetchone()
            cur.execute('INSERT INTO relations(information_id, file_id, contact_account_id) \
                                                               values(%s, %s, %s)',
                        (information_id, file_id, contact_account_id[0]))
            for i in range(len(key)):
                cur.execute('INSERT INTO fields(type, value, account_id, related_application) values \
                (%s, %s, %s, %s)', (key[i], value[i], contact_account_id[0], related_application))
                if i % 100 == 0:
                    conn.commit()
            conn.commit()

    except IndexError:
        print("0 Contacts Warning!")
