from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.output import ColorDepth
from prompt_toolkit.styles import Style

from src.main.client.console import print, printer

from src.main.common.interpreter import Interpreter


class RecursiveInterpreterCompleter(Completer):
    """
    一个自定义的补全器，它会根据 Interpreter 的递归结构动态生成补全建议。
    """

    def __init__(self, root_interpreter: Interpreter):
        self.root = root_interpreter

    def get_completions(self, document, complete_event):
        """
        prompt_toolkit 会在每次按键时调用此方法。
        document: 包含了当前的输入文本和光标位置。
        """
        # 获取光标前的所有文本
        text_before_cursor = document.text_before_cursor

        try:
            parts = text_before_cursor.lstrip().split()
        except Exception:
            return
        word_under_cursor = document.get_word_before_cursor(WORD=True)
        current_interpreter = self.root
        if text_before_cursor.endswith(" "):
            path_parts = parts
        else:
            path_parts = parts[:-1] if parts else []
        for part in path_parts:
            if part in current_interpreter.sub_interpreters:
                current_interpreter = current_interpreter.sub_interpreters[part]
            else:
                return
        for name, sub_int in current_interpreter.sub_interpreters.items():
            if name.lower().startswith(word_under_cursor.lower()):
                yield Completion(
                    name,
                    start_position=-len(word_under_cursor),
                    display_meta=f"[{sub_int.description}]",  # 显示类名作为提示
                )


def run_console(root_interpreter: Interpreter):
    """
    启动带有自动补全功能的交互式控制台
    """
    # 1. 创建补全器
    completer = RecursiveInterpreterCompleter(root_interpreter)

    # 2. 创建会话 (Session)
    # history: 保存历史记录，支持上下键翻阅
    session = PromptSession(
        completer=completer,
        history=InMemoryHistory(),
        # 可以自定义样式
        style=Style.from_dict(
            {
                "prompt": "#98C379 bold",
                # ===== 补全菜单 =====
                "completion-menu": "bg:#222222 #ffffff",
                "completion-menu.completion": "bg:#222222 #aaaaaa",
                "completion-menu.completion.current": "bg:#8CC265 #000000 bold",
                # ===== 右侧 meta 信息 =====
                "completion-menu.meta.completion": "bg:#333333 #aaaaaa",
                # ===== 滚动条 =====
                "scrollbar.background": "bg:#444444",
                "scrollbar.button": "bg:#888888",
            }
        ),
        color_depth=ColorDepth.TRUE_COLOR,
    )

    printer(f"[info]Workflow started. Root: {root_interpreter.name}[/info]")
    printer("[info]Press Tab to autocomplete. Type 'exit' to quit.[/info]")

    while True:
        try:
            # 3. 读取输入 (prompt_toolkit 会处理补全 UI)
            # message 可以是动态的，显示当前上下文
            text = session.prompt(f"{root_interpreter.name}> ")

            if not text.strip():
                continue

            if text.strip() in ["exit", "quit"]:
                break

            # 4. 执行指令
            # 这里调用 Interpreter 的 execute 方法
            root_interpreter.execute(text)

        except KeyboardInterrupt:
            # Ctrl+C 处理
            continue
        except EOFError:
            # Ctrl+D 退出
            break
        except Exception as e:
            print(f"[error]Error: {e}[/error]")

    printer("[info]Goodbye![/info]")
