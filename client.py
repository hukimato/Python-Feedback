import socket
HOST = '127.0.0.1'
PORT = 50007

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        email = bytes(input("Введите почту: "), 'utf-8')
        msg = bytes(input("Введите сообщение: "), 'utf-8')
        s.sendall(email)
        s.sendall(msg)
        answer = (s.recv(1024)).decode()
        if answer != "OK":
            print(answer + "\n" + "Попробуйте ввести данные еще раз.")
        else:
            break
