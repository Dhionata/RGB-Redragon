#include "openrgb_flowers/service/windows_startup_service.hpp"

#ifdef _WIN32
#include <windows.h>
#endif

#include <iostream>
#include <vector>

namespace openrgb_flowers::service {

WindowsStartupService::WindowsStartupService(std::string app_name)
    : app_name_(std::move(app_name)) {}

bool WindowsStartupService::is_enabled() const {
#ifdef _WIN32
    HKEY key = nullptr;
    if (RegOpenKeyExW(HKEY_CURRENT_USER, L"Software\\Microsoft\\Windows\\CurrentVersion\\Run", 0, KEY_READ, &key) != ERROR_SUCCESS) {
        return false;
    }

    std::wstring wname(app_name_.begin(), app_name_.end());
    DWORD type = 0;
    LONG res = RegQueryValueExW(key, wname.c_str(), nullptr, &type, nullptr, nullptr);
    RegCloseKey(key);
    return res == ERROR_SUCCESS;
#else
    return false;
#endif
}

bool WindowsStartupService::enable(const std::string& extra_args) const {
#ifdef _WIN32
    wchar_t exe_path[MAX_PATH];
    GetModuleFileNameW(nullptr, exe_path, MAX_PATH);

    std::wstring wextra(extra_args.begin(), extra_args.end());
    std::wstring cmd = L"\"" + std::wstring(exe_path) + L"\" " + wextra;

    HKEY key = nullptr;
    if (RegCreateKeyExW(HKEY_CURRENT_USER, L"Software\\Microsoft\\Windows\\CurrentVersion\\Run", 0, nullptr, 0, KEY_SET_VALUE, nullptr, &key, nullptr) != ERROR_SUCCESS) {
        return false;
    }

    std::wstring wname(app_name_.begin(), app_name_.end());
    LONG res = RegSetValueExW(
        key,
        wname.c_str(),
        0,
        REG_SZ,
        reinterpret_cast<const BYTE*>(cmd.c_str()),
        static_cast<DWORD>((cmd.size() + 1) * sizeof(wchar_t))
    );
    RegCloseKey(key);
    return res == ERROR_SUCCESS;
#else
    return false;
#endif
}

bool WindowsStartupService::disable() const {
#ifdef _WIN32
    HKEY key = nullptr;
    if (RegOpenKeyExW(HKEY_CURRENT_USER, L"Software\\Microsoft\\Windows\\CurrentVersion\\Run", 0, KEY_SET_VALUE, &key) != ERROR_SUCCESS) {
        return true;
    }

    std::wstring wname(app_name_.begin(), app_name_.end());
    RegDeleteValueW(key, wname.c_str());
    RegCloseKey(key);
    return true;
#else
    return false;
#endif
}

} // namespace openrgb_flowers::service
