:: Upload script for [FILENAME].jun
::   Authour:  [AUTHOUR]
::   Created:  [DAY] [MONTH], [YEAR]

REM Cross compiling Juniper sketch to c++
IF NOT EXIST "[DIRECTORY]\[FILENAME]" MKDIR "[DIRECTORY]\[FILENAME]"
copy "[DIRECTORY]\[FILENAME].jun" "[DIRECTORY]\[FILENAME]\[FILENAME].jun"
"[PROGRAM DIRECTORY]\Juniper\compiler\Juniper.exe"  -s "[DIRECTORY]\[FILENAME]\[FILENAME].jun" -o "[DIRECTORY]\[FILENAME]\[FILENAME].ino"

REM Compile the sketch and upload to [PORT=COM1] for [FQBN=arduino:avr:nano:cpu=atmega328old]
"[PROGRAM DIRECTORY]\core\arduino-cli\arduino-cli.exe" -v compile --fqbn arduino:avr:nano:cpu=atmega328old "[DIRECTORY]\[FILENAME]\[FILENAME].ino"
"[PROGRAM DIRECTORY]\core\arduino-cli\arduino-cli.exe" -v upload -p COM1 --fqbn arduino:avr:nano:cpu=atmega328old "[DIRECTORY]\[FILENAME]\[FILENAME].ino"

REM Clean up
del "[DIRECTORY]\[FILENAME]\[FILENAME].ino"
del "[DIRECTORY]\[FILENAME]\[FILENAME].jun"
rmdir "[DIRECTORY]\[FILENAME]"