import argparse
import platform

system = platform.system().lower()


def parse_args():
    parser = argparse.ArgumentParser(description='NetCutter - ARP-spoofing tool. !Arguments are NOT implemented at the moment!')

    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    parser.add_argument('-vc', '--verbose-scan', action='store_true', help='Gives more info about hosts')
    parser.add_argument('-t', '--targets', type=str, help='Skip scanning and attack provided hosts')

    return parser.parse_args()


args = parse_args()
