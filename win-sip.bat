REM Batch file to build sip-win-nc-3.5, -3.6 or 3.7.
REM Put this file in sip-win-nc-3.5, -3.6 or -3.7 and run it.
REM You may have to adapt it for your Python installation

python build.py
nmake

REM siplib\Makefile may be broken - copy files manually.
cd siplib
copy /y sip.h C:\python22\include
copy /y sipQt.h C:\python22\include
cd ..
