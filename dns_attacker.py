#! /usr/bin/python3
#
# This python program attacks name servers by making many requests very quickly.

import string
import dns
import dns.resolver
from typing import List
from collections import Counter
import threading


charset_str = string.ascii_letters+string.digits+"-"+"|"


def resolve(name, quiet=False):
    try:
        answer = dns.resolver.resolve(name, 'A')
        if not quiet:
            print("[+] " + str(name) + " : " + str(answer[0]))
        return 1, str(answer[0])
    except dns.resolver.NXDOMAIN:
        if not quiet:
            print("[.] Resolved but no entry for " + str(name))
        return 2, None
    except dns.resolver.NoNameservers:
        if not quiet:
            print("[-] Answer refused for " + str(name))
        return 3, None
    except dns.resolver.NoAnswer:
        if not quiet:
            print("[-] No answer section for " + str(name))
        return 4, None
    except dns.exception.Timeout:
        if not quiet:
            print("[-] Timeout")
        return 5, None


def populate_list()->List[str]:

    name_lst=[]
    for c1 in charset_str:
        if c1 == "|":
            continue
        for c2 in charset_str:
            if c2 == "|":
                continue
            for c3 in charset_str:
                if c3 == "|":
                    continue
                name_lst.append(c1+c2+c3+".com")
    return name_lst

name_list = populate_list()
threads = []
for t in range(4):
    threads.append(threading.Thread(name_list, name=str(t)))

                answer = resolve(name, quiet=True)
                answer_str = str(answer[1])
                print(answer_str)
                ctr += 1





