from scapy.all import sniff, Raw, UDP  # requires scapy

# results list (each entry is a dict with metadata + payload)
captured = []

def handler(pkt):
    # Only handle UDP packets that carry a Raw payload
    if UDP in pkt and Raw in pkt:
        payload = bytes(pkt[Raw].load)  # ensure bytes
        # try UTF-8 decode for readability, otherwise keep None
        try:
            text = payload.decode("utf-8", errors="ignore")
        except Exception:
            text = None

        captured.append(text)

def sniff_for(duration=6, iface=None, bpf_filter="udp"):
    """
    Run sniff for `duration` seconds, return the captured list.
    - duration: seconds to run (default 6)
    - iface: optional network interface name (e.g., "eth0", "wlan0"); None means default
    - bpf_filter: libpcap filter string (default "udp")
    """
    sniff(filter=bpf_filter, prn=handler, timeout=duration, store=0, iface=iface)
    return captured

def scanner(duration=6):
    packets = sniff_for(duration)
    
    hosts = list()
    for packet in packets:
        if packet.split(':')[0] == 'DarkChat':
            host = packet.split(':')[1]
            hosts.append(host)
    
    return set(hosts)
