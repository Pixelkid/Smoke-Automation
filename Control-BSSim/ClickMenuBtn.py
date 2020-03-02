import win32api
import win32con
import win32gui

# 得到父窗体句柄（主窗体）
# handle = win32gui.FindWindow(None,"ToolbarWindow32")  # {窗口标题：Caption}, {窗口类名：Class}
handle = 0x00071180
menu = win32gui.GetMenu(handle) # 菜单
menu1 = win32gui.GetSubMenu(menu, 1) # 第几个菜单
cmd_ID = win32gui.GetMenuItemID(menu1, 10) # 第几个子菜单
# 发送事件消息给菜单
#win32gui.PostMessage(hwnd, win32con.WM_COMMAND, cmd_ID, 1)

# 获取菜单的文本内容
def get_menu_item_txt(menu, idx):
    import win32gui_struct
    mii, extra = win32gui_struct.EmptyMENUITEMINFO() # 新建一个win32gui的空的结构体mii
    win32gui.GetMenuItemInfo(menu, idx, True, mii)
    ftype, fstate, wid, hsubmenu, hbmpchecked, hbmpunchecked,\
    dwitemdata, text, hbmpitem = win32gui_struct.UnpackMENUITEMINFO(mii) # 解包mii
    return text

# 遍历显示出菜单文本
for i in range(5):
    print(get_menu_item_txt(menu, i))
for i in range(5):
    print(get_menu_item_txt(menu1, i))
