from rich.console import Console
from rich.theme import Theme
from rich.markdown import Markdown
from rich.text import Text

import time

# 自定义主题颜色，方便统一修改
custom_theme = Theme({
    "info": "cyan",
    "log": "bright_black",
    "warning": "yellow",
    "error": "bold red",
    "markdown.code": "cyan",
    "markdown.h1": "bold green underline",
})

# 单例 Console 对象
global_console = Console(theme=custom_theme, record=True)

def print(text):
    global_console.print(text)

def printer(markup_text: str, delay: float = 0.02, end: str = "\n"):
    """
    实现了打字机效果的打印函数，兼容 Rich Markup。
    
    Args:
        markup_text: 包含 rich 标签的字符串
        delay: 每个字符的打印延迟（秒）
        end: 打印结束后的后缀（通常是换行）
    """
    text_obj = Text.from_markup(markup_text)
    segments = text_obj.render(global_console)
    for segment in segments:
        content, style, control = segment
        if control:
            global_console.control(control)
            continue
        for char in content:
            global_console.print(char, style=style, end="")
            time.sleep(delay)
    global_console.print(end, end="")

if __name__ == "__main__":
    printer("[info]Hello![/info] [warning]Are you ok?[/warning]")
    global_console.print("[error]Wish you a nice day![/error]")
    global_console.print("[log]This is a daily log.[/log]")
    global_console.print(
       Markdown(
        """
# Are you ok?
Did you have a nice day?
```python
print("I am happy everyday!")
```
        """
       ) 
    )
