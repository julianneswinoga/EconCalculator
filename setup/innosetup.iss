[Setup]
AppName=Econ Calculator
AppVersion=2.0
DefaultDirName={pf}\EconCalculator
DisableProgramGroupPage=yes

[Files]
Source: "../*"; Excludes: "setup.exe"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\EconCalculator"; Filename: "C:\Python27\pythonw.exe"; WorkingDir: "{app}"; Parameters: """{app}\EconCalculator\econcalculator.py""";
;IconFilename: "{app}\favicon.ico"

[Run]
;Generate LaTeX images
Filename: "C:\Python27\python.exe"; WorkingDir: "{app}\GUI"; Parameters: """{app}\GUI\GenerateImages.py""";
;getpip
Filename: "C:\Python27\python.exe"; WorkingDir: "{app}"; Parameters: """{app}\setup\getpip.py""";
;pip install pygtk
Filename: "C:\Python27\Scripts\pip.exe"; WorkingDir: "{app}"; Parameters: """install pygtk""";
;pip install py-expression-eval
Filename: "C:\Python27\Scripts\pip.exe"; WorkingDir: "{app}"; Parameters: """install py-expression-eval""";