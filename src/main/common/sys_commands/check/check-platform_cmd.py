from src.main.common.interpreter import Interpreter
from src.main.client.console import printer

import platform


class CheckPlatformInterpreter(Interpreter):
    def __init__(self):
        super().__init__("platform", description="检查平台是否受到支持")

    def default_behavior(self, args):
        os_name = platform.system()
        printer(f"[warning]当前操作系统：{os_name}[/warning]")
        if os_name == "Linux":
            printer("[info]本脚本支持当前系统。[/info]")
        else:
            printer("[error]本脚本暂不支持当前系统。[/error]")
