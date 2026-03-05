import os
import sys
import importlib.util
import inspect
import shlex

from src.main.client.console import printer, print 

ABS_PATH = os.path.dirname(__file__)

class Interpreter:
    def __init__(self, name: str = "System", plugin_dir: str = ""):
        """
        :param name: 当前解释器的名称（关键字）
        :param plugin_dir: 子解释器所在的目录路径（可选）
        """
        self.name = name
        self.sub_interpreters = {}  # 存储子解释器实例: {name: instance}
        
        # 如果指定了插件目录，则自动扫描并加载
        if plugin_dir:
            print("[log]Plugin dir found: {plugin_dir}[log]")
            print("[log]"+str(os.path.exists(plugin_dir))+"[/log]")
            self._load_plugins(plugin_dir)
        print(f"[log]Command {name} instantiated.[/log]")

    def _load_plugins(self, plugin_dir: str):
        """
        扫描指定目录下的 .py 文件，查找继承自 Interpreter 的类并实例化
        """
        if not os.path.exists(plugin_dir):
            print(f"[error]Path not found: {plugin_dir}[/error]")
            return

        # 遍历目录下的所有文件
        for filename in os.listdir(plugin_dir):
            if filename.endswith(".py") and filename != "__init__.py":
                file_path = os.path.join(plugin_dir, filename)
                module_name = filename[:-3]
                
                # 动态导入模块
                spec = importlib.util.spec_from_file_location(module_name, file_path)
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    sys.modules[module_name] = module
                    spec.loader.exec_module(module)
                    
                    # 检查模块中的类
                    for member_name, member_obj in inspect.getmembers(module):
                        if (inspect.isclass(member_obj) 
                            and issubclass(member_obj, Interpreter) 
                            and member_obj is not Interpreter): # 排除基类本身
                            
                            # 实例化子解释器
                            # 注意：这里假设子类构造函数不需要额外参数，
                            # 或者子类自己在 __init__ 中定义了自己的名字和子目录逻辑
                            try:
                                instance = member_obj()
                                self.sub_interpreters[instance.name] = instance
                                # print(f"[{self.name}] Loaded subcommand: {instance.name}")
                            except Exception as e:
                                print(f"[error]Error instantiating {member_name}: {e}[/error]")

    def execute(self, instruction: str):
        """
        解析指令并分发
        """
        # 使用 shlex 处理引号包含的参数，比 split() 更健壮
        # 例如: set msg "hello world" -> ['set', 'msg', 'hello world']
        try:
            parts = shlex.split(instruction)
        except ValueError:
            print("[error]Error: Syntax error in command.[/error]")
            return

        if not parts:
            self.default_behavior(None)
            return

        # print(parts)
        keyword = parts[0]
        
        # 递归分发逻辑
        if (keyword in self.sub_interpreters):
            remaining_args = parts[1:] 
            self.sub_interpreters[keyword]._execute(remaining_args)
        else:
            # 如果没有匹配的子关键字，执行当前解释器的默认行为
            self.default_behavior(parts)

    def _execute(self, instruction: list):
        if not instruction:
            self.default_behavior(None)
            return 
        # print(instruction)
        keyword = instruction[0]
        if keyword in self.sub_interpreters:
            remaining_args = instruction[1:]
            self.sub_interpreters[keyword]._execute(remaining_args)
        else:
            self.default_behavior(instruction)

    def default_behavior(self, args):
        """
        默认行为：当没有子解释器匹配时调用。
        子类应该重写这个方法来实现具体功能。
        """
        printer(f"[log]Command '{args[0]}' not recognized in module '{self.name}'.")
