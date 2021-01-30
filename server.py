import socket
import random
from smtplib import SMTP
import os
from os.path import join, dirname
from dotenv import load_dotenv
from email_validator import validate_email, EmailNotValidError


dotenv_path = join(dirname(""), '.env')
load_dotenv(dotenv_path)
SMTP_HOST = os.environ.get("SMTP_HOST")
SMTP_PORT = os.environ.get("SMTP_PORT")
username = 'server.python.tmp@gmail.com'
password = 'server.python.tmp.07122020'
receiver = 'danay2211@gmail.com'

HOST = '127.0.0.1'
PORT = 50007
HOST_COLLECTOR = '127.0.0.1'
PORT_COLLECTOR = 50008

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            email = conn.recv(1024)
            msg = conn.recv(2048)
            try:
                valid = validate_email(email.decode())
                ID = email.decode() + str(hash(msg)) + str(random.getrandbits(10))  # Уникальный ID
                with SMTP(SMTP_HOST, SMTP_PORT) as smtp:
                    smtp.starttls()
                    smtp.login(username, password)
                    BODY = "\r\n".join((
                        "From: %s" % username,
                        "To: %s" % os.environ.get("EMAIL_LOGIN"),
                        "Subject: %s" % ID,
                        "",
                         msg.decode()
                    ))
                    smtp.sendmail(
                        username,
                        os.environ.get("EMAIL_LOGIN"),
                        BODY
                    )
                    BODY = "\r\n".join((
                        "From: %s" % username,
                        "To: %s" % receiver,
                        "Subject: %s" % ID,
                        ""
                    ))
                    smtp.sendmail(
                        username,
                        email.decode(),
                        BODY
                    )
                    conn.sendall(b'OK')
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as c:
                    c.connect((HOST_COLLECTOR, PORT_COLLECTOR))
                    c.sendall(bytes(ID, 'utf-8'))

            except EmailNotValidError as e:
                conn.sendall(b'Format Error')
            conn, addr = s.accept()