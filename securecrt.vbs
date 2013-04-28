#$Language = "VBScript"
#$Interface = "1.0"

'"C:\[...]\SecureCRT.EXE" /SCRIPT securecrt.vbs /ARG %d /T /TELNET %h %p

crt.Screen.Synchronous = False           'To be used only if those functions are called: "WaitForString, WaitForStrings, ReadString, or WaitForCursor" (Performance issue if "True")

Sub main
   After_Connect()                       'Do the magic for the first time :D
   Do                                    'Create a loop that will stay active and "guard" the connection status ;)
      crt.Sleep 1000                     'Activate it every 1 second
      If Not crt.Session.Connected Then  'If the connection is down try to fix it, but after waiting 5 seconds...
         For i = 5 To 1 step -1          'Show the timeout in window title, while waiting 5 seconds
            crt.Window.Caption = crt.Arguments(0) & " - Reconnect in: " & i & "s"
            crt.Sleep 1000
         Next
         On Error Resume Next            'Ignore errors when can't connect!
         crt.Session.Connect             'Will perform a reconnect
         After_Connect()                 'Used again after the connection is reestablish
      End If
   Loop
End Sub

Function After_Connect()
   crt.Window.Caption = crt.Arguments(0) 'This can be done by CLI argument /N (from v6.7.5)
   crt.Sleep 1000                        'Wait a second for the connection to be established
   'crt.Screen.Send chr(13) & chr(10)    'Sends a new line into the terminal
   crt.Screen.Send vbcrlf                'Sends a new line into the terminal (Another way to do this)
End Function
