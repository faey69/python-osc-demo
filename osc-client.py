import argparse
import time
from typing import Union, Tuple, List

from pythonosc import udp_client
from pythonosc import osc_bundle_builder
from pythonosc import osc_message_builder

def send_msg_with_time(client: udp_client.SimpleUDPClient,
                       address: str,
                       value: Union[Tuple, List],
                       prev_time: float) -> float:
    """Sends an OSC message with the current timestamp (relative to the first message sent)."""
    now = time.perf_counter()
    delta = now - prev_time
    client.send_message(address, [*value, delta])
    prev_time = now
    return prev_time

if __name__ == "__main__":
    ip = "127.0.0.1"  # localhost
    port = 5005

    # Command line arguments (options)
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default=ip, help="The ip of the OSC server")
    parser.add_argument("--port", type=int, default=5005, help="The port the OSC server is listening on")
    args = parser.parse_args()

    # Connect to server at localhost on port 5005
    client = udp_client.SimpleUDPClient(args.ip, args.port)

    # Timestamp of first message sent
    start_perf = time.perf_counter()
    prev_time = start_perf  # Initialize prev_time with start_perf

    # Send a hello message
    prev_time = send_msg_with_time(client, "/hello", ("Hello", 123), prev_time)

    time.sleep(0.05)  # 50ms

    # Send a bye message
    prev_time = send_msg_with_time(client, "/bye", ["Bye", 321], prev_time)

    print("Message sent!")

    time.sleep(0.05) # 50ms

    # Send a message to default handler by using different address
    prev_time = send_msg_with_time(client, "/default/address", ["defVal", 555], prev_time)

    time.sleep(0.05)  # 50ms

    # Send a message to wildcard address handler
    prev_time = send_msg_with_time(client, "/tracking/vrsystem/somepath", ["fff", 222], prev_time)

    ###BUNDLE PART###
    # Create a bundle (executes immediately)
    bundle = osc_bundle_builder.OscBundleBuilder(osc_bundle_builder.IMMEDIATELY)

    # First message: to /hello
    msg1 = osc_message_builder.OscMessageBuilder(address="/hello")
    msg1.add_arg("Hello from bundle")
    msg1.add_arg(999)
    bundle.add_content(msg1.build())

    # Second message: to /bye
    msg2 = osc_message_builder.OscMessageBuilder(address="/bye")
    msg2.add_arg("Bye from bundle")
    msg2.add_arg(888)
    bundle.add_content(msg2.build())

    # Build the bundle
    built_bundle = bundle.build()

    # Send the bundle
    client.send(built_bundle)
    print("Bundle sent!")

