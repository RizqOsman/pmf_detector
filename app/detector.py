from scapy.all import sniff, Dot11Beacon, Dot11Elt
from typing import Dict

results: Dict[str, Dict[str, bool]] = {}

def parse_rsn(rsn_bytes):
    pmf_required = rsn_bytes[19] & 0b10000000  # Bit 7 of byte 19
    pmf_capable  = rsn_bytes[18] & 0b01000000  # Bit 6 of byte 18
    return bool(pmf_capable), bool(pmf_required)

def handle_packet(pkt):
    if pkt.haslayer(Dot11Beacon):
        ssid = pkt[Dot11Elt].info.decode(errors="ignore")
        rsn = pkt.getlayer(Dot11Elt, ID=48)  # RSN Information Element
        if rsn:
            rsn_bytes = bytes(rsn)
            if len(rsn_bytes) > 20:
                pmf_capable, pmf_required = parse_rsn(rsn_bytes)
                results[ssid] = {
                    "pmf_capable": pmf_capable,
                    "pmf_required": pmf_required
                }

def sniff_pmf(interface):
    print(f"[INFO] Scanning interface: {interface}")
    sniff(iface=interface, prn=handle_packet, timeout=15, store=0)
