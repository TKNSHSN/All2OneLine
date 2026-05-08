# All2OneLine

将 Python 脚本或 ELF/EXE 二进制文件转换为**一行命令 / Payload** 的工具，支持多平台终端环境，适用于 CTF 竞赛、渗透测试、红队行动等场景。

## 功能特性

- **Python 转一行命令** — 将任意 Python 代码/文件编码为一键执行的终端命令
- **ELF / EXE 转 Bash Payload** — 将二进制文件编码为 Linux Bash 一句话命令，落地即运行
- **多终端兼容** — 支持通用全平台、Linux/macOS Bash、Windows CMD、Windows PowerShell、Linux PowerShell、BusyBox（Docker/路由器）
- **Gzip 压缩** — 可选启用 gzip 压缩，大幅缩短最终命令长度
- **两种输出格式** — `python -c` 模式和管道（pipe）模式
- **GUI 界面** — 基于 Tkinter 的图形化工具，无需命令行即可操作
- **核心 API** — 纯 Python 实现，可直接 `import` 集成到其他项目中

## 项目结构

```
all2oneline/
├── all2oneline_core.py   # 核心模块（编码 + 命令生成）
├── all2oneline_gui.py    # Tkinter GUI 界面
└── demo.py               # API 调用示例（可用于其他项目集成）
```

## 快速开始

### 启动 GUI

```bash
python all2oneline_gui.py
```

界面包含两个标签页：

| 标签页 | 功能 |
|--------|------|
| **Python 转一行命令** | 选择 `.py` 文件或直接粘贴代码，生成一行命令 |
| **ELF/EXE 转 Bash 命令** | 选择二进制文件，生成 Bash 一句话 Payload |

### 在代码中集成

```python
from all2oneline_core import All2OneLineCore

# 示例：Python 代码 → 一行命令
code = """
import os
print("Hello from All2OneLine!")
os.system("whoami")
"""

b64 = All2OneLineCore.encode_code(code, use_gzip=True)
cmd = All2OneLineCore.generate_python_cmd(
    b64_str=b64,
    use_gzip=True,
    cmd_format="python_c",      # python_c 或 pipe
    term_type="universal"       # universal / bash / cmd / winps / linps / busybox
)
print(cmd)
```

### 二进制文件 → Bash Payload

```python
from all2oneline_core import All2OneLineCore

bin_data = All2OneLineCore.read_bin_file("payload.elf")
b64 = All2OneLineCore.encode_bin_data(bin_data, use_gzip=True)
cmd = All2OneLineCore.generate_bin_bash_payload(
    b64_str=b64,
    use_gzip=True,
    bin_type="elf"    # elf 或 exe
)
print(cmd)
```

更多示例见 [demo.py](./demo.py)。

## API 参考

### `All2OneLineCore`

| 方法 | 说明 |
|------|------|
| `read_file(filepath, encoding="utf-8")` | 读取文本文件内容 |
| `read_bin_file(filepath)` | 读取二进制文件内容 |
| `encode_code(code, use_gzip=False)` | 编码 Python 代码 → Base64（可选 gzip 压缩） |
| `encode_bin_data(data, use_gzip=False)` | 编码二进制数据 → Base64（可选 gzip 压缩） |
| `generate_python_cmd(b64_str, use_gzip, cmd_format, term_type)` | 生成 Python 一行命令 |
| `generate_bin_bash_payload(b64_str, use_gzip, bin_type)` | 生成二进制 Bash Payload |

### 参数说明

| 参数 | 可选值 | 说明 |
|------|--------|------|
| `cmd_format` | `python_c`, `pipe` | `python -c` 模式或管道模式 |
| `term_type` | `universal`, `bash`, `cmd`, `winps`, `linps`, `busybox` | 目标终端类型 |
| `bin_type` | `elf`, `exe` | 二进制文件类型 |
| `use_gzip` | `True`, `False` | 是否启用 gzip 压缩 |

## 依赖

- Python 3.6+
- 标准库：`base64`, `gzip`, `tkinter`（GUI 需要）

无需安装任何第三方库。

## 注意事项

- 本工具仅供**合法授权**的渗透测试、CTF 竞赛和安全研究使用
- 生成的命令/Payload 在目标系统上执行的行为由用户自行负责
- `demo.py` 中的示例文件（`test.py`、`test.elf`）需自行准备
