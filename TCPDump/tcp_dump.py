from scapy.all import *

# NOTE: pyinstaller --onefile .\tcp_dump.py

def capture_traffic(packet):
    if packet.haslayer(IP) and packet.haslayer(TCP):
        print(packet[IP].src, packet[TCP])
        # Append the packet to a list for further processing if needed
        packets.append(packet)

def handle_siging(signal, frame):
    # Print a message and exit the script
    print("\nExiting...")
    sys.exit(0)
    
packets = []
sniff(filter="tcp and portrange 80-82", prn=capture_traffic)

# Save captured packets to a PCAP file
wrpcap("captured_traffic.pcap", packets)
