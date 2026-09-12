#include "tests/cpp/test_framework.hpp"

#ifdef _WIN32
#define EXPORT_TEST __declspec(dllexport)
#else
#define EXPORT_TEST
#endif

extern "C" EXPORT_TEST int run_all_tests() {
    return ::openrgb_flowers::testing::TestRegistry::instance().run_all();
}

#ifndef BUILDING_TESTS_DLL
int main() {
    return run_all_tests();
}
#endif
