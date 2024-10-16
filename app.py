import os
import sys

import gradio as gr

from loguru import logger

from ui import main_ui

logging_level = os.environ.get("LOG_LEVEL", "DEBUG")
logger.configure(handlers=[{"sink": sys.stdout, "level": logging_level}])
logger.info("Starting Zeppelin Gradio Demo")

description = '<div align="center"> <h1>Price forecasting for used construction equipment</h1> </div>'

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown(description)
    main_ui()

demo.queue()
demo.launch()
