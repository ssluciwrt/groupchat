import socket, json, re, time, os

def client_run(*args):
    clt_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clt_sock.connect((args[0], args[1]))

    serv_banner = clt_sock.recv(1024).decode("utf-8")
    print(serv_banner, end='')
    alias_set = clt_sock.recv(1024).decode("utf-8")
    print(alias_set, end='')
    alias = input().encode("utf-8")
    clt_sock.sendall(alias)
    clt_sock.setblocking(False)

    pid = os.fork()
    if pid > 0:
        while True:
            try:
                data_recv = clt_sock.recv(1024).decode("utf-8")
                msg_recv = json.loads(data_recv)
                print("\n[{}] says: \"{}\"".format(msg_recv["from"], msg_recv["content"]))
            except BlockingIOError:
                time.sleep(0.01)
            except json.decoder.JSONDecodeError:
                exit(0)
    elif pid == 0:
        while True:
            msg_send = input("[{}] >>: ".format(alias.decode("utf-8")))
            if msg_send.upper() == 'Q':
                clt_sock.sendall(msg_send.encode("utf-8"))
                print("Quit")
                exit(0)
            clt_sock.sendall(msg_send.encode("utf-8"))


if __name__ == "__main__":
    client_run("127.0.0.1", 8008)