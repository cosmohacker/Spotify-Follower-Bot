try:
    import requests, random, string, names
except ImportError:
    input(
        "Error while importing modules. Please install the modules in requirements.txt"
    )
    exit()


class spotify:
    def __init__(self, profile, proxy=None):
        self.session = requests.Session()
        self.profile = profile
        self.proxy = proxy

    def register_account(self):
        headers = {
            "Accept": "*/*",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded",
            "Referer": "https://www.spotify.com/",
        }
        name = names.get_first_name()
        surname = " " + names.get_last_name()
        domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'hotmail.co.uk', 'hotmail.fr', 'outlook.com', 'icloud.com', 'mail.com', 'live.com', 'yahoo.it', 'yahoo.ca', 'yahoo.in', 'live.se', 'orange.fr', 'msn.com', 'mail.ru', 'mac.com']
        random_domain = random.choice(domains)
        email = "".join(random.choices(string.ascii_letters + string.digits, k=8)) + f'@{random_domain}'
        password = ("").join(random.choices(string.ascii_letters + string.digits, k=8))
        birth_year = random.randint(1970, 2005)
        birth_month = random.randint(1, 12)
        birth_day = random.randint(1, 28)
        gender = random.choice(["male", "female"])

        # print(f"Email: {email}")
        # print(f"Password: {password}")
        # print(f"Birth Date: {birth_month}/{birth_day}/{birth_year}")
        # print(f"Name Surname: {name}/{surname}")
        # print(f"Gender: {gender}")


        proxies = None
        if self.proxy != None:
            proxies = {"https": f"http://{self.proxy}"}
        data = f"birth_day={birth_day}&birth_month={birth_month}&birth_year={birth_year}&collect_personal_info=undefined&creation_flow=&creation_point=https://www.spotify.com/uk/&displayname={name}{surname}&email={email}&gender={gender}&iagree=1&key=a298bb7fb9bb41dda7454f887a9060a7&password={password}&password_repeat={password}&platform=www&referrer=&send-email=1&thirdpartyemail=0&fb=0"

        try:
            create = self.session.post(
                "https://spclient.wg.spotify.com/signup/public/v1/account",
                headers=headers,
                data=data,
                proxies=proxies,
            )
            if "login_token" in create.text:
                login_token = create.json()["login_token"]
                with open("Created.txt", "a") as f:
                    f.write(f"{email}:{password}:{login_token}\n")
                return login_token
            else:
                return None
        except:
            return False

    def get_csrf_token(self):
        try:
            r = self.session.get(
                "https://www.spotify.com/uk/signup/?forward_url=https://accounts.spotify.com/en/status&sp_t_counter=1"
            )
            return r.text.split('csrfToken":"')[1].split('"')[0]
        except:
            return None

    def get_token(self, login_token):
        headers = {
            "Accept": "*/*",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded",
            "X-CSRF-Token": self.get_csrf_token(),
            "Host": "www.spotify.com",
        }
        self.session.post(
            "https://www.spotify.com/api/signup/authenticate",
            headers=headers,
            data="splot=" + login_token,
        )
        headers = {
            "accept": "application/json",
            "Accept-Encoding": "gzip, deflate, br",
            "accept-language": "en",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
            "spotify-app-version": "1.1.52.204.ge43bc405",
            "app-platform": "WebPlayer",
            "Host": "open.spotify.com",
            "Referer": "https://open.spotify.com/",
        }
        try:
            r = self.session.get(
                "https://open.spotify.com/get_access_token?reason=transport&productType=web_player",
                headers=headers,
            )
            return r.json()["accessToken"]
        except:
            return None

    def follow(self):
        if "/user/" in self.profile:
            self.profile = self.profile.split("/user/")[1]
        if "?" in self.profile:
            self.profile = self.profile.split("?")[0]
        login_token = self.register_account()
        if login_token == None:
            return None, "while registering, ratelimit"
        elif login_token == False:
            if self.proxy == None:
                return None, f"unable to send request on register"
            return None, f"bad proxy on register {self.proxy}"
        auth_token = self.get_token(login_token)
        if auth_token == None:
            return None, "while getting auth token"
        headers = {
            "accept": "application/json",
            "Accept-Encoding": "gzip, deflate, br",
            "accept-language": "en",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
            "app-platform": "WebPlayer",
            "Referer": "https://open.spotify.com/",
            "spotify-app-version": "1.1.52.204.ge43bc405",
            "authorization": "Bearer {}".format(auth_token),
        }
        try:
            self.session.put(
                # Playlist bot dont forget to change id
                # "https://api.spotify.com/v1/playlists/5gruZX4W0sSOtDIBXY8rR7/followers?type=user&ids=" + self.profile,
                # Dynamic User Bot
                "https://api.spotify.com/v1/me/following?type=user&ids=" + self.profile,
                headers=headers,
            )
            return True, None
        except:
            return False, "while following"
