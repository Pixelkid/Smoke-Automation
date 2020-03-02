import ctypes
STD_OUTPUT_HANDLE= -11

FOREGROUND_BLUE = 0x01 # text color contains blue.
FOREGROUND_GREEN= 0x02 # text color contains green.
FOREGROUND_RED = 0x04 # text color contains red.
FOREGROUND_INTENSITY = 0x08 # text color is intensified.

BACKGROUND_BLUE = 0x10 # background color contains blue.
BACKGROUND_GREEN= 0x20 # background color contains green.
BACKGROUND_RED = 0x40 # background color contains red.
BACKGROUND_INTENSITY = 0x80 # background color is intensified.

fc_dict = { "r": FOREGROUND_RED, "g": FOREGROUND_GREEN, "b": FOREGROUND_BLUE }
bc_dict = { "r": BACKGROUND_RED, "g": BACKGROUND_GREEN, "b": BACKGROUND_BLUE }

def get_color_flag(desc, is_foreground):
    """
    通过一串描述，获取字体颜色的flag值
    """
    flag = 0
    if len(desc) < 1:
        return flag

    d = None
    if is_foreground:
        d = fc_dict
        flag = FOREGROUND_INTENSITY
    else:
        d = bc_dict
        flag = BACKGROUND_INTENSITY

    for k in desc:
        flag |= d.get(k, 0)
    return flag

class Color:
    std_out_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    default_color = FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE

    def set_cmd_color(self, color, handle=std_out_handle):
        """(color) -> bit
        Example: set_cmd_color(FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE | FOREGROUND_INTENSITY)
        """
        ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)

    def reset(self):
        self.set_cmd_color(Color.default_color)

    def print_text(self, msg, fdesc = "", bdesc = ""):
        fcolor = get_color_flag(fdesc, True)
        if 0 == fcolor:
            fcolor = Color.default_color
        self.set_cmd_color(fcolor | get_color_flag(bdesc, False))
        print (msg)
        self.reset()
        
        
clr = Color()
clr.print_text("红色文字！", "r")
clr.print_text("绿色文字！", "g")