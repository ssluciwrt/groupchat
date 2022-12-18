# Include functions for command line help

def help(arg):
    print(f"Usage: {arg} [IP] [Port]\n")
    print(f"IP\t\tThe IP address using for gcserver binds sevice.")
    print(f"Port\tThe transport layer identifier using for gcserver.")
    print(f"\nIf the server can not be started and gets \"address in use\" error message, check your TCP conn status with \"netstat\" tool.\n")

if __name__ == "__main__":
    help("gcserv")