import pyautogui as p

'''p.sleep(2)
print(p.position())'''
print('Bot 04')
p.doubleClick(x=113, y=127)
p.sleep(2)
p.write('www.udemy.com')
p.press('enter')
window = p.getActiveWindow()
window.maximize()
p.sleep(2)

localPesq = p.locateOnScreen('Pesquisa.PNG', confidence=0.9)
localPesquisa = p.center(localPesq)
xPesquisa, yPesquisa = localPesquisa
#print(localPesquisa)
p.moveTo(xPesquisa, yPesquisa, duration=1)
p.click(xPesquisa, yPesquisa)

p.sleep(1)
p.write('Charles Lima')
p.press('enter')
p.sleep(2)
p.screenshot('Cursos.png')
localClo = p.locateOnScreen('Close.PNG', confidence=0.9)
localClose = p.center(localClo)
xClose, yClose = localClose
p.moveTo(xClose, yClose, duration=1)
p.click(xClose, yClose)

