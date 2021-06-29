#!/usr/bin/env python3
import bluetooth
import sys
import pygatt
from binascii import hexlify
import time


def scan():

    nearby_devices = bluetooth.discover_devices(lookup_names=True)
    print("Found {} devices.".format(len(nearby_devices)))
    print(nearby_devices)
    for addr, name in nearby_devices:
        print("  {} - {}".format(addr, name))


def client(addr):

    if addr == None:
        print("No device specified. Searching all nearby bluetooth devices for "
            "the SampleServer service...")
    else:
        print("Searching for SampleServer on {}...".format(addr))

    # search for the SampleServer service
    uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
    service_matches = bluetooth.find_service(uuid=uuid, address=addr)

    if len(service_matches) == 0:
        print("Couldn't find the SampleServer service.")
        sys.exit(0)

    first_match = service_matches[0]
    port = first_match["port"]
    name = first_match["name"]
    host = first_match["host"]

    print("Connecting to \"{}\" on {}".format(name, host))

    # Create the client socket
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sock.connect((host, port))

    print("Connected. Type something...")
    while True:
        data = input()
        if not data:
            break
        sock.send(data)

    sock.close()


def server():

    server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    server_sock.bind(("", bluetooth.PORT_ANY))
    server_sock.listen(1)

    port = server_sock.getsockname()[1]

    uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

    bluetooth.advertise_service(server_sock, "SampleServer", service_id=uuid,
                                service_classes=[uuid, bluetooth.SERIAL_PORT_CLASS],
                                profiles=[bluetooth.SERIAL_PORT_PROFILE],
                                # protocols=[bluetooth.OBEX_UUID]
                                )

    print("Waiting for connection on RFCOMM channel", port)

    client_sock, client_info = server_sock.accept()
    print("Accepted connection from", client_info)

    try:
        while True:
            data = client_sock.recv(1024)
            if not data:
                break
            print("Received", data)
    except OSError:
        pass

    print("Disconnected.")

    client_sock.close()
    server_sock.close()
    print("All done.")



def gattConnector(addr, characteristic):

    if addr == None:
        print("No address specified. Exiting.")
        sys.exit(1)
    adapter = pygatt.GATTToolBackend()

    def handle_data(handle, value):
        """
        handle -- integer, characteristic read handle the data was received on
        value -- bytearray, the data returned in the notification
        """
        print("Received data: %s" % hexlify(value))

    try:
        adapter.start()
        device = adapter.connect(addr)
        
        # listen for music
        device.subscribe(characteristic,
                        callback=handle_data)

        # The subscription runs on a background thread. You must stop this main
        # thread from exiting, otherwise you will not receive any messages, and
        # the program will exit. Sleeping in a while loop like this is a simple
        # solution that won't eat up unnecessary CPU, but there are many other
        # ways to handle this in more complicated program. Multi-threaded
        # programming is outside the scope of this README.
        while True:
            time.sleep(10)
    finally:
        adapter.stop()
