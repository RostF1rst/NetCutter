import multiprocessing
import platform
import re
import socket
import subprocess


def _ping(host):
    system = platform.system().lower()

    try:
        if system == "windows":
            result = subprocess.run(["ping", "-n", "1", host], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    text=True)
            return "TTL=" in result.stdout
        else:
            result = subprocess.run(["ping", "-c", "1", host], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    text=True)
            return "1 packets transmitted, 1 received" in result.stdout

    except subprocess.CalledProcessError:
        return False


def _pings(j, q) -> None:
    while True:
        ip = j.get()
        if ip is None:
            break
        if _ping(ip):
            q.put(ip)


def _get_self_local_ip() -> str:
    platform_ = platform.system()

    if platform_ == 'Windows':
        result = subprocess.run(['ipconfig'], capture_output=True, text=True)
        ipconfig_output = result.stdout

        match = re.search(r'IPv4 Address\D+(192\.168\.100\.\d{1,3})', ipconfig_output)
        local_ip = match.group(1) if match else None

    elif platform_ == 'Linux':
        result = subprocess.run(['ifconfig'], capture_output=True, text=True)
        ifconfig_output = result.stdout

        match = re.search(r'inet \D*(192\.168\.100\.\d{1,3})', ifconfig_output)
        local_ip = match.group(1) if match else None

    else:
        raise NotImplementedError(f"Платформа {platform_} не поддерживается")

    return local_ip


def _get_name(ip: str) -> str:
    try:
        print(socket.gethostbyaddr(ip))
        return socket.gethostbyaddr(ip)[0]
    except socket.herror:
        return '[No name]'


def get_names(hosts: list) -> dict[str, str]:
    res = {}
    for host in hosts:
        res[host] = _get_name(host)
    return res


def get_hosts() -> list[str]:
    """
    Get IPs of all hosts in network
    :return: List of IP-addresses of hosts
    """
    ips = []
    jobs, res = multiprocessing.Queue(), multiprocessing.Queue()
    pool = [multiprocessing.Process(target=_pings, args=(jobs, res)) for _ in range(256)]

    for p in pool:
        p.start()

    for i in range(256):
        jobs.put(f'192.168.100.{i}')

    for _ in pool:
        jobs.put(None)

    for p in pool:
        p.join()

    while not res.empty():
        ip_ = res.get()
        ips.append(ip_)

    try:
        ips.remove('192.168.100.1')
    except ValueError:
        pass

    try:
        ips.remove(_get_self_local_ip())
    except ValueError:
        pass

    return ips
