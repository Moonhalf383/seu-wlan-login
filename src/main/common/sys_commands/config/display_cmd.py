from src.main.common.interpreter import Interpreter
from src.main.client.console import printer
from main import ROOT_DIR
import os


class ConfigDisplayInterpreter(Interpreter):
    def __init__(self):
        super().__init__("display", description="显示当前配置")

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
        printer(f"[info]username: {config['username']}[/info]")
        printer(f"[info]password: {config['password']}[/info]")
        printer("[info]配置显示完毕。[/info]")
