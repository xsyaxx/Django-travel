#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
# 这段脚本是 Django 项目的入口文件之一，
# 名字通常是 manage.py，它是开发和管理 Django 项目的 命令行工具脚本。

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', '去哪儿旅游数据分析推荐系统.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
