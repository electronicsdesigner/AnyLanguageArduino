#!/bin/bash
# Upload script for [FILENAME].jun
#   Authour:  [AUTHOUR]
#   Created:  [DAY] [MONTH], [YEAR]

echo Cross compiling Juniper sketch to c++
mkdir -p "[DIRECTORY]/[FILENAME]"
cp "[DIRECTORY]/[FILENAME].jun" "[DIRECTORY]/[FILENAME]/[FILENAME].jun"
"[PROGRAM DIRECTORY]/Juniper/compiler/Juniper" -s "[DIRECTORY]/[FILENAME]/[FILENAME].jun" -o "[DIRECTORY]/[FILENAME]/[FILENAME].ino"

echo Compile and upload the sketch to [PORT=/dev/ttyUSB0]  for [FQBN=arduino:avr:nano:cpu=atmega328old]
"[PROGRAM DIRECTORY]/core/arduino-cli/arduino-cli" -v compile --fqbn arduino:avr:nano:cpu=atmega328old "[DIRECTORY]/[FILENAME]/[FILENAME].ino"
"[PROGRAM DIRECTORY]/core/arduino-cli/arduino-cli" -v upload -p /dev/ttyUSB0 --fqbn arduino:avr:nano:cpu=atmega328old "[DIRECTORY]/[FILENAME]/[FILENAME].ino"

echo Clean up
rm "[DIRECTORY]/[FILENAME]/[FILENAME].ino"
rm "[DIRECTORY]/[FILENAME]/[FILENAME].jun"
rmdir "[DIRECTORY]/[FILENAME]"