#include "openrgb_flowers/hardware/layout_factory.hpp"
#include "openrgb_flowers/hardware/k556_matrix_layout_provider.hpp"
#include "openrgb_flowers/hardware/k556_layout_provider.hpp"
#include "openrgb_flowers/hardware/redragon_k556_transmitter.hpp"

namespace openrgb_flowers::hardware {

std::shared_ptr<core::interfaces::ILayoutProvider> LayoutFactory::create_layout(
    const std::shared_ptr<core::interfaces::IFrameTransmitter>& transmitter
) {
    if (std::dynamic_pointer_cast<RedragonK556Transmitter>(transmitter)) {
        return std::make_shared<K556MatrixLayoutProvider>();
    }
    return std::make_shared<K556LayoutProvider>();
}

} // namespace openrgb_flowers::hardware
