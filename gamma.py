import ctypes


def set_gamma(gamma):
    hdc = ctypes.windll.user32.GetDC(0)

    class RAMP(ctypes.Structure):
        _fields_ = [
            ("red", ctypes.c_ushort * 256),
            ("green", ctypes.c_ushort * 256),
            ("blue", ctypes.c_ushort * 256),
        ]

    ramp = RAMP()

    for i in range(256):
        ramp.red[i] = ramp.green[i] = ramp.blue[i] = int(
            pow(i / 255.0, 1.0 / gamma) * 65535.0 + 0.5
        )

    result = ctypes.windll.gdi32.SetDeviceGammaRamp(hdc, ctypes.byref(ramp))

    ctypes.windll.user32.ReleaseDC(0, hdc)

    if not result:
        raise Exception(
            "SetDeviceGammaRamp() failed: " + str(ctypes.GetLastError())
        )


# Example usage
set_gamma(1)
