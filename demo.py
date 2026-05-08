#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Py2OneLine 核心模块使用 Demo
用于其他项目 import 集成调用
无 GUI、纯 API、可直接嵌入你的工具中
"""

from py2oneline_core import Py2OneLineCore

# ==============================================
# 示例 1：Python 代码 → 生成一行命令
# ==============================================
def demo_python_code_to_command():
    print("=" * 60)
    print("[Demo 1] Python 代码转一行命令")
    print("=" * 60)

    # 1. 你的 Python 代码
    code = """
import os
print("Hello from Py2OneLine!")
os.system("id")
"""

    # 2. 编码（可选压缩）
    use_gzip = True
    b64 = Py2OneLineCore.encode_code(code, use_gzip=use_gzip)

    # 3. 生成命令（支持各种平台）
    cmd = Py2OneLineCore.generate_python_cmd(
        b64_str=b64,
        use_gzip=use_gzip,
        cmd_format="python_c",    # python_c / pipe
        term_type="universal"     # universal / bash / cmd / winps ...
    )

    print("生成的一行命令：")
    print(cmd)
    print()


# ==============================================
# 示例 2：Python 文件 → 生成一行命令
# ==============================================
def demo_python_file_to_command():
    print("=" * 60)
    print("[Demo 2] Python 文件转一行命令")
    print("=" * 60)

    try:
        # 1. 读取文件
        code = Py2OneLineCore.read_file("test.py")

        # 2. 编码
        b64 = Py2OneLineCore.encode_code(code, use_gzip=True)

        # 3. 生成 PowerShell 专用命令
        cmd = Py2OneLineCore.generate_python_cmd(
            b64_str=b64,
            use_gzip=True,
            cmd_format="python_c",
            term_type="winps"
        )

        print("Windows PowerShell 专用命令：")
        print(cmd)

    except Exception as e:
        print("读取文件失败：", e)
    print()


# ==============================================
# 示例 3：ELF / EXE 二进制 → Bash Payload
# ==============================================
def demo_binary_to_bash():
    print("=" * 60)
    print("[Demo 3] ELF/EXE 转 Bash Payload")
    print("=" * 60)

    try:
        # 1. 读取二进制（ELF 或 EXE）
        bin_data = Py2OneLineCore.read_bin_file("test.elf")

        # 2. 压缩 + base64
        b64 = Py2OneLineCore.encode_bin_data(bin_data, use_gzip=True)

        # 3. 生成 Bash 命令
        payload = Py2OneLineCore.generate_bin_bash_payload(
            b64_str=b64,
            use_gzip=True,
            bin_type="elf"  # elf / exe
        )

        print("生成的 Linux Bash 命令：")
        print(payload)

    except Exception as e:
        print("处理二进制失败：", e)
    print()


# ==============================================
# 示例 4：只获取 Base64（自定义使用）
# ==============================================
def demo_only_base64():
    print("=" * 60)
    print("[Demo 4] 只输出压缩+Base64 字符串")
    print("=" * 60)

    code = "print('test')"
    b64 = Py2OneLineCore.encode_code(code, use_gzip=True)
    print("压缩后 Base64：", b64[:80], "...")
    print()


# ==============================================
# 运行所有示例
# ==============================================
if __name__ == "__main__":
    demo_python_code_to_command()
    demo_python_file_to_command()
    demo_binary_to_bash()
    demo_only_base64()