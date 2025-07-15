#!/usr/bin/env python3
import threading
import subprocess
import sys
import os

Compiler: str = "clang++"
StripUtil: str = "llvm-strip-20"
LinkFlags: str = "-lSDL2 -lSDL2_image -lSDL2_mixer -lSDL2_ttf"
Source: str = "src/main.cpp"

test_build: bool = False
debug_build: bool = False
release_build: bool = False
prod_build: bool = False
test_run: bool = False

def createdeps():
    os.makedirs("bin/test", exist_ok=True)
    os.makedirs("bin/debug", exist_ok=True)
    os.makedirs("bin/release", exist_ok=True)
    os.makedirs("bin/prod", exist_ok=True)

def maketest():
    print("Building test")
    if subprocess.run(Compiler+" "+Source+" -o bin/test/main -O0 -g0 -Wall "+LinkFlags, shell=True).returncode == 0:
        subprocess.run(StripUtil+" --strip-all bin/test/main", shell=True)

def makedebug():
    print("Building debug")
    if subprocess.run(Compiler+" "+Source+" -o bin/debug/main -O0 -g3 -Wall "+LinkFlags, shell=True).returncode == 0:
        subprocess.run(StripUtil+" --strip-unneeded bin/debug/main", shell=True)

def makerelease():
    print("Building release")
    if subprocess.run(Compiler+" "+Source+" -o bin/release/main -O2 -g0 -flto=thin -Wall "+LinkFlags, shell=True).returncode == 0:
        subprocess.run(StripUtil+" --strip-all bin/release/main", shell=True)

def makeprod():
    print("Building production")
    if subprocess.run(Compiler+" "+Source+" -o bin/prod/main -O3 -g0 -flto=full -Wall "+LinkFlags, shell=True).returncode == 0:
        subprocess.run(StripUtil+" --strip-all bin/prod/main", shell=True)

if __name__ == "__main__":
    createdeps()
    if len(sys.argv) < 2:
        print("No build flag, building debug only")
        makedebug()
    else:
        if "test" in sys.argv:
            test_build = True
        if "debug" in sys.argv:
            debug_build = True
        if "release" in sys.argv:
            release_build = True
        if "prod" in sys.argv:
            prod_build = True
        if "all" in sys.argv:
            test_build = True
            debug_build = True
            release_build = True
            prod_build = True
        if "run" in sys.argv:
            test_build = True
            test_run = True
    
    TestThread = ""
    DebugThread = ""
    ReleaseThread = ""
    ProdThread = ""
    if prod_build:
        ProdThread = threading.Thread(target=makeprod)
        ProdThread.start()
    if release_build:
        ReleaseThread = threading.Thread(target=makerelease)
        ReleaseThread.start()
    if debug_build:
        DebugThread = threading.Thread(target=makedebug)
        DebugThread.start()
    if test_build:
        TestThread = threading.Thread(target=maketest)
        TestThread.start()
    if test_run:
        TestThread.join()
        print("Running test...\n\n")
        if subprocess.run("./bin/test/main",shell=True).returncode == 0:
            print("\n\nTest success")
        else:
            print("\n\nTest failed")
    if debug_build:
        DebugThread.join()
    if release_build:
        ReleaseThread.join()
    if prod_build:
        ProdThread.join()