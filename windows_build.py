#!/usr/bin/env python3
import threading
import subprocess
import sys
import os
import shutil

# === Configuration ===
Compiler = "clang++"
StripUtil = "llvm-strip"  # Set to empty string if not installed
SDL2_INCLUDE = "libs/sdl2/include"
SDL2_LIB = "libs/sdl2/lib"
SDL2_DLL = os.path.join("libs/sdl2/bin", "SDL2.dll")
LinkFlags = f"-I{SDL2_INCLUDE} -L{SDL2_LIB} -lSDL2main -lSDL2 -Xlinker /subsystem:windows -lShell32"
# Optional flags — tune as needed
ExtraFlags = "-MD"

# Gather all .cpp files
SourceFiles = " ".join([
    os.path.join("src", file)
    for file in os.listdir("src")
    if file.endswith(".cpp")
])

OutputName = 'main.exe'

# === Build Flags ===
test_build = debug_build = release_build = prod_build = test_run = False

# === Create output folders ===
def createdeps():
    os.makedirs("bin/test", exist_ok=True)
    os.makedirs("bin/debug", exist_ok=True)
    os.makedirs("bin/release", exist_ok=True)
    os.makedirs("bin/prod", exist_ok=True)

# === Strip helper ===
def run_strip(path, strip_type):
    if StripUtil:
        try:
            subprocess.run(f"{StripUtil} {strip_type} {path}", shell=True, check=True)
        except subprocess.CalledProcessError:
            print(f"⚠️  Warning: Failed to strip {path}")

# === Copy SDL2.dll ===
def copy_dll(destination_folder):
    if os.path.exists(SDL2_DLL):
        shutil.copy(SDL2_DLL, os.path.join(destination_folder, "SDL2.dll"))

# === Build Types ===
def compile_variant(name, opt_flags, strip_type):
    print(f"📦 Building {name}")
    out = f"bin/{name}/{OutputName}"
    cmd = f'{Compiler} {SourceFiles} -o "{out}" {LinkFlags} {opt_flags} {ExtraFlags}'
    print(f"🔧 Compiling with: {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode == 0:
        run_strip(out, strip_type)
        copy_dll(f"bin/{name}")
    else:
        print(f"❌ {name} build failed.")

def maketest():   compile_variant("test",    "-O0 -g0", "--strip-all")
def makedebug():  compile_variant("debug",   "-O0 -g3", "--strip-unneeded")
def makerelease():compile_variant("release", "-O2 -g0 -flto=thin", "--strip-all")
def makeprod():   compile_variant("prod",    "-O3 -g0 -flto=full", "--strip-all")

# === Main ===
if __name__ == "__main__":
    createdeps()

    if len(sys.argv) < 2:
        print("No build flag, defaulting to debug")
        debug_build = True
    else:
        args = sys.argv[1:]
        test_build = "test" in args
        debug_build = "debug" in args
        release_build = "release" in args
        prod_build = "prod" in args
        test_run = "run" in args
        if "all" in args:
            test_build = debug_build = release_build = prod_build = True

    # Threads
    threads = {}

    if test_build:
        threads["test"] = threading.Thread(target=maketest)
        threads["test"].start()
    if debug_build:
        threads["debug"] = threading.Thread(target=makedebug)
        threads["debug"].start()
    if release_build:
        threads["release"] = threading.Thread(target=makerelease)
        threads["release"].start()
    if prod_build:
        threads["prod"] = threading.Thread(target=makeprod)
        threads["prod"].start()

    if test_run:
        try:
            threads["test"].join()
            print("\n🏃 Running test build...\n")
            result = subprocess.run("bin/test/" + OutputName, shell=True)
            if result.returncode == 0:
                print("\n✅ Test success")
            else:
                print("\n❌ Test failed")
        except Exception as e:
            print(f"Error: {e}")

    for name, thread in threads.items():
        if not (test_run and name == "test"):  # Already joined above
            thread.join()
