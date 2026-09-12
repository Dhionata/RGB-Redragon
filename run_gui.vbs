' OpenRGB Flowers Blooming - Silent GUI Launcher (Zero Console Window)
Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
strDir = fso.GetParentFolderName(WScript.ScriptFullName)
WshShell.CurrentDirectory = strDir

' Resolve pythonw.exe path
strPyw = ""
candidates = Array( _
    strDir & "\.venv\Scripts\pythonw.exe", _
    strDir & "\venv\Scripts\pythonw.exe", _
    WshShell.ExpandEnvironmentStrings("%LOCALAPPDATA%") & "\Programs\Python\Python310\pythonw.exe", _
    WshShell.ExpandEnvironmentStrings("%LOCALAPPDATA%") & "\Programs\Python\Python311\pythonw.exe", _
    WshShell.ExpandEnvironmentStrings("%LOCALAPPDATA%") & "\Programs\Python\Python312\pythonw.exe", _
    WshShell.ExpandEnvironmentStrings("%LOCALAPPDATA%") & "\Programs\Python\Python313\pythonw.exe" _
)
For Each c In candidates
    If fso.FileExists(c) Then
        strPyw = c
        Exit For
    End If
Next

If strPyw = "" Then
    strPyw = "pythonw.exe"
End If

strLauncher = strDir & "\launcher.py"
If fso.FileExists(strLauncher) Then
    cmd = """" & strPyw & """ """ & strLauncher & """ --gui"
Else
    cmd = """" & strPyw & """ -m openrgb_flowers --gui"
End If

WshShell.Run cmd, 0, False

Set WshShell = Nothing
Set fso = Nothing
