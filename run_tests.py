#!/usr/bin/env python3
"""Native C++ unit test runner for OpenRGB Flowers Blooming.
Executes the compiled C++ test suite library directly via native ctypes.
Bypasses host process-creation restrictions (e.g., Avast Hardened Mode).
"""
import ctypes
import os
import sys

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        os.path.join(base_dir, "build", "libflowers_tests_shared.dll"),
        os.path.join(base_dir, "build", "flowers_tests_shared.dll"),
        os.path.join(base_dir, "build", "Release", "flowers_tests_shared.dll"),
        os.path.join(base_dir, "build", "Debug", "flowers_tests_shared.dll"),
        os.path.join(base_dir, "libflowers_tests_shared.dll"),
        os.path.join(base_dir, "flowers_tests_shared.dll"),
    ]

    dll_path = next((p for p in candidates if os.path.isfile(p)), None)
    if not dll_path:
        print("[Runner ERRO] Biblioteca de testes compartilhada (flowers_tests_shared.dll) nao encontrada.")
        print("Locais verificados:")
        for c in candidates:
            print(f"  - {c}")
        sys.exit(1)

    print(f"[Runner] Carregando suite de testes nativa C++: {dll_path}")
    try:
        # Add DLL directory to search path for dependencies on Windows
        dll_dir = os.path.dirname(dll_path)
        if hasattr(os, "add_dll_directory"):
            os.add_dll_directory(dll_dir)
            mingw_dir = r"C:\Users\xiyun\AppData\Local\Nuitka\Nuitka\Cache\downloads\gcc\x86_64\15.2.0posix-13.0.0-msvcrt-r6\mingw64\bin"
            if os.path.isdir(mingw_dir):
                os.add_dll_directory(mingw_dir)

        # Load native C++ test library
        test_lib = ctypes.CDLL(dll_path)
        test_lib.run_all_tests.restype = ctypes.c_int
        exit_code = test_lib.run_all_tests()
        sys.exit(exit_code)
    except Exception as e:
        print(f"[Runner ERRO] Falha ao executar suite de testes nativa: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
