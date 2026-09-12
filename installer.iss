; ==============================================================================
; Inno Setup Script - OpenRGB Flowers Blooming
; Produces professional standalone installer: FlowersBlooming_Setup.exe
; ==============================================================================

#ifndef MyAppVersion
#define MyAppVersion "1.0.0"
#endif

#ifndef MyAppName
#define MyAppName "OpenRGB Flowers Blooming"
#endif

#ifndef MyAppPublisher
#define MyAppPublisher "OpenRGB Community"
#endif

#ifndef MyAppURL
#define MyAppURL "https://github.com/Dhionata/RGB-Redragon"
#endif

#ifndef MyAppExeName
#define MyAppExeName "FlowersBlooming.exe"
#endif

#ifndef SourceDir
#define SourceDir "dist\FlowersBlooming_Portable"
#endif

#ifndef OutputDir
#define OutputDir "dist"
#endif

#ifndef OutputBaseFilename
#define OutputBaseFilename "FlowersBlooming_Setup"
#endif

[Setup]
; AppId identifies this application uniquely for upgrades and uninstallation
AppId={{8E0F0E38-66B8-4395-81E4-F6901844B36A}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} v{#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}/issues
AppUpdatesURL={#MyAppURL}/releases

; Per-user clean installation without forcing administrative elevation.
; {autopf} resolves to {localappdata}\Programs when PrivilegesRequired=lowest,
; and to {commonpf} if administrative privilege is explicitly chosen.
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog
DefaultDirName={autopf}\OpenRGB Flowers
DefaultGroupName=OpenRGB Flowers
AllowNoIcons=yes

; Output settings
OutputDir={#OutputDir}
OutputBaseFilename={#OutputBaseFilename}
UninstallFilesDir={app}
UninstallDisplayName={#MyAppName}
UninstallDisplayIcon={app}\assets\icon.ico
SetupIconFile=assets\icon.ico

; Compression
Compression=lzma2/normal
SolidCompression=yes

; UI and Modern Appearance
WizardStyle=modern
ArchitecturesInstallIn64BitMode=x64
DisableProgramGroupPage=yes

; Gracefully prompt to close active instances before file copy / uninstall
CloseApplications=yes
RestartApplications=no

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; Standalone portable directory containing executable and native dependencies
Source: "{#SourceDir}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; Official application icon assets
Source: "assets\*"; DestDir: "{app}\assets"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
; Start Menu shortcut
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; WorkingDir: "{app}"; IconFilename: "{app}\assets\icon.ico"
; Desktop shortcut (optional via Task)
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; WorkingDir: "{app}"; IconFilename: "{app}\assets\icon.ico"; Tasks: desktopicon
; Uninstaller shortcut in Start Menu group
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"; IconFilename: "{app}\assets\icon.ico"

[Run]
; Option to launch the application immediately upon installation completion
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#MyAppName}}"; WorkingDir: "{app}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
; Clean up runtime logs or temporary state
Type: files; Name: "{app}\*.log"
Type: dirifempty; Name: "{app}"
