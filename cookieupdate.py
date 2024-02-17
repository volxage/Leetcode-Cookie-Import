from getpass import getpass
import time

username = "volxage" #Replace with Leetcode username!!!

def login(wd):
    username_field = wd.find_element(By.ID, "id_login")
    password_field = wd.find_element(By.ID, "id_password")
    submit_button = wd.find_element(By.CLASS_NAME, "btn-content__2V4r")
    username_field.send_keys(username)
    password_field.send_keys(getpass())
    submit_button.click()

def write_cookies(csrf, session):
    file = open("../leetcode.toml", "r")
    lines = file.readlines()
    #TODO: Rewrite, search for 'csrf' line without loop.
    for line in lines:
        if(line.startswith("csrf")):
            lines[lines.index(line) + 1] = "session = \"" + session + "\"\n"
            lines[lines.index(line)] = "csrf = \"" + csrf + "\"\n"
            break
    file.close()
    file = open("../leetcode.toml", "w")
    file.writelines(lines)
    file.close()


opts = FirefoxOptions()
opts.add_argument("--headless")
wd = webdriver.Firefox(options = opts)

wd.get("https://leetcode.com/accounts/login")
while(wd.current_url != "https://leetcode.com/"):
    print("Logging in...")
    login(wd)
    i = 0
    while (wd.current_url != "https://leetcode.com/") and (i < 5):
        print("Waiting for successful sign-in... Current url: " + wd.current_url)
        i += 1
        time.sleep(1)

if(wd.current_url != "https://leetcode.com/"):
    print("Not logged in, cry about it.")

#try:
csrf =  wd.get_cookie("csrftoken")["value"]
session = wd.get_cookie("LEETCODE_SESSION")["value"]
write_cookies(csrf, session)
#except:
#    print("Cookie not found.")

wd.close()
