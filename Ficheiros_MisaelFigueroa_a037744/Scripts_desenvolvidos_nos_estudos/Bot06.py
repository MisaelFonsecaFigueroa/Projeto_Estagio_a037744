import rpa as r
import pyautogui as p
import pandas as pd
import os as o

r.init(headless_mode=True, chrome_browser=True)
r.url('https://rpachallengeocr.azurewebsites.net/')
window = p.getActiveWindow()
window.maximize()
p.sleep(5)

countPage = 1
while countPage <= 3:
    r.table('//*[@id="tableSandbox"]', 'Temp.csv')
    dados = pd.read_csv('Temp.csv')
    if countPage == 1:
        dados.to_csv(r'WebTable.csv', mode='a', index=None, header=True)
    else:
        dados.to_csv(r'WebTable.csv', mode='a', index=None, header=False)
    r.click('//*[@id="tableSandbox_next"]')
    countPage += 1
r.close()
o.remove('Temp.csv')

csv_xlsx = pd.read_csv('WebTable.csv')
csv_xlsx.to_excel(r'WebTable2.xlsx')
