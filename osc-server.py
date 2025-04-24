import argparse
import os
from pythonosc import dispatcher
from pythonosc import osc_server

def handle_hello(addr, *args):
    print(f"Received message at {addr}")
    print("Arguments from OSC client:")
    for i, arg in enumerate(args):
        print(f"  arg[{i}]: {arg} (type: {type(arg)})")

def handle_bye(addr, *args):
    print(f"Received message at {addr}")
    print("Arguments from OSC client:")
    for i, arg in enumerate(args):
        print(f"  arg[{i}]: {arg} (type: {type(arg)})")

def default_handler_function(addr, *args):
    for arg in args:
        print(f"Default handler: {addr} : {arg}")

def wildcard_address_test_function(addr, *args):
    for arg in args:
        print(f"Wildcard address handler: {addr} : {arg}")

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    ip = "127.0.0.1"
    port = 5005

    parser = argparse.ArgumentParser()
    parser.add_argument("--ip",
                        default=ip, help="The ip to listen on")
    parser.add_argument("--port",
                        type=int, default=port, help="The port to listen on")
    args = parser.parse_args()

    # Set up the dispatcher
    disp = dispatcher.Dispatcher()

    # Map OSC addresses to handler functions
    disp.map("/hello", handle_hello, "fixedArgHello", 100)
    disp.map("/bye", handle_bye, ["fixedArgBye", 200])
    disp.map("/tracking/*", wildcard_address_test_function)
    disp.set_default_handler(default_handler_function)

    # Create and start the server
    server = osc_server.ThreadingOSCUDPServer((args.ip, args.port), disp)
    print(f"Server running on {args.ip}:{args.port}...")
    server.serve_forever()
