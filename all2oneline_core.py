# all2oneline_core.py
import base64
import gzip

class All2OneLineCore:
    # ==================== Python 脚本处理 ====================
    @staticmethod
    def read_file(filepath: str, encoding="utf-8") -> str:
        with open(filepath, "r", encoding=encoding) as f:
            return f.read()

    @staticmethod
    def encode_code(code: str, use_gzip: bool = False) -> str:
        data = code.encode("utf-8")
        if use_gzip:
            data = gzip.compress(data)
        return base64.b64encode(data).decode("ascii")

    @staticmethod
    def generate_python_cmd(
        b64_str: str,
        use_gzip: bool = False,
        cmd_format: str = "python_c",
        term_type: str = "universal"
    ) -> str:
        cmd = ""
        if cmd_format == "python_c":
            if not use_gzip:
                core = "import base64; exec(base64.b64decode({}).decode())"
            else:
                core = "import base64,gzip; exec(gzip.decompress(base64.b64decode({})).decode())"

            if term_type in ("universal", "cmd", "busybox"):
                payload = core.format(f"'{b64_str}'")
                cmd = f'python -c "{payload}"'
            elif term_type == "bash":
                payload = core.format(f"'{b64_str}'")
                cmd = f'python -c "{payload}"'
            elif term_type in ("winps", "linps"):
                payload = core.format(f'"{b64_str}"')
                cmd = f"python -c '{payload}'"

        elif cmd_format == "pipe":
            py = "python3" if term_type != "busybox" else "python"
            if term_type in ("universal", "bash", "linps", "busybox"):
                cmd = f'echo "{b64_str}" | base64 -d'
            elif term_type == "cmd":
                cmd = f'echo {b64_str} | base64 -d'
            elif term_type == "winps":
                cmd = f'Write-Output "{b64_str}" | base64 -d'

            if use_gzip:
                cmd += " | gzip -d"
            cmd += f" | {py}"
        return cmd

    # ==================== 二进制 ELF / EXE 处理 ====================
    @staticmethod
    def read_bin_file(filepath: str) -> bytes:
        with open(filepath, "rb") as f:
            return f.read()

    @staticmethod
    def encode_bin_data(data: bytes, use_gzip: bool = False) -> str:
        if use_gzip:
            data = gzip.compress(data)
        return base64.b64encode(data).decode("ascii")

    @staticmethod
    def generate_bin_bash_payload(
        b64_str: str,
        use_gzip: bool = False,
        bin_type: str = "elf"
    ) -> str:
        quote = "'"
        echo_cmd = f'echo {quote}{b64_str}{quote}'
        decode_chain = "base64 -d"
        if use_gzip:
            decode_chain += " | gzip -d"

        tmp_path = "/tmp/bin_payload"

        if bin_type == "elf":
            return (
                f"{echo_cmd} | {decode_chain} > {tmp_path} && "
                f"chmod +x {tmp_path} && "
                f"{tmp_path} && "
                f"rm -f {tmp_path}"
            )
        else:
            return (
                f"{echo_cmd} | {decode_chain} > {tmp_path} && "
                f"wine {tmp_path} && "
                f"rm -f {tmp_path}"
            )