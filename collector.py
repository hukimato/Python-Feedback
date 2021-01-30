import socket
from multiprocessing import Process, Queue
import imaplib
import os
import time
import email
from os.path import join, dirname
from dotenv import load_dotenv
import logging

dotenv_path = join(dirname(""), '.env')
load_dotenv(dotenv_path)
EMAIL_LOGIN = os.environ.get("EMAIL_LOGIN")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
PERIOD_CHECK = int(os.environ.get("PERIOD_CHECK"))

HOST_COLLECTOR = '127.0.0.1'
PORT_COLLECTOR = 50008

IDs = Queue()


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST_COLLECTOR, PORT_COLLECTOR))
    s.listen(1)
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(EMAIL_LOGIN, EMAIL_PASSWORD)
        while True:
            data = conn.recv(1024)
            IDs.put(data.decode())
            if not IDs.empty():
                mail.list()
                mail.select("inbox")
                result, data = mail.search(None, "ALL")

                ids = data[0]
                id_list = ids.split()
                latest_email_id = id_list[-1]

                result, data = mail.fetch(latest_email_id, "(RFC822)")
                raw_email = data[0][1]
                raw_email_string = raw_email.decode('utf-8')
                email_message = email.message_from_string(raw_email_string)

                if email_message['Subject'] == IDs.get():
                    logging.basicConfig(filename="success_request.log", level=logging.INFO)
                    logging.info(email_message['Subject'])
                    body = email_message.get_payload(decode=True).decode('utf-8')
                    logging.info(body)
                else:
                    logging.basicConfig(filename="error_request.log", level=logging.INFO)
                    body = email_message.get_payload(decode=True).decode('utf-8')
                    logging.error(body)
            time.sleep(PERIOD_CHECK)
            conn, addr = s.accept()

