#! /usr/bin/env python3

import socket
import sys
import os.path
import time


class TraceRoute:
    def __init__(self, destination_name):
        self.destination_name = destination_name
        self.destination_address = socket.gethostbyname(destination_name)
        self.max_hops = 30
        self.current_address = None
        self.current_name = None

    def send(self):
        # host = socket.gethostbyname(socket.gethostname())
        port = 33434
        icmp = socket.getprotobyname('icmp')
        udp = socket.getprotobyname('udp')
        ttl = 1

        print("Tracing: {0} ({1})".format(self.destination_name,
                                          self.destination_address))
        while True:
            receive_socket = socket.socket(socket.AF_INET,
                                           socket.SOCK_RAW,
                                           icmp)
            receive_socket.settimeout(2.5)
            # receive_socket.bind((host, port))

            send_socket = socket.socket(socket.AF_INET,
                                        socket.SOCK_DGRAM,
                                        udp)
            send_socket.setsockopt(socket.SOL_IP,
                                   socket.IP_TTL,
                                   ttl)
            time_sent = time.time()
            send_socket.sendto(b"", (self.destination_address, port))
            try:
                _, current_address = receive_socket.recvfrom(128)
                receive_time = time.time() - time_sent
                self.current_address = current_address[0]
                try:
                    self.current_name = socket.gethostbyaddr(
                        self.current_address)[0]
                except socket.error:
                    self.current_name = self.current_address
            except (KeyboardInterrupt, SystemExit):
                sys.exit(1)
            except socket.error:
                pass
            finally:
                send_socket.close()
                receive_socket.close()

            if self.current_address is not None:
                current_host = '{host}  ({address})'.format(
                    host=self.current_name,
                    address=self.current_address)
            else:
                current_host = '*'

            print("{ttl}\t{host} {time} msec".format(
                                            ttl=ttl,
                                            host=current_host,
                                            time=round(receive_time * 1000, 4)))

            if self.current_address == self.destination_address \
                    or ttl > self.max_hops:
                break
            ttl += 1


def main(destination_name):
    trace = TraceRoute(destination_name)
    trace.send()


if __name__ == '__main__':
    try:
        main(sys.argv[1])
    except IndexError:
        print("Usage: {0} www.google.com".format(
                os.path.basename(__file__)))
