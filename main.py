import platform
import re
import time
import clstr
from pyfiglet import Figlet
from net_analyzing import get_hosts, get_names
from netcutter import start_cutting_networks


def _is_admin() -> bool:
    if platform.system().lower() == 'windows':
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    else:
        import os
        return os.getuid() == 0


def _print_banner() -> None:
    f = Figlet(font='big')
    print(clstr.light_green('\n'.join(f.renderText('NetCutter').split('\n')[:-3:])))
    print(clstr.light_gray('by @RostF1rst'))


def _host_choice(hosts: dict[str, str]) -> list[str]:
    ips = list(hosts.keys())
    print(clstr.light_green('Found {} networks:'.format(len(hosts))))
    for ip, name in hosts.items():
        print(clstr.light_green(str(ips.index(ip) + 1) + ')'), clstr.light_cyan(ip), '---',
              clstr.light_yellow(name))

    print(clstr.
          light_green('Enter numbers of devices you want to cut off (for example: "1", "2 3 4", etc.) or 0 if each'))
    while True:
        choices = input(clstr.light_yellow('>>> '))
        if choices == '0':
            return ips
        if re.fullmatch(r'\d+(\s\d+)*', choices):
            choices = [int(s) - 1 for s in choices.split()]
            if any([0 <= i < len(hosts) for i in choices]):
                break
            else:
                print(clstr.light_red('No networks were chosen. Please try again.'))
        else:
            print(clstr.light_red('Incorrect input. Please try again.'))
    chosen_ips = []
    for i in choices:
        try:
            chosen_ips.append(ips[i])
        except IndexError:
            pass
    return chosen_ips


def main() -> int:
    _print_banner()
    print()
    if not _is_admin():
        print(clstr.
              light_red('No admin privileges. Try executing as su (Linux) or with admin rights (Windows). Quitting...'))
        return 0
    time.sleep(1)
    print(clstr.light_green('Scanning networks...'))
    hosts = get_hosts()
    if not hosts:
        print(clstr.light_red('Haven\'t found any networks. Quitting...'))
        return 0
    chosen_ips = _host_choice(get_names(hosts))
    start_cutting_networks(chosen_ips)
    while True:
        try:
            input(clstr.light_green('Currently working. Use ^C to stop.\n'))
        except KeyboardInterrupt:
            break
    return 0


if __name__ == '__main__':
    exit(main())
