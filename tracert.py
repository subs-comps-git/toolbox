import socket
import sys


def main(dest_name):
    dest_addr = socket.gethostbyname(dest_name)
    host = socket.gethostbyname(socket.gethostname())
    port = 33434
    max_hops = 30
    icmp = socket.getprotobyname('icmp')
    udp = socket.getprotobyname('udp')
    ttl = 1
    print("Tracing: {0} ({1})".format(dest_name, dest_addr))

    while True:
        recv_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
        send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, udp)
        send_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)

        recv_socket.settimeout(2.5)
        recv_socket.bind((host, port))
        send_socket.sendto(b"", (dest_addr, port))
        curr_addr = None
        curr_name = None

        try:
            _, curr_addr = recv_socket.recvfrom(128)
            curr_addr = curr_addr[0]
            try:
                curr_name = socket.gethostbyaddr(curr_addr)[0]
            except socket.error:
                curr_name = curr_addr
        except (KeyboardInterrupt, SystemExit):
            sys.exit(1)
        except socket.error:
            pass
        finally:
            send_socket.close()
            recv_socket.close()

        if curr_addr is not None:
            curr_host = "%s  (%s)" % (curr_name, curr_addr)
        else:
            curr_host = "*"
        # print "%d\t%s" % (ttl, curr_host)
        print("%d\t%s" % (ttl, curr_host))

        ttl += 1
        if curr_addr == dest_addr or ttl > max_hops:
            break


if __name__ == '__main__':
    try:
        main(sys.argv[1])
    except IndexError:
        print("Usage: {0} www.google.com".format(sys.argv[0]))

