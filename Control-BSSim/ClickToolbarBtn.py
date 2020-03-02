#-*- coding: utf-8 -*-
import win32api, win32gui, win32con
import time
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

'''
 获取主窗体句柄
'''
mainFormList = dict() # 存储运行中的所有程序的'句柄'和'标题'

def get_all_hwnd(hwnd,mouse):
    if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
        mainFormList.update({hwnd:win32gui.GetWindowText(hwnd)}) # 更新mainFormList
win32gui.EnumWindows(get_all_hwnd, 0)

# 查询 title 中包含'Base Station Simulator'的 handle（需要BSS软件为运行状态）
# 也就是从 mainFormList 字典中查询包含'Base Station Simulator'的键
keys = [x[0] for x in mainFormList.items() if 'Base Station Simulator' in x[1]] # 该键即为BSS程序的主窗体句柄
if len(keys):
    for i in keys: #去除键的[]
        mainHandle = i
    '''
     获取子窗体句柄
     这里是获取的工具栏 ToolbarWindow32 窗口的句柄（需要操作的按钮在这其中）
    '''
    childHandleList = [] # 子窗体的句柄
    childTitleList = [] # 子窗体的标题
    win32gui.EnumChildWindows(mainHandle, lambda hwnd, param: param.append(hwnd), childHandleList) # 通过主窗体句柄，得到所有子窗体句柄

    # 通过句柄得到标题，并存储到 childTitleList
    for i in childHandleList:
        childTitleList.append(win32gui.GetClassName(i))


    # 将子窗体的'句柄'和'标题'两个list组成字典
    '''
    Ps：将句柄和标题列表合并成为字典，方便找到指定标题对应的句柄。
    有其他方法能实现相同的目的，毕竟两个列表中的值都是一一对应的。
    '''
    childFormList = dict(zip(childHandleList, childTitleList))

    # 从 childFormList 中查找值为“ToolbarWindow32”的键，即为 ToolbarWindow32 的句柄
    keys = [x[0] for x in childFormList.items() if 'ToolbarWindow32' in x[1]]
    for i in keys:
            toolbarHandle = i # 得到 ToolbarWindow32 的句柄

else:
    clr.print_text("运行前请先手动运行BSS软件！", "r")
    input("按回车键退出：")


# 单击"开始运行"按钮
def start_button(ToolbarHandle):
    # 置顶窗口后，获取坐标
    win32gui.ShowWindow(mainHandle, win32con.SW_SHOWNORMAL) # 窗口需要最大化且在后台，不能最小化 ctypes.windll.user32.ShowWindow(mainHandle, 3)
    win32gui.SetForegroundWindow(mainHandle)
    time.sleep(0.5) # 等待窗口置顶
    left, top, right, bottom = win32gui.GetWindowRect(ToolbarHandle)
    # 根据'ToolbarWindow32'窗体的大小，计算出按钮所在位置
    buttonX = left + 266 
    buttonY = top + 13

    # 鼠标定位到开始按钮的坐标
    win32api.SetCursorPos((buttonX, buttonY))
    
    # 执行鼠标左键单击
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN | win32con.MOUSEEVENTF_LEFTUP, 0,0,0,0)
    print(buttonX, buttonY)


# 单击"停止运行"按钮
def stop_button(ToolbarHandle):
    # 置顶窗口后，获取坐标
    win32gui.ShowWindow(mainHandle, win32con.SW_SHOWNORMAL) # 窗口需要最大化且在后台，不能最小化 
    ctypes.windll.user32.ShowWindow(mainHandle, 3)
    win32gui.SetForegroundWindow(mainHandle)
    # time.sleep(0.2) # 等待窗口置顶
    left, top, right, bottom = win32gui.GetWindowRect(ToolbarHandle)
    # 根据'ToolbarWindow32'窗体的大小，计算出按钮所在位置
    buttonX = left + 266 + 26
    buttonY = top + 13

    # 鼠标定位到停止按钮的坐标
    win32api.SetCursorPos((buttonX, buttonY))
    
    # 执行鼠标左键单击
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN | win32con.MOUSEEVENTF_LEFTUP, 0,0,0,0)
    print("-------------------------")
    clr.print_text("检查是否点击了 循环 按钮！", "g")


try:
    stop_button(toolbarHandle)
except Exception as e:
    print(e)
    input("请记录报错信息，按回车退出：")