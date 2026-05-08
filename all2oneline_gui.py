# all2oneline_gui.py
import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext
from all2oneline_core import All2OneLineCore

class All2OneLineGUI:
    def __init__(self, root):
        self.full_py_cmd = ""
        self.full_bin_cmd = ""
        self.root = root
        self.core = All2OneLineCore()
        self.root.title("All2OneLine 终极稳定版 | Python/ELF/EXE  Payload 工具")
        self.root.geometry("920x750")

        self.notebook = ttk.Notebook(root)
        self.tab_py = ttk.Frame(self.notebook)
        self.tab_bin = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_py, text="Python 转一行命令")
        self.notebook.add(self.tab_bin, text="ELF/EXE 转Bash命令")
        self.notebook.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)

        self.build_python_tab()
        self.build_binary_tab()

    # ==================== Python 标签页 ====================
    def build_python_tab(self):
        tab = self.tab_py
        self.input_mode = tk.StringVar(value="file")

        ttk.Label(tab, text="输入方式：").grid(row=0, column=0, padx=6, pady=8, sticky="w")
        ttk.Radiobutton(tab, text="📁 选择Py文件", variable=self.input_mode, value="file", command=self.switch_mode_py).grid(row=0, column=1, sticky="w")
        ttk.Radiobutton(tab, text="✍️ 直接输入代码", variable=self.input_mode, value="code", command=self.switch_mode_py).grid(row=0, column=2, sticky="w")

        ttk.Label(tab, text="Python 文件：").grid(row=1, column=0, padx=6, pady=6, sticky="w")
        self.file_var = tk.StringVar(value="")
        self.file_entry = ttk.Entry(tab, textvariable=self.file_var, width=70)
        self.file_entry.grid(row=1, column=1, padx=5, pady=3)
        self.browse_btn = ttk.Button(tab, text="浏览", command=self.select_file_py)
        self.browse_btn.grid(row=1, column=2, padx=5, pady=3)

        ttk.Label(tab, text="Python 代码：").grid(row=2, column=0, padx=6, pady=6, sticky="nw")
        self.code_text = scrolledtext.ScrolledText(tab, width=85, height=10)
        self.code_text.grid(row=2, column=1, columnspan=2, padx=5, pady=3)
        self.code_text.grid_remove()

        ttk.Label(tab, text="全局 Gzip 压缩：").grid(row=3, column=0, padx=6, pady=8, sticky="w")
        self.gzip_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(tab, text="启用压缩", variable=self.gzip_var).grid(row=3, column=1, sticky="w")

        ttk.Label(tab, text="命令行格式：").grid(row=4, column=0, padx=6, pady=8, sticky="w")
        self.format_var = tk.StringVar(value="python_c")
        fmts = [("python -c 模式", "python_c"), ("管道模式", "pipe")]
        for i, (txt, v) in enumerate(fmts):
            ttk.Radiobutton(tab, text=txt, variable=self.format_var, value=v).grid(row=4, column=1+i, sticky="w")

        ttk.Label(tab, text="终端平台：").grid(row=5, column=0, padx=6, pady=8, sticky="w")
        self.term_var = tk.StringVar(value="universal")
        terms = [
            ("✅ 通用全平台", "universal"),
            ("Linux/macOS Bash", "bash"),
            ("Windows CMD", "cmd"),
            ("Windows PowerShell", "winps"),
            ("Linux PowerShell", "linps"),
            ("BusyBox(Docker/路由)", "busybox"),
        ]
        for i, (txt, v) in enumerate(terms):
            r = 6 + (i // 2)
            c = 1 + (i % 2)
            ttk.Radiobutton(tab, text=txt, variable=self.term_var, value=v).grid(row=r, column=c, sticky="w", padx=2, pady=1)

        ttk.Button(tab, text="🚀 生成命令", command=self.on_gen_py, width=40).grid(row=9, column=0, columnspan=3, pady=10)

        ttk.Label(tab, text="生成命令：").grid(row=10, column=0, columnspan=3, sticky="w", padx=5)
        self.out_py = scrolledtext.ScrolledText(tab, width=110, height=12)
        self.out_py.grid(row=11, column=0, columnspan=3, padx=5, pady=6)
        ttk.Button(tab, text="📋 复制完整命令", command=self.copy_full_command).grid(row=12, column=0, columnspan=3, pady=4)
    def switch_mode_py(self):
        mode = self.input_mode.get()
        if mode == "file":
            self.file_entry.grid()
            self.browse_btn.grid()
            self.code_text.grid_remove()
        else:
            self.file_entry.grid_remove()
            self.browse_btn.grid_remove()
            self.code_text.grid()

    def select_file_py(self):
        path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py"), ("所有文件", "*.*")])
        if path:
            self.file_var.set(path)

    def get_py_code(self):
        mode = self.input_mode.get()
        if mode == "file":
            path = self.file_var.get().strip()
            if not path:
                raise Exception("请选择 Py 文件")
            return self.core.read_file(path)
        else:
            code = self.code_text.get(1.0, tk.END).strip()
            if not code:
                raise Exception("请输入 Python 代码")
            return code

    def on_gen_py(self):
        self.out_py.delete(1.0, tk.END)
        try:
            code = self.get_py_code()
            b64 = self.core.encode_code(code, self.gzip_var.get())
            cmd = self.core.generate_python_cmd(
                b64, self.gzip_var.get(), self.format_var.get(), self.term_var.get()
            )
            self.full_py_cmd = cmd  # 保存完整命令
            show = cmd[:200] + "..." if len(cmd) > 200 else cmd
            self.out_py.insert(tk.END, show)
        except Exception as e:
            self.out_py.insert(tk.END, f"错误：{str(e)}")

    # ==================== ELF/EXE 标签页 ====================
    def build_binary_tab(self):
        tab = self.tab_bin

        ttk.Label(tab, text="ELF/EXE 二进制文件：").grid(row=0, column=0, padx=6, pady=10, sticky="w")
        self.bin_path_var = tk.StringVar(value="")
        ttk.Entry(tab, textvariable=self.bin_path_var, width=70).grid(row=0, column=1, padx=5)
        ttk.Button(tab, text="浏览选择", command=self.select_bin_file).grid(row=0, column=2, padx=5)

        ttk.Label(tab, text="文件类型：").grid(row=1, column=0, padx=6, pady=8, sticky="w")
        self.bin_type_var = tk.StringVar(value="elf")
        ttk.Radiobutton(tab, text="Linux ELF", variable=self.bin_type_var, value="elf").grid(row=1, column=1, sticky="w")
        ttk.Radiobutton(tab, text="Windows EXE", variable=self.bin_type_var, value="exe").grid(row=1, column=2, sticky="w")

        ttk.Label(tab, text="Gzip 压缩：").grid(row=2, column=0, padx=6, pady=8, sticky="w")
        self.bin_gzip_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(tab, text="启用压缩（缩短长度）", variable=self.bin_gzip_var).grid(row=2, column=1, sticky="w")

        ttk.Button(tab, text="🚀 生成 Bash 命令", command=self.on_gen_bin, width=40).grid(row=3, column=0, columnspan=3, pady=15)

        ttk.Label(tab, text="生成命令（直接复制到 Linux 运行）：").grid(row=4, column=0, columnspan=3, sticky="w", padx=5)
        self.out_bin = scrolledtext.ScrolledText(tab, width=110, height=18)
        self.out_bin.grid(row=5, column=0, columnspan=3, padx=5, pady=6)
        ttk.Button(tab, text="📋 复制完整命令", command=self.copy_full_command).grid(row=6, column=0, columnspan=3, pady=4)
    def select_bin_file(self):
        path = filedialog.askopenfilename(filetypes=[
            ("可执行文件", "*.elf *.exe"),
            ("所有文件", "*.*")
        ])
        if path:
            self.bin_path_var.set(path)

    def on_gen_bin(self):
        self.out_bin.delete(1.0, tk.END)
        path = self.bin_path_var.get().strip()
        if not path:
            self.out_bin.insert(tk.END, "请选择 ELF / EXE 文件")
            return
        try:
            bin_data = self.core.read_bin_file(path)
            b64 = self.core.encode_bin_data(bin_data, self.bin_gzip_var.get())
            payload = self.core.generate_bin_bash_payload(
                b64_str=b64,
                use_gzip=self.bin_gzip_var.get(),
                bin_type=self.bin_type_var.get()
            )
            self.full_bin_cmd = payload  # 保存完整命令
            show = payload[:200] + "..." if len(payload) > 200 else payload
            self.out_bin.insert(tk.END, show)
        except Exception as e:
            self.out_bin.insert(tk.END, f"错误：{str(e)}")

    def copy_full_command(self):
        # 判断当前在哪个标签页
        current_tab = self.notebook.index(self.notebook.select())
        if current_tab == 0:
            to_copy = self.full_py_cmd
        else:
            to_copy = self.full_bin_cmd

        if to_copy:
            self.root.clipboard_clear()
            self.root.clipboard_append(to_copy)
            self.root.update()
if __name__ == "__main__":
    root = tk.Tk()
    All2OneLineGUI(root)
    root.mainloop()