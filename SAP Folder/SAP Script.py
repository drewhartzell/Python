VB Script: If Not IsObject(application) Then
   Set SapGuiAuto  = GetObject("SAPGUI")
   Set application = SapGuiAuto.GetScriptingEngine
End If
If Not IsObject(connection) Then
   Set connection = application.Children(0)
End If
If Not IsObject(session) Then
   Set session    = connection.Children(0)
End If
If IsObject(WScript) Then
   WScript.ConnectObject session,     "on"
   WScript.ConnectObject application, "on"
End If
session.findById("wnd[0]").maximize
session.findById("wnd[0]/tbar[0]/okcd").text = "sq01"
session.findById("wnd[0]").sendVKey 0
session.findById("wnd[0]/tbar[1]/btn[19]").press
session.findById("wnd[1]/usr/cntlGRID1/shellcont/shell").currentCellRow = 7
session.findById("wnd[1]/usr/cntlGRID1/shellcont/shell").selectedRows = "7"
session.findById("wnd[1]/tbar[0]/btn[0]").press
session.findById("wnd[0]/usr/ctxtRS38R-QNUM").text = "zsdvbfa"
session.findById("wnd[0]/usr/ctxtRS38R-QNUM").setFocus
session.findById("wnd[0]/usr/ctxtRS38R-QNUM").caretPosition = 7
session.findById("wnd[0]/tbar[1]/btn[8]").press
session.findById("wnd[0]/mbar/menu[2]/menu[0]/menu[0]").select
session.findById("wnd[1]/usr/cntlALV_CONTAINER_1/shellcont/shell").currentCellRow = 1
session.findById("wnd[1]/usr/cntlALV_CONTAINER_1/shellcont/shell").selectedRows = "1"
session.findById("wnd[1]/tbar[0]/btn[2]").press
session.findById("wnd[0]/tbar[1]/btn[8]").press
session.findById("wnd[0]/usr/cntlCONTAINER/shellcont/shell").pressToolbarContextButton "&MB_EXPORT"
session.findById("wnd[0]/usr/cntlCONTAINER/shellcont/shell").selectContextMenuItem "&PC"
session.findById("wnd[1]/usr/subSUBSCREEN_STEPLOOP:SAPLSPO5:0150/sub:SAPLSPO5:0150/radSPOPLI-SELFLAG[1,0]").select
session.findById("wnd[1]/usr/subSUBSCREEN_STEPLOOP:SAPLSPO5:0150/sub:SAPLSPO5:0150/radSPOPLI-SELFLAG[1,0]").setFocus
session.findById("wnd[1]/tbar[0]/btn[0]").press

' Get current date and time
Dim currentDate
currentDate = Now()

' Format date and time
Dim formattedDate
formattedDate = Year(currentDate) & "_" & Right("0" & Month(currentDate), 2) & "_" & Right("0" & Day(currentDate), 2)

' Set the filename with datetime stamp
session.findById("wnd[1]/usr/ctxtDY_FILENAME").text = "VBFA_new_" & formattedDate & ".txt"
session.findById("wnd[1]/usr/ctxtDY_PATH").text = "XXXXXXXXX"
session.findById("wnd[1]/usr/ctxtDY_PATH").setFocus
session.findById("wnd[1]/usr/ctxtDY_PATH").caretPosition = 32
session.findById("wnd[1]/tbar[0]/btn[0]").press
