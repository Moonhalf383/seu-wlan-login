from src.main.common.interpreter import Interpreter
from src.main.client.console import printer, global_console
from rich.traceback import install
from curl_cffi import requests
import re
import json
import base64

def render_error(message:str):
    global_console.print(f'[error]{message}[/error]')
    global_console.print_exception(show_locals=True)


def login():
    try:
        config_file = 'config.json'
        pattern = re.compile(r'\{.*\}')

        try:
            r = requests.get(
                'https://w.seu.edu.cn/drcom/chkstatus?callback=dr1002',
                impersonate="chrome120",
                verify=False
            )
        except OSError:
            render_error("错误：连接失败。[系统错误]")
            return False

        if r.status_code != 200:
            render_error("错误：连接失败。[请求失败]")
            return False
        status = json.loads(pattern.findall(r.text)[0])

        if status['result'] == 1:
            global_console.print('[error]错误：你已经登录了 seu-wlan。[/error]')
            return False
        elif status['result'] != 0:
            render_error("错误：未知错误。")
            return False

        try:
            with open(config_file) as f:
                config = json.load(f)
        except IOError:
            global_console.print('[error]错误：配置文件 config.json 不存在。[/error]')
            with open(config_file, 'w') as f:
                config = {
                    'username': '',
                    'password': ''
                }
                json.dump(config, f, indent=2)
                return False

        if config['username'] == '' or config['password'] == '':
            global_console.print('[error]错误：请在配置文件 config.json 中填写用户名及密码。[/error]')
            return False

        login_url = 'https://w.seu.edu.cn:801/eportal/?c=Portal&a=login&callback=dr1003&login_method=1&user_account=%2C0%2C' + config['username'] + '&user_password=' + config['password'] + '&wlan_user_ip=' + status['v46ip']
        try:
            r = requests.get(login_url)
        except OSError:
            render_error("错误：连接失败。[系统错误]")
            return False

        if r.status_code != 200:
            render_error("错误：连接失败。[请求失败]")
            return False
        login = json.loads(pattern.findall(r.text)[0])

        if login['result'] != '1':
            message = base64.b64decode(login['msg']).decode()
            if message == 'ldap auth error':
                global_console.print('[error]错误：用户名或密码错误。[/error]')
            elif message == 'userid error1':
                global_console.print('[error]错误：用户名不存在。[/error]')
            elif message == 'userid error2':
                global_console.print('[error]错误：密码错误。[/error]')
            else:
                global_console.print('[error]错误：登录失败。[/error]')
            return False

        global_console.print('[info]登录成功。[/info]')
        return True

    except Exception as e:
        global_console.print(f'[error]{e}[/error]')
        return False

class LoginInterpreter(Interpreter):
    def __init__(self):
        super().__init__("login")

    def default_behavior(self, args):
        login()
