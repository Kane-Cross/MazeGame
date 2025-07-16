#!/usr/bin/env python3
import subprocess
import threading
import hashlib
import sys
import os

Compiler: str = "clang++"
StripUtil: str = "llvm-strip-20"
LinkFlags: str = "-lSDL2 -lSDL2_image -lSDL2_mixer -lSDL2_ttf"
TestBin: str = "bin/test"
DebugBin: str = "bin/debug"
ReleaseBin: str = "bin/release"
ProdBin: str = "bin/prod"
Sources: list[str] = []

PendingSources: list[str] = []
test_hashes: list[str] = []
debug_hashes: list[str] = []
release_hashes: list[str] = []
prod_hashes: list[str] = []

verbose_logging: bool = False
def log(message: str):
    if verbose_logging:
        print(message)

test_build: bool = False
debug_build: bool = False
release_build: bool = False
prod_build: bool = False
test_run: bool = False
clean: bool = False

def get_obj_filename(src: str):
    if src.endswith(".cpp"):
        if "/" in src:
            src = src[src.rfind("/")+1:].removesuffix(".cpp") + ".o"
    return src

def CompilationThread():
    global PendingSources
    while len(PendingSources) > 0:
        my_src: str = PendingSources.pop()
        my_obj: str = get_obj_filename(my_src)
        if test_build:
            if my_src in test_hashes:
                pass
        if debug_build:
            pass
        if prod_build:
            pass
        if test_build:
            pass

def get_all_srcs():
    global Sources
    for dir, dirs, files in os.walk("src"):
        for file in files:
            if file.endswith(".cpp"):
                Sources += [dir+"/"+file]

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("No build flag, usage:")
        print(" ./mybuild.py [build flag]\n")
        print("  valid build flags:")
        print("   test      - no optimization quick build")
        print("   debug     - no optimization, debug-info-laden build (very large binaries)")
        print("   release   - light optimization 'preview' build (for stress testing)")
        print("   prod      - fully optimized production build")
        print("   all       - alias for all of the above")
        print("   run       - build test and run it")
        print("   clean     - deletes the bin directory (after all other targets)")
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
        if "clean" in sys.argv:
            clean = True

    os.makedirs(".mybuild/")
    if test_build:
        os.makedirs("bin/test", exist_ok=True)
        try:
            with open(".mybuild/testhashes.db", "r") as testhfd:
                test_hashes = testhfd.readlines()
        except:
            pass
    if debug_build:
        os.makedirs("bin/debug", exist_ok=True)
        try:
            with open(".mybuild/debughashes.db", "r") as debughfd:
                debug_hashes = debughfd.readlines()
        except:
            pass
    if release_build:
        os.makedirs("bin/release", exist_ok=True)
        try:
            with open(".mybuild/releasehashes.db", "r") as releasehfd:
                release_hashes = releasehfd.readlines()
        except:
            pass
    if prod_build:
        os.makedirs("bin/prod", exist_ok=True)
        try:
            with open(".mybuild/prodhashes.db", "r") as prodhfd:
                prod_hashes = prodhfd.readlines()
        except:
            pass

    get_all_srcs()
    PendingSources = Sources
    print(PendingSources)
    CompilationThread()

    #TODO COMPILE

    #TODO LINK

    if test_run:
        returncode: int = subprocess.run("./bin/test/main",shell=True).returncode
        if returncode == 0:
            print("Test success!")
        else:
            print("Test fail, returncode: "+str(returncode))

    if clean:
        os.removedirs("bin")
        os.removedirs(".mybuild")
    
"""
def maketest():
    print("Building test")
    
    print("Linking test")
    if subprocess.run(Compiler+" "+Source+" -o bin/test/main -O0 -g0 -Wall -DNDEBUG -DBUILD_TEST "+LinkFlags, shell=True).returncode == 0:
        subprocess.run(StripUtil+" --strip-all bin/test/main", shell=True)

def makedebug():
    print("Building debug")
    if subprocess.run(Compiler+" "+Source+" -o bin/debug/main -O0 -g3 -Wall -DDEBUG -DBUILD_DEBUG "+LinkFlags, shell=True).returncode == 0:
        subprocess.run(StripUtil+" --strip-unneeded bin/debug/main", shell=True)

def makerelease():
    print("Building release")
    if subprocess.run(Compiler+" "+Source+" -o bin/release/main -O2 -g0 -flto=thin -Wall -DNDEBUG -DBUILD_RELEASE "+LinkFlags, shell=True).returncode == 0:
        subprocess.run(StripUtil+" --strip-all bin/release/main", shell=True)

def makeprod():
    print("Building production")
    if subprocess.run(Compiler+" "+Source+" -o bin/prod/main -O3 -g0 -flto=full -Wall -DNDEBUG -DBUILD_PRODUCTION "+LinkFlags, shell=True).returncode == 0:
        subprocess.run(StripUtil+" --strip-all bin/prod/main", shell=True)
"""