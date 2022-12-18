import socket, time, re, json

def alias_validator(alias, conn_dict):
    if re.match(r"^\d+$", args[0]):
        return False
    if alias in dictx.values():
        return False
    return True

def broadcast(alias, msg, conn_dict):
    for each_conn, each_alias in conn_dict.items():
        if alias != each_alias:
            each_conn.sendall(json.dumps({"alias": each_alias, "content": msg, "from": alias}).encode("utf-8"))
            print("sent \"{}\" from {} to {}".format(msg, alias, each_alias))

def run_serv(*args):
    srv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv_sock.bind((args[0], args[1]))
    srv_sock.listen(args[2])
    srv_sock.setblocking(False) # setting server socket to nonblocking

    clt_conn_dict = {} # a dictionary for conn sockets storing
    alias = 0 # default starting alias before chatter gives one
    while True:
        try: # handling error from server socket nonblocking
            clt_conn, clt_addr = srv_sock.accept()
            clt_conn.setblocking(False) # setting client conn socket to nonblocking
            clt_conn_dict.update({clt_conn: alias})
            alias += 1
            print(f"Chatter from [{clt_addr[0]}:{clt_addr[1]}] is online.")
            clt_conn.sendall("=============== Welcome to \"GroupChat\" ==================\n\n".encode("utf-8"))
            clt_conn.sendall("Set your alias in chatting: ".encode("utf-8"))
        except BlockingIOError:
            time.sleep(0.1)
            
        for curr_conn, curr_alias in clt_conn_dict.items():
            if type(curr_alias) == int:
                try: # handling error from client conn socket nonblocking
                    new_alias = curr_conn.recv(32).decode("utf-8").rstrip('\n')
                    clt_conn_dict[curr_conn] = new_alias
                    print("Chatter from [{}: {}] renamed from {} to \"{}\"".format(curr_conn.getpeername()[0], curr_conn.getpeername()[1], curr_alias, new_alias))
                    break
                except BlockingIOError:
                    time.sleep(0.05)
            else:       
                try:
                    clt_data = curr_conn.recv(1024)
                    clt_msg = clt_data.decode("utf-8")
                    if clt_msg.rstrip('\n').upper() == 'Q' or clt_msg == '':
                        clt_conn_dict.pop(curr_conn)
                        print(f"Chatter from [{curr_conn.getpeername()[0]}:{curr_conn.getpeername()[1]}]({curr_alias}) is offline.")
                        curr_conn.close()
                        break
                    if not re.match(r"\s+", clt_msg):
                        print("[{}]-[{}:{}]- \"{}\"".format(curr_alias, curr_conn.getpeername()[0], curr_conn.getpeername()[1], clt_msg.rstrip('\n')))
                        broadcast(curr_alias, clt_msg.rstrip('\n'), clt_conn_dict)
                except BlockingIOError:
                    time.sleep(0.05)
                except OSError:
                    pass



if __name__ == "__main__":
    run_serv("127.0.0.1", 8008, 3)