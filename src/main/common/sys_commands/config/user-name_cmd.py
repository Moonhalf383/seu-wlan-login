from src.main.common.interpreter import Interpreter
from src.main.client.console import printer
from main import ROOT_DIR
import os


class UserNameInterpreter(Interpreter):
    def __init__(self):
        super().__init__("username", description="配置SEU-WLAN登录用户名")

    def default_behavior(self, args):
        try:
            config_file = os.path.join(ROOT_DIR, "config.json")
        except Exception:
            printer("[error]无法读取配置文件，请检查路径是否正确。[/error]")
            return

        try:
            import json
        except ImportError:
            printer("[error]请确保已安装json模块。[/error]")
            return

        with open(config_file, "r") as f:
            config = json.load(f)
        if args:
            config["username"] = args[0]
            with open(config_file, "w") as f:
                json.dump(config, f, indent=2)
            printer(f"[info]用户名已设置为: {args[0]}[/info]")
        else:
            printer("[error]请输入用户名。例如：config username my_username[/error]")
