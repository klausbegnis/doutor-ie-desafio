"""
File: main.py
Project: app
File Created: Friday, 11th July 2025 9:26:52 am
Author: Klaus Begnis (kbegnis23@gmail.com)
-----
Last Modified: Friday, 11th July 2025 9:27:18 am
Modified By: Klaus Begnis (kbegnis23@gmail.com>)
-----
Copyright (c) - Creative Commons Attribution 2025
"""

from fastapi import FastAPI

from src.app.routes.consulta_router import consulta_router

app = FastAPI()
app.include_router(consulta_router)
