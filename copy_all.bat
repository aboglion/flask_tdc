@echo off
setlocal enabledelayedexpansion
net use G: \\ilnhv-fs01

set source_folder="G:\WF-OUT\OUT"
set destination_folder="G:\Aspen_Works\TDC" 
set exclude_folder_scripts="G:\Aspen_Works\TDC\scripts"
set exclude_folder_git="G:\Aspen_Works\TDC\CODE\.git"
set exclude_folder_git="G:\Aspen_Works\TDC\DB\.git"
del /q /s /f "G:\Aspen_Works\TDC\Rep\*"

set command_options=/MIR /XD "G:\Aspen_Works\TDC\CODE\.git" %exclude_folder_git% %exclude_folder_scripts% 
echo %command_options%

ROBOCOPY %source_folder% %destination_folder% %command_options%
del /q /s /f "G:\WF-OUT\OUT\Rep\*"

CD %destination_folder%\CODE
git add .
git commit -m "Auto commit at %date% %time%" 

cd %destination_folder%\DB
git add ./*BC/*.EB
@REM git commit -m "Auto commit at %date% %time%" 
  
set "mov_option="
if "%~1"=="/MOV" rd %source_folder% /s /q

echo Folder "%source_folder%" has been copied to "%destination_folder%".
if errorlevel 1 (
	pause
)