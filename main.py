from src.main.common.System_cmd import SystemInterpreter
from src.main.client.workflow import run_console

if __name__ == "__main__":
    root = SystemInterpreter()
    try:
        run_console(root) 
    except KeyboardInterrupt:
        print("\nAborted.")
    except Exception as e:
        print(f"An error occurred: {e}")
