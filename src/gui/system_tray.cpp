#include "openrgb_flowers/gui/system_tray.hpp"

#ifdef _WIN32
#include <windows.h>
#include <shellapi.h>

constexpr UINT WM_TRAYICON = WM_USER + 101;
constexpr UINT_PTR TRAY_ICON_ID = 1;

constexpr int IDM_EFFECT_BLOOMING = 1001;
constexpr int IDM_EFFECT_RANDOM = 1002;
constexpr int IDM_PALETTE_SAKURA = 1101;
constexpr int IDM_PALETTE_ROSE = 1102;
constexpr int IDM_PALETTE_LOTUS = 1103;
constexpr int IDM_PALETTE_SUNFLOWER = 1104;
constexpr int IDM_PALETTE_LAVENDER = 1105;
constexpr int IDM_PALETTE_RAINBOW = 1106;
constexpr int IDM_PALETTE_CYBERPUNK = 1107;
constexpr int IDM_PALETTE_AURORA = 1108;
constexpr int IDM_QUIT = 1999;

namespace {

static openrgb_flowers::gui::SystemTray* s_current_tray = nullptr;

LRESULT CALLBACK TrayWndProc(HWND hwnd, UINT msg, WPARAM wParam, LPARAM lParam) {
    if (msg == WM_TRAYICON) {
        if (lParam == WM_RBUTTONUP || lParam == WM_LBUTTONUP) {
            POINT pt;
            GetCursorPos(&pt);

            HMENU hMenu = CreatePopupMenu();
            HMENU hPaletteSub = CreatePopupMenu();
            HMENU hEffectSub = CreatePopupMenu();

            AppendMenuW(hEffectSub, MF_STRING, IDM_EFFECT_BLOOMING, L"Flores Desabrochando (Blooming)");
            AppendMenuW(hEffectSub, MF_STRING, IDM_EFFECT_RANDOM, L"Mosaico Cromático (Random Blend)");
            AppendMenuW(hMenu, MF_POPUP, reinterpret_cast<UINT_PTR>(hEffectSub), L"🌸 Efeito");

            AppendMenuW(hPaletteSub, MF_STRING, IDM_PALETTE_SAKURA, L"Sakura (Cerejeira)");
            AppendMenuW(hPaletteSub, MF_STRING, IDM_PALETTE_ROSE, L"Rosa Velvet (Rose)");
            AppendMenuW(hPaletteSub, MF_STRING, IDM_PALETTE_LOTUS, L"Lótus Sagrado (Lotus)");
            AppendMenuW(hPaletteSub, MF_STRING, IDM_PALETTE_SUNFLOWER, L"Girassol Solar (Sunflower)");
            AppendMenuW(hPaletteSub, MF_STRING, IDM_PALETTE_LAVENDER, L"Lavanda Provençal (Lavender)");
            AppendMenuW(hPaletteSub, MF_STRING, IDM_PALETTE_RAINBOW, L"Arco-Íris Dinâmico (Rainbow)");
            AppendMenuW(hPaletteSub, MF_STRING, IDM_PALETTE_CYBERPUNK, L"Cyberpunk Neon");
            AppendMenuW(hPaletteSub, MF_STRING, IDM_PALETTE_AURORA, L"Aurora Boreal");
            AppendMenuW(hMenu, MF_POPUP, reinterpret_cast<UINT_PTR>(hPaletteSub), L"🎨 Paleta");

            AppendMenuW(hMenu, MF_SEPARATOR, 0, nullptr);
            AppendMenuW(hMenu, MF_STRING, IDM_QUIT, L"✕ Encerrar");

            SetForegroundWindow(hwnd);
            int cmd = TrackPopupMenu(hMenu, TPM_RETURNCMD | TPM_NONOTIFY, pt.x, pt.y, 0, hwnd, nullptr);
            DestroyMenu(hMenu);

            PostMessage(hwnd, WM_COMMAND, static_cast<WPARAM>(cmd), 0);
            return 0;
        }
    } else if (msg == WM_COMMAND) {
        int cmd = LOWORD(wParam);
        if (s_current_tray) {
            switch (cmd) {
                case IDM_EFFECT_BLOOMING:
                    PostMessage(hwnd, WM_USER + 201, 0, 0);
                    break;
                case IDM_EFFECT_RANDOM:
                    PostMessage(hwnd, WM_USER + 202, 0, 0);
                    break;
                case IDM_PALETTE_SAKURA:
                    PostMessage(hwnd, WM_USER + 301, 0, 0);
                    break;
                case IDM_PALETTE_ROSE:
                    PostMessage(hwnd, WM_USER + 302, 0, 0);
                    break;
                case IDM_PALETTE_LOTUS:
                    PostMessage(hwnd, WM_USER + 303, 0, 0);
                    break;
                case IDM_PALETTE_SUNFLOWER:
                    PostMessage(hwnd, WM_USER + 304, 0, 0);
                    break;
                case IDM_PALETTE_LAVENDER:
                    PostMessage(hwnd, WM_USER + 305, 0, 0);
                    break;
                case IDM_PALETTE_RAINBOW:
                    PostMessage(hwnd, WM_USER + 306, 0, 0);
                    break;
                case IDM_PALETTE_CYBERPUNK:
                    PostMessage(hwnd, WM_USER + 307, 0, 0);
                    break;
                case IDM_PALETTE_AURORA:
                    PostMessage(hwnd, WM_USER + 308, 0, 0);
                    break;
                case IDM_QUIT:
                    PostMessage(hwnd, WM_CLOSE, 0, 0);
                    break;
                default:
                    break;
            }
        }
        return 0;
    } else if (msg == WM_CLOSE) {
        DestroyWindow(hwnd);
        return 0;
    } else if (msg == WM_DESTROY) {
        PostQuitMessage(0);
        return 0;
    }
    return DefWindowProcW(hwnd, msg, wParam, lParam);
}

} // anonymous namespace
#endif

namespace openrgb_flowers::gui {

SystemTray::SystemTray(
    std::string tooltip,
    PaletteCallback on_palette,
    EffectCallback on_effect,
    QuitCallback on_quit
) : tooltip_(std::move(tooltip)),
    on_palette_(std::move(on_palette)),
    on_effect_(std::move(on_effect)),
    on_quit_(std::move(on_quit)) {}

SystemTray::~SystemTray() {
    stop();
}

bool SystemTray::is_running() const {
    return running_;
}

bool SystemTray::start() {
#ifdef _WIN32
    if (running_) return true;

    running_ = true;
    s_current_tray = this;
    worker_thread_ = std::thread(&SystemTray::message_loop, this);
    return true;
#else
    return false;
#endif
}

void SystemTray::stop() {
#ifdef _WIN32
    if (!running_ && !worker_thread_.joinable()) return;
    running_ = false;

    if (hwnd_) {
        PostMessageW(static_cast<HWND>(hwnd_), WM_CLOSE, 0, 0);
    }
    if (worker_thread_.joinable()) {
        if (std::this_thread::get_id() != worker_thread_.get_id()) {
            worker_thread_.join();
        }
    }
    s_current_tray = nullptr;
#endif
}

void SystemTray::message_loop() {
#ifdef _WIN32
    HINSTANCE hInstance = GetModuleHandleW(nullptr);
    const wchar_t CLASS_NAME[] = L"OpenRGBFlowersTrayClass";

    WNDCLASSEXW wx{};
    wx.cbSize = sizeof(WNDCLASSEXW);
    wx.lpfnWndProc = TrayWndProc;
    wx.hInstance = hInstance;
    wx.lpszClassName = CLASS_NAME;
    RegisterClassExW(&wx);

    HWND hWnd = CreateWindowExW(
        0, CLASS_NAME, L"OpenRGB Flowers Tray",
        WS_OVERLAPPED, 0, 0, 0, 0,
        nullptr, nullptr, hInstance, nullptr
    );
    hwnd_ = hWnd;

    NOTIFYICONDATAW nid{};
    nid.cbSize = sizeof(NOTIFYICONDATAW);
    nid.hWnd = hWnd;
    nid.uID = TRAY_ICON_ID;
    nid.uFlags = NIF_MESSAGE | NIF_ICON | NIF_TIP;
    nid.uCallbackMessage = WM_TRAYICON;
    nid.hIcon = LoadIconW(nullptr, MAKEINTRESOURCEW(32512));

    std::wstring wtip(tooltip_.begin(), tooltip_.end());
    wcsncpy_s(nid.szTip, wtip.c_str(), _countof(nid.szTip) - 1);

    Shell_NotifyIconW(NIM_ADD, &nid);

    MSG msg;
    while (GetMessageW(&msg, nullptr, 0, 0)) {
        if (msg.message == WM_USER + 201) {
            if (on_effect_) on_effect_("blooming");
        } else if (msg.message == WM_USER + 202) {
            if (on_effect_) on_effect_("random_blend");
        } else if (msg.message == WM_USER + 301) {
            if (on_palette_) on_palette_("sakura");
        } else if (msg.message == WM_USER + 302) {
            if (on_palette_) on_palette_("rose");
        } else if (msg.message == WM_USER + 303) {
            if (on_palette_) on_palette_("lotus");
        } else if (msg.message == WM_USER + 304) {
            if (on_palette_) on_palette_("sunflower");
        } else if (msg.message == WM_USER + 305) {
            if (on_palette_) on_palette_("lavender");
        } else if (msg.message == WM_USER + 306) {
            if (on_palette_) on_palette_("rainbow");
        } else if (msg.message == WM_USER + 307) {
            if (on_palette_) on_palette_("cyberpunk");
        } else if (msg.message == WM_USER + 308) {
            if (on_palette_) on_palette_("aurora");
        }

        TranslateMessage(&msg);
        DispatchMessageW(&msg);
    }

    Shell_NotifyIconW(NIM_DELETE, &nid);
    hwnd_ = nullptr;
    running_ = false;

    if (on_quit_) {
        on_quit_();
    }
#endif
}

} // namespace openrgb_flowers::gui
