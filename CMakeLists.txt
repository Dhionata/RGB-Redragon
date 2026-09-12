cmake_minimum_required(VERSION 3.20)
project(FlowersBlooming VERSION 1.0.0 LANGUAGES C CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Compiler optimization and warning flags
if(MSVC)
    set(CMAKE_MSVC_RUNTIME_LIBRARY "MultiThreaded$<$<CONFIG:Debug>:Debug>")
    add_compile_options(/W3 /permissive- /utf-8)
    add_definitions(-D_CRT_SECURE_NO_WARNINGS -DNOMINMAX -DWIN32_LEAN_AND_MEAN)
else()
    add_compile_options(-Wall -Wextra -O3 -fno-strict-aliasing)
    # Statically link libgcc and libstdc++ so binary is 100% standalone without external DLLs
    set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -static-libgcc -static-libstdc++ -static")
    set(CMAKE_SHARED_LINKER_FLAGS "${CMAKE_SHARED_LINKER_FLAGS} -static-libgcc -static-libstdc++")
endif()

include_directories(
    ${CMAKE_CURRENT_SOURCE_DIR}/include
    ${CMAKE_CURRENT_SOURCE_DIR}/src
    ${CMAKE_CURRENT_SOURCE_DIR}
)

# Core Library Sources (reusable between main app and unit tests)
set(LIB_SOURCES
    src/core/models/color_rgb.cpp
    src/core/models/color_hsv.cpp
    src/core/models/key_coordinate.cpp
    src/core/models/render_frame.cpp
    src/core/models/effect_config.cpp
    src/core/json_helper.cpp
    src/math/fast_color.cpp
    src/math/easing.cpp
    src/math/spatial_grid.cpp
    src/effects/petal_geometry.cpp
    src/effects/flower_instance.cpp
    src/effects/blooming_engine.cpp
    src/effects/random_blend_engine.cpp
    src/effects/effect_engine_factory.cpp
    src/effects/palettes/base_palette.cpp
    src/effects/palettes/sakura_palette.cpp
    src/effects/palettes/rose_palette.cpp
    src/effects/palettes/lotus_palette.cpp
    src/effects/palettes/sunflower_palette.cpp
    src/effects/palettes/lavender_palette.cpp
    src/effects/palettes/rainbow_palette.cpp
    src/effects/palettes/cyberpunk_palette.cpp
    src/effects/palettes/aurora_palette.cpp
    src/effects/palettes/palette_registry.cpp
    src/effects/blending/organic_weighted_blend.cpp
    src/effects/blending/additive_blend.cpp
    src/effects/blending/screen_blend.cpp
    src/hardware/k556_matrix_layout_provider.cpp
    src/hardware/k556_layout_provider.cpp
    src/hardware/mock_transmitter.cpp
    src/hardware/redragon_k556_transmitter.cpp
    src/hardware/openrgb_transmitter.cpp
    src/hardware/transmitter_factory.cpp
    src/hardware/layout_factory.cpp
    src/service/runner_service.cpp
    src/service/config_storage_service.cpp
    src/service/windows_startup_service.cpp
    src/cli/argument_parser.cpp
    src/gui/system_tray.cpp
)

set(PLATFORM_LIBS "")
if(WIN32)
    set(PLATFORM_LIBS hid setupapi ws2_32 shell32 user32 advapi32)
endif()

# Static library for core logic
add_library(flowers_core STATIC ${LIB_SOURCES})
target_link_libraries(flowers_core PUBLIC ${PLATFORM_LIBS})

# Windows resources (version metadata and icon)
set(APP_RESOURCES "")
if(WIN32)
    set(APP_RESOURCES src/version.rc)
endif()

# Main Standalone Native Executable
add_executable(FlowersBlooming src/main.cpp ${APP_RESOURCES})
target_link_libraries(FlowersBlooming PRIVATE flowers_core)
set_target_properties(FlowersBlooming PROPERTIES OUTPUT_NAME "FlowersBlooming")
if(MSVC)
    target_sources(FlowersBlooming PRIVATE "${CMAKE_CURRENT_SOURCE_DIR}/src/app.manifest")
endif()

# Unit Tests Executable
set(TEST_SOURCES
    tests/cpp/test_main.cpp
    tests/cpp/test_color_models.cpp
    tests/cpp/test_math.cpp
    tests/cpp/test_palettes.cpp
    tests/cpp/test_blending.cpp
    tests/cpp/test_engines.cpp
    tests/cpp/test_layouts.cpp
    tests/cpp/test_hardware_packets.cpp
    tests/cpp/test_config.cpp
    tests/cpp/test_cli.cpp
)

add_executable(tests_cpp ${TEST_SOURCES} ${APP_RESOURCES})
target_link_libraries(tests_cpp PRIVATE flowers_core)
if(MSVC)
    target_sources(tests_cpp PRIVATE "${CMAKE_CURRENT_SOURCE_DIR}/src/app.manifest")
endif()

# Shared test library to allow execution via ctypes runner in environments blocking untrusted executables
if(MINGW)
    add_library(flowers_tests_shared SHARED ${TEST_SOURCES} ${APP_RESOURCES})
    target_link_libraries(flowers_tests_shared PRIVATE flowers_core)
    target_compile_definitions(flowers_tests_shared PRIVATE BUILDING_TESTS_DLL)
endif()

enable_testing()
add_test(NAME UnitTests COMMAND tests_cpp)

# Optional packaging target (executed manually or via build scripts)
add_custom_target(dist_package
    COMMAND ${CMAKE_COMMAND} -E make_directory ${CMAKE_CURRENT_SOURCE_DIR}/dist/FlowersBlooming_Portable
    COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_FILE:FlowersBlooming> ${CMAKE_CURRENT_SOURCE_DIR}/dist/FlowersBlooming_Portable/FlowersBlooming.exe
    COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_FILE:FlowersBlooming> ${CMAKE_CURRENT_SOURCE_DIR}/dist/FlowersBlooming.exe
    COMMAND ${CMAKE_COMMAND} -E copy ${CMAKE_CURRENT_SOURCE_DIR}/config.example.json ${CMAKE_CURRENT_SOURCE_DIR}/dist/FlowersBlooming_Portable/config.example.json
    COMMAND ${CMAKE_COMMAND} -E copy ${CMAKE_CURRENT_SOURCE_DIR}/README.md ${CMAKE_CURRENT_SOURCE_DIR}/dist/FlowersBlooming_Portable/README.md
    DEPENDS FlowersBlooming
)
