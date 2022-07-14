import pyautogui as p
def funbot01():
    p.FAILSAFE = False
    p.hotkey('win','r')
    p.sleep(1)
    p.typewrite('notepad')
    p.sleep(2)
    p.press('enter')
    p.typewrite('Oi, eu sou um Bot!')
    p.sleep(2)
    valor = p.getActiveWindow()
    valor.close()
    p.press('right')
    p.sleep(2)
    p.press('enter')
funbot01()
