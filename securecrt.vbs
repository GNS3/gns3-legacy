#$Language = "VBScript"
#$Interface = "1.0"

Sub main
	crt.window.caption = crt.arguments(0)
	crt.Sleep 1000
	crt.Screen.Send chr(13)
End Sub
