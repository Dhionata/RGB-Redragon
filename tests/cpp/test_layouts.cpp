#include "tests/cpp/test_framework.hpp"
#include "openrgb_flowers/hardware/k556_matrix_layout_provider.hpp"
#include "openrgb_flowers/hardware/k556_layout_provider.hpp"
#include "openrgb_flowers/hardware/layout_factory.hpp"
#include "openrgb_flowers/hardware/mock_transmitter.hpp"
#include "openrgb_flowers/hardware/redragon_k556_transmitter.hpp"

using namespace openrgb_flowers::hardware;

TEST_CASE(Layouts, K556Matrix132Keys) {
    K556MatrixLayoutProvider provider;
    EXPECT_EQ(provider.get_key_count(), 132);

    const auto& coords = provider.get_coordinates();
    EXPECT_EQ(coords.size(), 132);

    // Escape is at (0, 0)
    EXPECT_EQ(coords[0].row, 0);
    EXPECT_EQ(coords[0].col, 0);
    EXPECT_EQ(coords[0].name, "Escape");

    // Check array pointers
    EXPECT_TRUE(provider.get_x_coords() != nullptr);
    EXPECT_TRUE(provider.get_y_coords() != nullptr);
}

TEST_CASE(Layouts, K556Physical104Keys) {
    K556LayoutProvider provider;
    EXPECT_EQ(provider.get_key_count(), 104);

    const auto& coords = provider.get_coordinates();
    EXPECT_EQ(coords.size(), 104);
    EXPECT_EQ(coords[0].name, "Escape");
}

TEST_CASE(Layouts, LayoutFactoryResolution) {
    auto mock_tx = std::make_shared<MockTransmitter>();
    auto mock_layout = LayoutFactory::create_layout(mock_tx);
    EXPECT_EQ(mock_layout->get_key_count(), 104);

    auto redragon_tx = std::make_shared<RedragonK556Transmitter>();
    auto redragon_layout = LayoutFactory::create_layout(redragon_tx);
    EXPECT_EQ(redragon_layout->get_key_count(), 132);
}
