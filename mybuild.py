#!/usr/bin/env python3
import subprocess
import threading
import hashlib
import shutil
import time
import sys
import os

Compiler: str = "clang++"
StripUtil: str = "llvm-strip-20"
LinkFlags: str = "-lglfw -lGL -lX11 -lpthread -lXrandr -lXi -ldl"
AllCFlags: str = ""
TestCFlags: str = "-O0 -g0 -DTEST -DNDEBUG"
DebugCFlags: str = "-Og -g3 -DDEBUG"
ReleaseCFlags: str = "-O2 -g0 -flto=thin -DRELEASE -DNDEBUG -Wall"
ProdCFlags: str = "-O3 -g0 -flto=full -DPRODUCTION -DNDEBUG -Wall"
TestStripFlag: str = "--strip-debug"
DebugStripFlag: str = "--strip-unneeded"
ReleaseStripFlag: str = "--strip-unneeded"
ProdStripFlag: str = "--strip-all"
TestObjBin: str = ".mybuild/bin/test/"
DebugObjBin: str = ".mybuild/bin/debug/"
ReleaseObjBin: str = ".mybuild/bin/release/"
ProdObjBin: str = ".mybuild/bin/prod/"
TestBin: str = "bin/test/"
DebugBin: str = "bin/debug/"
ReleaseBin: str = "bin/release/"
ProdBin: str = "bin/prod/"
ExecutableName: str = "MazeGame"
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

build_fail_test: bool = False
build_fail_debug: bool = False
build_fail_release: bool = False
build_fail_prod: bool = False

verbose_logging: bool = False
silent_mode: bool = False
force_build: bool = False
def log(message: str):
    if verbose_logging and not silent_mode:
        print(message)
def plog(message: str):
    if not silent_mode:
        print(message)

test_build: bool = False
debug_build: bool = False
release_build: bool = False
prod_build: bool = False
test_run: bool = False
clean: bool = False

def get_file_dependencies():
    pass

def get_obj_filename(src: str):
    if src.endswith(".cpp"):
        if "/" in src:
            src = src[src.rfind("/")+1:].removesuffix(".cpp") + ".o"
    return src

def get_all_srcs():
    global Sources
    for dir, dirs, files in os.walk("src"):
        for file in files:
            if file.endswith(".cpp"):
                Sources += [dir+"/"+file]

def get_all_hdrs():
    headers: list[str] = []
    for dir, dirs, files in os.walk("src"):
        for file in files:
            if file.endswith(".hpp"):
                headers += [dir+"/"+file]
    return headers

def get_cpp_dependencies(src: str, build_mode: str):
    include_list: list[str] = []
    header_dependencies: list[str] = []
    if build_mode == "test":
        result = subprocess.run(Compiler+" -M "+TestCFlags+" "+src, shell=True, capture_output=True)
    if build_mode == "debug":
        result = subprocess.run(Compiler+" -M "+DebugCFlags+" "+src, shell=True, capture_output=True)
    if build_mode == "release":
        result = subprocess.run(Compiler+" -M "+ReleaseCFlags+" "+src, shell=True, capture_output=True)
    if build_mode == "prod":
        result = subprocess.run(Compiler+" -M "+ProdCFlags+" "+src, shell=True, capture_output=True)
    if result.returncode == 0:
        headers = get_all_hdrs()
        include_list = str(result.stdout, "utf-8").lstrip(get_obj_filename(src)+":").replace("\\", "").splitlines()
        for item in include_list:
            for header in headers:
                if header in item:
                    header_dependencies += [header]
        return header_dependencies
    return ["Failed"]

def get_obj_hash(src: str):
    with open(src, "rb") as input_file:
        input_filedata = input_file.read()
    return hashlib.md5(input_filedata).hexdigest()

def HashCheckThread():
    global Sources, PendingSources, new_test_hashes, new_debug_hashes, new_release_hashes, new_prod_hashes
    while len(Sources) > 0:
        my_src: str = Sources.pop()
        if my_src not in PendingSources:
            input_src = my_src + " " + get_obj_hash(my_src) + "\n"
            need_to_compile: bool = force_build

            if test_build:
                all_dependencies: list[str] = []
                all_headers: list[str] = get_cpp_dependencies(my_src, "test")
                if all_headers != ["Failed"]:
                    for item in all_headers:
                        all_dependencies += [item + " " + get_obj_hash(item) + "\n"]
                    all_dependencies += [input_src]
                else:
                    all_dependencies = [input_src]
                all_headers.clear()

                for src in all_dependencies:
                    if src not in test_hashes:
                        need_to_compile = True

            if debug_build:
                all_dependencies: list[str] = []
                all_headers: list[str] = get_cpp_dependencies(my_src, "debug")
                if all_headers != ["Failed"]:
                    for item in all_headers:
                        all_dependencies += [item + " " + get_obj_hash(item) + "\n"]
                    all_dependencies += [input_src]
                else:
                    all_dependencies = [input_src]
                all_headers.clear()

                for src in all_dependencies:
                    if src not in debug_hashes:
                        need_to_compile = True

            if release_build:
                all_dependencies: list[str] = []
                all_headers: list[str] = get_cpp_dependencies(my_src, "release")
                if all_headers != ["Failed"]:
                    for item in all_headers:
                        all_dependencies += [item + " " + get_obj_hash(item) + "\n"]
                    all_dependencies += [input_src]
                else:
                    all_dependencies = [input_src]
                all_headers.clear()

                for src in all_dependencies:
                    if src not in release_hashes:
                        need_to_compile = True

            if prod_build:
                all_dependencies: list[str] = []
                all_headers: list[str] = get_cpp_dependencies(my_src, "prod")
                if all_headers != ["Failed"]:
                    for item in all_headers:
                        all_dependencies += [item + " " + get_obj_hash(item) + "\n"]
                    all_dependencies += [input_src]
                else:
                    all_dependencies = [input_src]
                all_headers.clear()

                for src in all_dependencies:
                    if src not in prod_hashes:
                        need_to_compile = True

            if test_build:
                if need_to_compile:
                    PendingSources += [("test", my_src)]
                for item in all_dependencies:
                    if item not in new_test_hashes:
                        new_test_hashes += item
            if debug_build:
                if need_to_compile:
                    PendingSources += [("debug", my_src)]
                for item in all_dependencies:
                    if item not in new_debug_hashes:
                        new_debug_hashes += item
            if release_build:
                if need_to_compile:
                    PendingSources += [("release", my_src)]
                for item in all_dependencies:
                    if item not in new_release_hashes:
                        new_release_hashes += item
            if prod_build:
                if need_to_compile:
                    PendingSources += [("prod", my_src)]
                for item in all_dependencies:
                    if item not in new_prod_hashes:
                        new_prod_hashes += item

def CompilationThread():
    global PendingSources, new_test_hashes, new_debug_hashes, new_release_hashes, new_prod_hashes, build_fail_test, build_fail_debug, build_fail_release, build_fail_prod
    while len(PendingSources) > 0:
        build_type, my_src = PendingSources.pop()
        my_obj: str = get_obj_filename(my_src)
        if build_type == "test":
            command: str = Compiler + " -c "+ my_src +" -o "+ TestObjBin +"/"+ my_obj + " "+ TestCFlags +" "+ AllCFlags
        if build_type == "debug":
            command: str = Compiler + " -c "+ my_src +" -o "+ DebugObjBin +"/"+ my_obj + " "+ DebugCFlags +" "+ AllCFlags
        if build_type == "release":
            command: str = Compiler + " -c "+ my_src +" -o "+ ReleaseObjBin +"/"+ my_obj + " "+ ReleaseCFlags +" "+ AllCFlags
        if build_type == "prod":
            command: str = Compiler + " -c "+ my_src +" -o "+ ProdObjBin +"/"+ my_obj + " "+ ProdCFlags +" "+ AllCFlags
        plog(" Compiling ("+build_type.center(7, " ")+"): "+my_src.removeprefix("src/"))
        result = subprocess.run(command, shell=True).returncode
        if result != 0:
            if build_type == "test":
                build_fail_test = True
                PendingSources.clear()
            if build_type == "debug":
                build_fail_debug = True
                PendingSources.clear()
            if build_type == "release":
                build_fail_release = True
                PendingSources.clear()
            if build_type == "prod":
                build_fail_prod = True
                PendingSources.clear()

def LinkThread():
    global PendingSources, build_fail_test, build_fail_debug, build_fail_release, build_fail_prod
    while len(PendingSources) > 0:
        build_type: str = PendingSources.pop()[0]
        get_all_srcs()
        expected_srcs: list[str] = Sources
        expected_objs: list[str] = []
        my_srcs: str = ""
        for item in range(len(expected_srcs)):
            if get_obj_filename(expected_srcs[item]) not in expected_objs:
                expected_objs += [get_obj_filename(expected_srcs[item])]
        actual_objs: list[str] = []
        if build_type == "test":
            actual_objs = os.listdir(TestObjBin)
        if build_type == "debug":
            actual_objs = os.listdir(DebugObjBin)
        if build_type == "release":
            actual_objs = os.listdir(ReleaseObjBin)
        if build_type == "prod":
            actual_objs = os.listdir(ProdObjBin)
        for item in expected_objs:
            if item not in actual_objs:
                if build_type == "test":
                    build_fail_test = True
                    return
                if build_type == "debug":
                    build_fail_debug = True
                    return
                if build_type == "release":
                    build_fail_release = True
                    return
                if build_type == "prod":
                    build_fail_prod = True
                    return
            else:
                if build_type == "test" and (TestObjBin + item + " ") not in my_srcs:
                    my_srcs += TestObjBin + item + " "
                if build_type == "debug" and (DebugObjBin + item + " ") not in my_srcs:
                    my_srcs += DebugObjBin + item + " "
                if build_type == "release" and (ReleaseObjBin + item + " ") not in my_srcs:
                    my_srcs += ReleaseObjBin + item + " "
                if build_type == "prod" and (ProdObjBin + item + " ") not in my_srcs:
                    my_srcs += ProdObjBin + item + " "

        my_srcs = my_srcs.rstrip(" ")
        if build_type == "test":
            command: str = Compiler + " "+ my_srcs +" -o "+ TestBin + ExecutableName + " "+ TestCFlags +" "+ AllCFlags + " " + LinkFlags
        if build_type == "debug":
            command: str = Compiler + " "+ my_srcs +" -o "+ DebugBin + ExecutableName + " "+ DebugCFlags +" "+ AllCFlags + " " + LinkFlags
        if build_type == "release":
            command: str = Compiler + " "+ my_srcs +" -o "+ ReleaseBin + ExecutableName + " "+ ReleaseCFlags +" "+ AllCFlags + " " + LinkFlags
        if build_type == "prod":
            command: str = Compiler + " "+ my_srcs +" -o "+ ProdBin + ExecutableName + " "+ ProdCFlags +" "+ AllCFlags + " " + LinkFlags
        plog(" Linking   ("+build_type.center(7, " ")+"): "+ExecutableName)
        result = subprocess.run(command, shell=True)
        if result.returncode != 0:
            if build_type == "test":
                build_fail_test = True
            if build_type == "debug":
                build_fail_debug = True
            if build_type == "release":
                build_fail_release = True
            if build_type == "prod":
                build_fail_prod = True

def StripThread():
    global PendingSources
    while len(PendingSources) > 0:
        size_before: int = 0
        size_after: int = 0
        build_type: str = PendingSources.pop()[0]
        binary: str = ""
        if build_type == "test":
            binary = TestBin + ExecutableName
        if build_type == "debug":
            binary = DebugBin + ExecutableName
        if build_type == "release":
            binary = ReleaseBin + ExecutableName
        if build_type == "prod":
            binary = ProdBin + ExecutableName

        if build_type == "test":
            command: str = StripUtil +" "+ binary +" "+ TestStripFlag
        if build_type == "debug":
            command: str = StripUtil +" "+ binary +" "+ DebugStripFlag
        if build_type == "release":
            command: str = StripUtil +" "+ binary +" "+ ReleaseStripFlag
        if build_type == "prod":
            command: str = StripUtil +" "+ binary +" "+ ProdStripFlag
        size_before = os.path.getsize(binary)
        plog(" Stripping ("+build_type.center(7, " ")+"): "+ExecutableName)
        result = subprocess.run(command, shell=True)
        size_after = os.path.getsize(binary)
        if result.returncode != 0:
            if build_type == "debug":
                log("Debug strip failed")
            if build_type == "release":
                log("Release strip failed")
            if build_type == "prod":
                log("Prod strip failed")
        else:
            #log(" File size before strip ("+build_type.center(7, " ")+"):  "+str(size_before))
            #log(" File size after strip  ("+build_type.center(7, " ")+"):  "+str(size_after))
            #log(" File size reduction    ("+build_type.center(7, " ")+"):  "+str(size_before - size_after))
            log(" File size reduction %  ("+build_type.center(7, " ")+"):  "+str(round(((size_before - size_after)/size_before) * 100, 3)))

if __name__ == "__main__":
    start_time = time.time()
    if len(sys.argv) < 2:
        print("No build flag, usage:")
        print(" ./mybuild.py [build flag] [flags]\n")
        print("  valid build flags:")
        print("   test      - no optimization quick build")
        print("   debug     - no optimization, debug-info-laden build (very large binaries)")
        print("   release   - light optimization 'preview' build (for stress testing)")
        print("   prod      - fully optimized production build")
        print("   all       - alias for all of the above")
        print("   run       - build test and run it")
        print("   clean     - deletes the bin directory (after all other targets)")
        print("\n  valid flags")
        print("   --verbose - verbose logging")
        print("   -v        - [alias] verbose logging")
        print("   --silent  - do not log at all")
        print("   -s        - [alias] silent")
        print("   --force   - force build all sources")
        print("   -f        - [alias] force build")
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
        if "-v" in sys.argv or "--verbose" in sys.argv:
            verbose_logging = True
        if "-s" in sys.argv or "--silent" in sys.argv:
            silent_mode = True
        if "-f" in sys.argv or "--force" in sys.argv:
            force_build = True

    os.makedirs(".mybuild/", exist_ok=True)
    if test_build:
        os.makedirs(TestObjBin, exist_ok=True)
        os.makedirs(TestBin, exist_ok=True)
        try:
            with open(".mybuild/testhashes.db", "r") as testhfd:
                test_hashes = testhfd.readlines()
        except:
            pass
    if debug_build:
        os.makedirs(DebugObjBin, exist_ok=True)
        os.makedirs(DebugBin, exist_ok=True)
        try:
            with open(".mybuild/debughashes.db", "r") as debughfd:
                debug_hashes = debughfd.readlines()
        except:
            pass
    if release_build:
        os.makedirs(ReleaseObjBin, exist_ok=True)
        os.makedirs(ReleaseBin, exist_ok=True)
        try:
            with open(".mybuild/releasehashes.db", "r") as releasehfd:
                release_hashes = releasehfd.readlines()
        except:
            pass
    if prod_build:
        os.makedirs(ProdObjBin, exist_ok=True)
        os.makedirs(ProdBin, exist_ok=True)
        try:
            with open(".mybuild/prodhashes.db", "r") as prodhfd:
                prod_hashes = prodhfd.readlines()
        except:
            pass

    built_something: bool = True
    get_all_srcs()
    log("Running checks...")
    thread_count = os.cpu_count()
    if thread_count == None:
        HashCheckThread()
    elif thread_count > len(Sources):
        thread_count = len(Sources)
    
    if thread_count != None:
        log("Using "+str(thread_count)+" threads")
        AllThreads: list[threading.Thread] = []
        for thread_number in range(thread_count):
            AllThreads += [threading.Thread(target=HashCheckThread)]
        for thread_number in range(thread_count):
            AllThreads[thread_number].start()
        for thread_number in range(thread_count):
            AllThreads[thread_number].join()

    if len(PendingSources) == 0:
        log("Nothing to build")
        built_something = False
    else:
        log("Compiling...")
        thread_count = os.cpu_count()
        if thread_count == None and len(PendingSources) > 0:
            CompilationThread()
        elif thread_count > len(PendingSources):
            thread_count = len(PendingSources)

        if thread_count != None and len(PendingSources) > 0:
            log("Using "+str(thread_count)+" threads")
            AllThreads: list[threading.Thread] = []
            for thread_number in range(thread_count):
                AllThreads += [threading.Thread(target=CompilationThread)]
            for thread_number in range(thread_count):
                AllThreads[thread_number].start()
            for thread_number in range(thread_count):
                AllThreads[thread_number].join()

        log("Linking...")
        if test_build:
            PendingSources += [("test", "")]
        if debug_build:
            PendingSources += [("debug", "")]
        if release_build:
            PendingSources += [("release", "")]
        if prod_build:
            PendingSources += [("prod", "")]
        thread_count = os.cpu_count()
        if thread_count == None and len(PendingSources) > 0:
            LinkThread()
        elif thread_count > len(PendingSources):
            thread_count = len(PendingSources)

        if thread_count != None and len(PendingSources) > 0:
            log("Using "+str(thread_count)+" threads")
            AllThreads: list[threading.Thread] = []
            for thread_number in range(thread_count):
                AllThreads += [threading.Thread(target=LinkThread)]
            for thread_number in range(thread_count):
                AllThreads[thread_number].start()
            for thread_number in range(thread_count):
                AllThreads[thread_number].join()
    
        log("Strip...")
        if release_build:
            PendingSources += [("release", "")]
        if prod_build:
            PendingSources += [("prod", "")]
        thread_count = os.cpu_count()
        if thread_count == None and len(PendingSources) > 0:
            StripThread()
        elif thread_count > len(PendingSources):
            thread_count = len(PendingSources)

        if thread_count != None and len(PendingSources) > 0:
            log("Using "+str(thread_count)+" threads")
            AllThreads: list[threading.Thread] = []
            for thread_number in range(thread_count):
                AllThreads += [threading.Thread(target=StripThread)]
            for thread_number in range(thread_count):
                AllThreads[thread_number].start()
            for thread_number in range(thread_count):
                AllThreads[thread_number].join()

    if built_something:
        plog("Build time: "+str(round(time.time()-start_time, 3))+"s")

    log("Saving state...")
    if test_build and not build_fail_test:
        with open(".mybuild/testhashes.db", "w") as testhfd:
            testhfd.writelines(new_test_hashes)
    if debug_build and not build_fail_debug:
        with open(".mybuild/debughashes.db", "w") as debughfd:
            debughfd.writelines(new_debug_hashes)
    if release_build and not build_fail_release:
        with open(".mybuild/releasehashes.db", "w") as releasehfd:
            releasehfd.writelines(new_release_hashes)
    if prod_build and not build_fail_prod:
        with open(".mybuild/prodhashes.db", "w") as prodhfd:
            prodhfd.writelines(new_prod_hashes)

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
        log("Running test...")
        returncode: int = subprocess.run(TestBin+ExecutableName,shell=True).returncode
        if returncode == 0:
            plog("Test success!")
        else:
            plog("Test fail, returncode: "+str(returncode))

    if clean:
        log("Cleaning...")
        shutil.rmtree("bin", ignore_errors=True)
        shutil.rmtree(".mybuild", ignore_errors=True)
    
    if build_fail_test:
        print("Test build failed")
    if build_fail_debug:
        print("Debug build failed")
    if build_fail_release:
        print("Release build failed")
    if build_fail_prod:
        print("Prod build failed")