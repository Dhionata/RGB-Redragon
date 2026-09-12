#include "tests/cpp/test_framework.hpp"
#include "openrgb_flowers/cli/argument_parser.hpp"

using namespace openrgb_flowers::cli;

TEST_CASE(CLI, DefaultValues) {
    std::vector<std::string> args = {};
    auto parsed = ArgumentParser::parse(args);

    EXPECT_FALSE(parsed.show_help);
    EXPECT_FALSE(parsed.mock);
    EXPECT_FALSE(parsed.tray);
    EXPECT_FALSE(parsed.autostart);
    EXPECT_FALSE(parsed.install_startup);
    EXPECT_FALSE(parsed.uninstall_startup);
    EXPECT_EQ(parsed.driver, "auto");
    EXPECT_EQ(parsed.config.effect_type, "blooming");
    EXPECT_EQ(parsed.config.palette_name, "sakura");
    EXPECT_NEAR(parsed.config.fps, 30.0f, 0.01f);
    EXPECT_NEAR(parsed.config.speed, 1.0f, 0.01f);
    EXPECT_EQ(parsed.config.max_flowers, 7);
    EXPECT_NEAR(parsed.config.spawn_rate, 1.4f, 0.01f);
    EXPECT_NEAR(parsed.config.brightness, 1.0f, 0.01f);
    EXPECT_NEAR(parsed.config.saturation, 1.0f, 0.01f);
    EXPECT_EQ(parsed.config.blend_mode, "weighted");
    EXPECT_EQ(parsed.config.host, "127.0.0.1");
    EXPECT_EQ(parsed.config.port, 6742);
    EXPECT_FALSE(parsed.max_frames.has_value());
}

TEST_CASE(CLI, HelpFlag) {
    std::vector<std::string> args1 = {"--help"};
    auto p1 = ArgumentParser::parse(args1);
    EXPECT_TRUE(p1.show_help);

    std::vector<std::string> args2 = {"-h"};
    auto p2 = ArgumentParser::parse(args2);
    EXPECT_TRUE(p2.show_help);
}

TEST_CASE(CLI, LongFlags) {
    std::vector<std::string> args = {
        "--effect", "random_blend",
        "--palette", "cyberpunk",
        "--fps", "60",
        "--speed", "2.5",
        "--max-flowers", "10",
        "--spawn-rate", "3.0",
        "--brightness", "0.7",
        "--saturation", "1.5",
        "--blend", "additive",
        "--driver", "redragon",
        "--host", "192.168.1.100",
        "--port", "8888",
        "--device", "K556",
        "--config", "custom.json",
        "--max-frames", "500",
        "--tray"
    };

    auto p = ArgumentParser::parse(args);
    EXPECT_EQ(p.config.effect_type, "random_blend");
    EXPECT_EQ(p.config.palette_name, "cyberpunk");
    EXPECT_NEAR(p.config.fps, 60.0f, 0.01f);
    EXPECT_NEAR(p.config.speed, 2.5f, 0.01f);
    EXPECT_EQ(p.config.max_flowers, 10);
    EXPECT_NEAR(p.config.spawn_rate, 3.0f, 0.01f);
    EXPECT_NEAR(p.config.brightness, 0.7f, 0.01f);
    EXPECT_NEAR(p.config.saturation, 1.5f, 0.01f);
    EXPECT_EQ(p.config.blend_mode, "additive");
    EXPECT_EQ(p.driver, "redragon");
    EXPECT_EQ(p.config.host, "192.168.1.100");
    EXPECT_EQ(p.config.port, 8888);
    EXPECT_EQ(p.config.device_name, "K556");
    EXPECT_EQ(p.config_file, "custom.json");
    EXPECT_TRUE(p.max_frames.has_value());
    EXPECT_EQ(p.max_frames.value(), 500);
    EXPECT_TRUE(p.tray);
}

TEST_CASE(CLI, ShortFlags) {
    std::vector<std::string> args = {
        "-e", "random_blend",
        "-p", "aurora",
        "-s", "1.8",
        "-b", "0.5",
        "-m", "5",
        "-d", "Redragon",
        "-c", "test.json"
    };

    auto p = ArgumentParser::parse(args);
    EXPECT_EQ(p.config.effect_type, "random_blend");
    EXPECT_EQ(p.config.palette_name, "aurora");
    EXPECT_NEAR(p.config.speed, 1.8f, 0.01f);
    EXPECT_NEAR(p.config.brightness, 0.5f, 0.01f);
    EXPECT_EQ(p.config.max_flowers, 5);
    EXPECT_EQ(p.config.device_name, "Redragon");
    EXPECT_EQ(p.config_file, "test.json");
}

TEST_CASE(CLI, MockAndAutostartFlags) {
    std::vector<std::string> args = {"--mock", "--autostart"};
    auto p = ArgumentParser::parse(args);
    EXPECT_TRUE(p.mock);
    EXPECT_EQ(p.driver, "mock");
    EXPECT_TRUE(p.autostart);
    EXPECT_TRUE(p.tray);
}

TEST_CASE(CLI, StartupRegistrationFlags) {
    std::vector<std::string> args1 = {"--install-startup"};
    auto p1 = ArgumentParser::parse(args1);
    EXPECT_TRUE(p1.install_startup);

    std::vector<std::string> args2 = {"--uninstall-startup"};
    auto p2 = ArgumentParser::parse(args2);
    EXPECT_TRUE(p2.uninstall_startup);
}

TEST_CASE(CLI, DurationFlag) {
    std::vector<std::string> args = {"--mock", "--duration", "5", "--fps", "30"};
    auto p = ArgumentParser::parse(args);
    EXPECT_TRUE(p.mock);
    EXPECT_TRUE(p.duration.has_value());
    EXPECT_NEAR(p.duration.value(), 5.0f, 0.01f);
    EXPECT_TRUE(p.max_frames.has_value());
    EXPECT_EQ(p.max_frames.value(), 150);
}

