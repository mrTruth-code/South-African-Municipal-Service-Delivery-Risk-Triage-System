import os
import sys

# Ensure project root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.app import build_app

# Instantiate the Gradio Blocks demo
demo = build_app()

# Top-level ASGI/WSGI exports for cloud hosts
app = getattr(demo, "app", demo)
application = app
handler = app

if __name__ == "__main__":
    demo.launch()
