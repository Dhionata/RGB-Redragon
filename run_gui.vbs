' OpenRGB Flowers Blooming - Silent GUI Launcher (Zero Console Window)
Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
strDir = fso.GetParentFolderName(WScript.ScriptFullName)
WshShell.CurrentDirectory = strDir

' Resolve pythonw.exe path
strLocalPyw = WshShell.ExpandEnvironmentStrings("%LOCALAPPDATA%") & "\Programs\Python\Python310\pythonw.exe"
If fso.FileExists(strLocalPyw) Then
    cmd = """" & strLocalPyw & """ -m openrgb_flowers --gui"
Else
    cmd = "pythonw.exe -m openrgb_flowers --gui"
End If

WshShell.Run cmd, 0, False

Set WshShell = Nothing
Set fso = Nothing
