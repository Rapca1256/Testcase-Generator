import subprocess
import tempfile
import sys
import os

class Output:
    def __init__(self, source, input_filepath, output_filepath, timeout=5):
        self.source = source
        self.input_filepath = input_filepath
        self.output_filepath = output_filepath
        self.timeout = timeout

        self.solve() # 出力を生成

    def solve(self):
        lang = self.detect_language(self.source)

        with tempfile.TemporaryDirectory() as workdir:
            if lang == "python":
                cmd = [sys.executable, self.source]

            elif lang == "cpp":
                exe = os.path.join(workdir, "a.out")
                compile_cmd = ["g++", self.source, "-O2", "-std=c++17", "-o", exe]
                self.run(compile_cmd)
                cmd = [exe]

            elif lang == "java":
                class_name = os.path.splitext(os.path.basename(self.source))[0]
                compile_cmd = ["javac", "-d", workdir, self.source]
                self.run(compile_cmd)
                cmd = ["java", "-cp", workdir, class_name]

            self.run(cmd)

    def run(self, cmd):
        with open(self.input_filepath) as f_in, open(self.output_filepath, "w") as f_out:
            try:
                subprocess.run(
                    cmd,
                    stdin=f_in,
                    stdout=f_out,
                    stderr=subprocess.PIPE,
                    text=True,
                    timeout=self.timeout,
                    check=True
                )
            except subprocess.TimeoutExpired:
                raise RuntimeError("実行がタイムアウトしました")
            except subprocess.CalledProcessError as e:
                raise RuntimeError(e.stderr)
    
    def detect_language(self, path):
        ext = os.path.splitext(path)[1].lower()
        if ext == ".py":
            return "python"
        if ext == ".cpp":
            return "cpp"
        if ext == ".java":
            return "java"
        raise ValueError("未対応の言語です")
