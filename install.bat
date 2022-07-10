REM Installing Python dependencies
pip install pywin32
pip install wxPython

REM Building configuration files
for /R %%f in (*install.py) do (
    cd "%%~dpf"
    python "%%f"
)