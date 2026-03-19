G21        ; mm units
G90        ; absolute mode

G00 X0 Y0 Z5
G01 Z-2 F100
G01 X20 Y0
G01 X20 Y20
G01 X0 Y20
G01 X0 Y0

G00 Z5
M30