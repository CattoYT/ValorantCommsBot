import subprocess
import sys
import os
import time
exe = sys.executable
print("Compiling Rust Modules...")
subprocess.run([exe, "-m", "maturin", "develop", "-r"], check=True)
print("Compiled Rust Modules! Restarting...")
time.sleep(2)
os.execv(exe, [exe] + sys.argv)