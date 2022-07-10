# AnyLanguageArduino
Arduino IDE that supports arbitrary coding languages

## Installation:
Currently only the Windows OS is supported. This project was written
with compatibility in Linux Mint in mind; however, this feature has
not been fully written and tested yet.

AnyLanguageArduino was developed using Python 3.9.6 and a compatible 
version of Python must be installed on your computer in order to run 
he IDE.

Run the file "install.bat" file to install Python dependences and 
automatically generate the .cfg config files for each supported language
package.

## Usage:
### To launch the program:
> "AnyLanguageArduino.bat"
### To load an existing sketch:
Drag an Arduino sketch with the appropriate filename extension into the
AnyLanguageArduino application window.
### To create a new sketch:
Drag a windows folder into the AnyLanguageArduino application window to
create a new sketch (based on the example template defined in the 
appropriate .cfg configuration file)
### To save your sketch:
Sketches are saved automatically.
### To change 'new sketch' template:
The location of this template is the SOURCE CODE variable in the .cfg config
file. It is a regular code file with special text strings [FILENAME], 
[AUTHOUR], [DAY], [MONTH], [YEAR] that will automatically populate upon
creation of a new file.
### Everything else:
Have a look through the .cfg and template files. These contain a number of
configurable options.