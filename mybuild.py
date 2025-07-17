#!/usr/bin/env python3
import subprocess
import threading
import hashlib
import shutil
import sys
import os

Compiler: str = "clang++"
StripUtil: str = "llvm-strip-20"
LinkFlags: str = "-lSDL2 -lSDL2_image -lSDL2_mixer -lSDL2_ttf"
AllCFlags: str = "-Wall"
TestCFlags: str = "-O0 -g0 -DTEST -DNDEBUG"
DebugCFlags: str = "-Og -g3 -DDEBUG"
ReleaseCFlags: str = "-O2 -g0 -flto=thin -DRELEASE -DNDEBUG"
ProdCFlags: str = "-O3 -g0 -flto=full -DPRODUCTION -DNDEBUG"
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

new_test_hashes: list[str] = []
new_debug_hashes: list[str] = []
new_release_hashes: list[str] = []
new_prod_hashes: list[str] = []

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

def get_cpp_dependencies(src: str, build_mode: str):
    include_list: list[str] = ""
    if build_mode == "test":
        result = subprocess.run(Compiler+" -M "+TestCFlags+" "+src, shell=True, capture_output=True)
    if build_mode == "debug":
        result = subprocess.run(Compiler+" -M "+DebugCFlags+" "+src, shell=True, capture_output=True)
    if build_mode == "release":
        result = subprocess.run(Compiler+" -M "+ReleaseCFlags+" "+src, shell=True, capture_output=True)
    if build_mode == "prod":
        result = subprocess.run(Compiler+" -M "+ProdCFlags+" "+src, shell=True, capture_output=True)
    if result.returncode == 0:
        include_list = str(result.stdout, "utf-8").lstrip(get_obj_filename(src)+":").splitlines()
        for item in range(len(include_list)):
            include_list[item] = include_list[item].lstrip(" ").rstrip("\\ ")
            if len(include_list[item].split()) > 1:
                print(include_list[item].split())
        #return include_list
    return ["Failed"]

def get_obj_hash(src: str):
    with open(src, "rb") as input_file:
        input_filedata = input_file.read()
    return hashlib.md5(input_filedata).hexdigest()

def CompilationThread():
    global PendingSources, new_test_hashes, new_debug_hashes, new_release_hashes, new_prod_hashes
    while len(PendingSources) > 0:
        build_type, my_src = PendingSources.pop()
        my_obj: str = get_obj_filename(my_src)
        input_src = my_src + " " + get_obj_hash(my_src) + "\n"
        need_to_compile: bool = False
        all_dependencies: list[str] = []
        all_headers: list[str] = get_cpp_dependencies(my_src, build_type)
        if all_headers != ["Failed"]:
            for item in all_headers:
                all_dependencies += [item + " " + get_obj_hash(item) + "\n"]
            all_dependencies += [input_src]
        else:
            all_dependencies = [input_src]
        all_headers.clear()

        for src in all_dependencies:
            if build_type == "test":
                if src not in test_hashes:
                    need_to_compile = True
            if build_type == "debug":
                if src not in debug_hashes:
                    need_to_compile = True
            if build_type == "release":
                if src not in release_hashes:
                    need_to_compile = True
            if build_type == "prod":
                if src not in prod_hashes:
                    need_to_compile = True

        if need_to_compile:
            if build_type == "test":
                command: str = Compiler + " -c "+ my_src +" -o "+ TestBin +"/"+ my_obj + " "+ TestCFlags +" "+ AllCFlags
            if build_type == "debug":
                command: str = Compiler + " -c "+ my_src +" -o "+ DebugBin +"/"+ my_obj + " "+ DebugCFlags +" "+ AllCFlags
            if build_type == "release":
                command: str = Compiler + " -c "+ my_src +" -o "+ ReleaseBin +"/"+ my_obj + " "+ ReleaseCFlags +" "+ AllCFlags
            if build_type == "prod":
                command: str = Compiler + " -c "+ my_src +" -o "+ ProdBin +"/"+ my_obj + " "+ ProdCFlags +" "+ AllCFlags
            print(" Compiling ("+build_type.center(7, " ")+"): "+my_src.removeprefix("src/"))
            result = subprocess.run(command, shell=True).returncode
            if result == 0:
                if build_type == "test":
                    new_test_hashes += all_dependencies
                if build_type == "debug":
                    new_debug_hashes += all_dependencies
                if build_type == "release":
                    new_release_hashes += all_dependencies
                if build_type == "prod":
                    new_prod_hashes += all_dependencies
            else:
                PendingSources.clear()
                new_test_hashes.clear()
                new_debug_hashes.clear()
                new_release_hashes.clear()
                new_prod_hashes.clear()
                return
        else:
            print(" Skipping  ("+build_type.center(7, " ")+"): "+my_src.removeprefix("src/"))
            if build_type == "test":
                new_test_hashes += all_dependencies
            if build_type == "debug":
                new_debug_hashes += all_dependencies
            if build_type == "release":
                new_release_hashes += all_dependencies
            if build_type == "prod":
                new_prod_hashes += all_dependencies

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

    os.makedirs(".mybuild/", exist_ok=True)
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
    for item in Sources:
        if test_build:
            PendingSources += [("test", item)]
        if debug_build:
            PendingSources += [("debug", item)]
        if release_build:
            PendingSources += [("release", item)]
        if prod_build:
            PendingSources += [("prod", item)]
    thread_count = os.cpu_count()
    if thread_count == None:
        CompilationThread()
    elif thread_count > len(PendingSources):
        thread_count = len(PendingSources)
    
    if thread_count != None:
        print("Using "+str(thread_count)+" threads")
        AllThreads: list[threading.Thread] = []
        for thread_number in range(thread_count):
            AllThreads += [threading.Thread(target=CompilationThread)]
        for thread_number in range(thread_count):
            AllThreads[thread_number].start()
        for thread_number in range(thread_count):
            AllThreads[thread_number].join()

    #TODO LINK

    if test_build:
        with open(".mybuild/testhashes.db", "w") as testhfd:
            testhfd.writelines(new_test_hashes)
    if debug_build:
        with open(".mybuild/debughashes.db", "w") as debughfd:
            debughfd.writelines(new_debug_hashes)
    if release_build:
        with open(".mybuild/releasehashes.db", "w") as releasehfd:
            releasehfd.writelines(new_release_hashes)
    if prod_build:
        with open(".mybuild/prodhashes.db", "w") as prodhfd:
            prodhfd.writelines(new_prod_hashes)

    if test_run:
        returncode: int = subprocess.run("./bin/test/main",shell=True).returncode
        if returncode == 0:
            print("Test success!")
        else:
            print("Test fail, returncode: "+str(returncode))

    if clean:
        shutil.rmtree("bin", ignore_errors=True)
        shutil.rmtree(".mybuild", ignore_errors=True)
    
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