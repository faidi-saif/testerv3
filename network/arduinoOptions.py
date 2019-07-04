'''
    '0': EP Rst.
    '1': Jtag Rst.
    '2': Shutter.
    '3' Power/Mode.

    P : press
    R : release
    V : volt
'''


RE_INIT          = str.encode("Z")

PRESS_EP_RST     = str.encode("P0")
RELEASE_EP_RST   = str.encode("R0")
VOLT_RST         = str.encode("V0")

PRESS_JTAG_RST   = str.encode("P1")
RELEASE_JTAG_RST = str.encode("R1")
VOLT_JTAG        = str.encode("V1")

PRESS_SHUTT      = str.encode("P2")
RELEASE_SHUTT    = str.encode("R2")
VOLT_SHUTT       = str.encode("V2")

PRESS_POW        = str.encode("P3")
RELEASE_POW      = str.encode("R3")
VOLT_POWER       = str.encode("V3")

