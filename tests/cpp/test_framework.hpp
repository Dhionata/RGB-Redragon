#pragma once

#include <cmath>
#include <exception>
#include <functional>
#include <iostream>
#include <string>
#include <vector>

namespace openrgb_flowers::testing {

struct TestCase {
    std::string suite;
    std::string name;
    std::function<void()> func;
};

class TestRegistry {
public:
    static TestRegistry& instance() {
        static TestRegistry reg;
        return reg;
    }

    void add_test(std::string suite, std::string name, std::function<void()> func) {
        tests_.push_back({std::move(suite), std::move(name), std::move(func)});
    }

    int run_all() {
        int passed = 0;
        int failed = 0;
        std::cout << "\n==================================================\n";
        std::cout << "🧪 Running OpenRGB Flowers C++ Unit Test Suite\n";
        std::cout << "==================================================\n";

        for (const auto& test : tests_) {
            std::cout << " [RUN]  " << test.suite << "." << test.name << " ... ";
            try {
                test.func();
                std::cout << "PASSED\n";
                ++passed;
            } catch (const std::exception& e) {
                std::cout << "FAILED: " << e.what() << "\n";
                ++failed;
            } catch (...) {
                std::cout << "FAILED: Unknown exception\n";
                ++failed;
            }
        }

        std::cout << "==================================================\n";
        std::cout << "Results: " << passed << " passed, " << failed << " failed, "
                  << tests_.size() << " total.\n";
        std::cout << "==================================================\n\n";
        return failed == 0 ? 0 : 1;
    }

private:
    std::vector<TestCase> tests_;
};

struct TestRegistrar {
    TestRegistrar(const std::string& suite, const std::string& name, std::function<void()> func) {
        TestRegistry::instance().add_test(suite, name, std::move(func));
    }
};

#define TEST_CASE(suite, name) \
    void suite##_##name##_impl(); \
    static ::openrgb_flowers::testing::TestRegistrar suite##_##name##_reg(#suite, #name, suite##_##name##_impl); \
    void suite##_##name##_impl()

#define EXPECT_TRUE(cond) \
    do { \
        if (!(cond)) { \
            throw std::runtime_error(std::string("Assertion failed: ") + #cond + " at line " + std::to_string(__LINE__)); \
        } \
    } while (0)

#define EXPECT_FALSE(cond) EXPECT_TRUE(!(cond))

#define EXPECT_EQ(a, b) \
    do { \
        if ((a) != (b)) { \
            throw std::runtime_error(std::string("Assertion failed: ") + #a + " == " + #b + " at line " + std::to_string(__LINE__)); \
        } \
    } while (0)

#define EXPECT_NE(a, b) \
    do { \
        if ((a) == (b)) { \
            throw std::runtime_error(std::string("Assertion failed: ") + #a + " != " + #b + " at line " + std::to_string(__LINE__)); \
        } \
    } while (0)

#define EXPECT_GE(a, b) \
    do { \
        if (!((a) >= (b))) { \
            throw std::runtime_error(std::string("Assertion failed: ") + #a + " >= " + #b + " at line " + std::to_string(__LINE__)); \
        } \
    } while (0)

#define EXPECT_LE(a, b) \
    do { \
        if (!((a) <= (b))) { \
            throw std::runtime_error(std::string("Assertion failed: ") + #a + " <= " + #b + " at line " + std::to_string(__LINE__)); \
        } \
    } while (0)

#define EXPECT_NEAR(a, b, eps) \
    do { \
        if (std::fabs((a) - (b)) > (eps)) { \
            throw std::runtime_error(std::string("Assertion failed: |") + #a + " - " + #b + "| <= " + #eps + " at line " + std::to_string(__LINE__)); \
        } \
    } while (0)

#define EXPECT_THROW(stmt, exc_type) \
    do { \
        bool caught = false; \
        try { \
            stmt; \
        } catch (const exc_type&) { \
            caught = true; \
        } catch (...) {} \
        if (!caught) { \
            throw std::runtime_error(std::string("Expected exception: ") + #exc_type + " for " + #stmt + " at line " + std::to_string(__LINE__)); \
        } \
    } while (0)

} // namespace openrgb_flowers::testing
