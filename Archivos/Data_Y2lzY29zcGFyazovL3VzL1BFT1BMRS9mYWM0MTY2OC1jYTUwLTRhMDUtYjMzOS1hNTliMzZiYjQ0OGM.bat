@echo on
set UserId=Y2lzY29zcGFyazovL3VzL1BFT1BMRS9mYWM0MTY2OC1jYTUwLTRhMDUtYjMzOS1hNTliMzZiYjQ0OGM
netsh wlan show interface > temp1
netsh interface ipv4 show address Wi-Fi > temp2
more +3 temp2 > temp
type temp1 temp > datos.txt
del /f/q temp1
del /f/q temp2
del /f/q temp
echo %~p0
echo %~dp0
set var=%~p0
set var=%var:\=/%
echo %var%
For /F "UseBackQ Tokens=* Delims=." %%a In (datos.txt) Do (
       Set /A Count+=1
       Call Set "Var%%Count%%=%%~a
)
set var1=%Var5: =%
set var2=%Var7: =%
set var3=%Var10: =%
set var4=%Var14: =%
set var5=%Var17: =%
set var6=%Var20: =%
setlocal EnableDelayedExpansion
set line2=%var1:*ca:=%
set line3=%var2:*:=%
set line4=%var3:*:=%
set line5=%var4:*:=%
set line6=%var5:*:=%
set line7=%var6:*:=%
set line1=!var1:/%line2%=!
setlocal DisableDelayedExpansion
curl -X POST ^ -H "content-type: application/json" ^ -d "{\"userId\":\"%UserId%\",\"mac\":\"%line2%\",\"ssid\":\"%line3%\",\"radio\":\"%line4%\",\"canal\":\"%line5%\",\"senal\":\"%line6%\",\"ip\":\"%line7%\"}" \ https://webexbotseneca.azurewebsites.net/data
del /f/q datos.txt