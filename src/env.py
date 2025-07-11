"""
File: env.py
Project: src
File Created: Friday, 11th July 2025 10:12:43 am
Author: Klaus Begnis (kbegnis23@gmail.com)
-----
Last Modified: Friday, 11th July 2025 10:18:22 am
Modified By: Klaus Begnis (kbegnis23@gmail.com>)
-----
Copyright (c) - Creative Commons Attribution 2025
"""

from pathlib import Path

DATABASE_URL = "postgresql://root:root@localhost:5432/doutor-ie"
CONTENT_SOURCES = [
    {
        "url": "https://doutorie.com.br/duvidas/",
        "path": Path("data/funcionalidades_plataforma_doutorie.txt"),
    },
    {
        "url": "https://doutorie.com.br/quem-somos/",
        "path": Path("data/quem-somos.txt"),
    },
]
