Set WshShell = CreateObject("WScript.Shell")
strDir = WshShell.CurrentDirectory
WshShell.Run "cmd /c """ & strDir & "\start_voice.bat""", 0, False
