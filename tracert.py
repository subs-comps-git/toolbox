#! /usr/bin/env python3

import socket
import sys
import os.path
import time
import struct
import random
import string


class TraceRoute:
    def __init__(self, destination_name):
        self.destination_name = destination_name
        self.destination_address = socket.gethostbyname(destination_name)
        self.max_hops = 30
        self.ttl = 1
        self.current_address = None
        self.current_name = None

    def receive_message(self, receive_socket):
        """Receives ICMP time-exceeded messages from each hop along
        the path until the destination is reached or *max_hops* is exceeded.
        """
        try:
                _, current_address = receive_socket.recvfrom(128)
                # receive_time = time.time() - time_sent
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
        return self.current_address, self.current_name

    def send_message(self, send_socket, destination_name):
        """Sends a UDP packet to the destination on port 33434."""
        port = 33434

        size = 16
        s = struct.Struct(str(size) + 's')
        values = [random.choice(string.ascii_letters + string.digits) for n in range(size)]
        values = str.encode(''.join(values))
        data = s.pack(values)
        data = struct.pack(">d", time.time()) + data

        send_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, self.ttl)
        send_socket.sendto(data, (self.destination_address, port))
        port += 1

    def trace(self):
        """Handles iteration of send/receive messages and setup of sockets.
        Initial ttl=1,  then increments ttl and repeats until the destination
        is reached or *max_hops* is exceeded.
        """
        icmp = socket.getprotobyname('icmp')
        udp = socket.getprotobyname('udp')

        receive_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
        send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, udp)

        while True:
            send_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, self.ttl)
            time_sent = time.time()
            self.send_message(send_socket, self.destination_name)
            current_address, current_name = self.receive_message(receive_socket)
            receive_time = time.time() - time_sent

            if current_address is not None:
                current_host = '{host}  ({address})'.format(host=current_name,
                                                            address=current_address)
            else:
                current_host = '*'
            print("{ttl}\t{host} {time} msec".format(ttl=self.ttl,
                                                     host=current_host,
                                                     time=round(receive_time * 1000, 3)))

            if current_address == self.destination_address or self.ttl >= self.max_hops:
                break
            self.ttl += 1

        send_socket.close()
        receive_socket.close()


def main(destination_name):
    traceroute = TraceRoute(destination_name)
    traceroute.trace()


if __name__ == '__main__':
    try:
        main(sys.argv[1])
    except IndexError:
        print("Usage: {0} www.google.com".format(
                os.path.basename(__file__)))
