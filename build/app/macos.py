import os.path
import subprocess

from app.build import Builder
from app.cmd import create_dir_if_not_exists, delete_dir_if_exists

class MacosBuilder(Builder):
    def __init__(self, build_dir: str):
        super().__init__(build_dir)
        self.framework_dir = os.path.join(self.lib_dir, "macos_dylib")
        delete_dir_if_exists(self.framework_dir)
        create_dir_if_not_exists(self.framework_dir)
        create_dir_if_not_exists(self.framework_dir+"/arm64")
        create_dir_if_not_exists(self.framework_dir+"/amd64")
        self.lib_file = "libXray.dylib"
        self.lib_header_file = "libXray.h"

    def before_build(self):
        super().before_build()
        self.prepare_static_lib()

    def build(self):
        self.before_build()
        self.build_macos("arm64")
        self.build_macos("amd64")
        self.after_build()

    def build_macos(self, arch):
        output_dir = os.path.join(self.framework_dir, arch)
        create_dir_if_not_exists(output_dir)
        output_file = os.path.join(output_dir, self.lib_file)
        run_env = os.environ.copy()
        run_env["GOOS"] = "darwin"
        run_env["GOARCH"] = arch
        run_env["CC"] = "gcc"
        run_env["CXX"] = "g++"
        run_env["CGO_ENABLED"] = "1"

        cmd = [
            "go",
            "build",
            "-ldflags=-w",
            f"-o={output_file}",
            "-buildmode=c-shared",
        ]
        os.chdir(self.lib_dir)
        print(run_env)
        print(cmd)
        ret = subprocess.run(cmd, env=run_env)
        if ret.returncode != 0:
            raise Exception(f"build_linux failed")

    def after_build(self):
        super().after_build()
        self.reset_files()
