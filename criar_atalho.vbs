' OpenRGB Flowers Blooming - Criador de Atalho Limpo na Area de Trabalho
Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
strDir = fso.GetParentFolderName(WScript.ScriptFullName)

desktopPath = WshShell.SpecialFolders("Desktop")
shortcutPath = desktopPath & "\OpenRGB Flowers Blooming.lnk"

Set shortcut = WshShell.CreateShortcut(shortcutPath)
shortcut.TargetPath = "wscript.exe"
shortcut.Arguments = """" & strDir & "\run_gui.vbs"""
shortcut.WorkingDirectory = strDir

iconPath = strDir & "\assets\icon.ico"
If fso.FileExists(iconPath) Then
    shortcut.IconLocation = iconPath & ",0"
End If

shortcut.Description = "OpenRGB & Redragon K556 - Flores Desabrochando RGB"
shortcut.Save

WScript.Echo "Atalho criado com sucesso na Area de Trabalho com o icone oficial!"
Set shortcut = Nothing
Set WshShell = Nothing
Set fso = Nothing
