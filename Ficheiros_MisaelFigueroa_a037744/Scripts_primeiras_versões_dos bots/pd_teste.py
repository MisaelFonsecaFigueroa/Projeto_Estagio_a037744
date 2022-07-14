
# import time as t
import datetime as dt
from datetime import date
import calendar as ca


'''Script utilizado para realizar teste dos mecanismos e planear a arquitetura dos ciclos for'''

# Formatar datas
dataInicio = str(date.today().replace(day=15).strftime('%Y-%m-%d'))
# dataInicio = str(date.today().replace(month=-1).strftime('%Y-%m-%d'))

mes = int(dt.datetime.now().date().month)
if mes != 1:
    mes -= 1
else:
    mes = 12

dataInicio = str(date.today().replace(month=mes).strftime('%Y-%m-%d'))
print( dataInicio)


ano = int(dt.datetime.now().date().year)
mes = int(dt.datetime.now().date().month)
if mes != 1:
    mes -= 1
else:
    mes = 12
dataInicio = str(date.today().replace(month=mes).strftime('%Y-%m-%d'))

cal = ca.Calendar()
print(f"Para o mês {mes} do ano {ano}")
for dia in cal.itermonthdays(ano, mes):
    if dia != 0:
        flexData = str(dt.datetime.now().date().replace(day=dia, month=mes).strftime('%Y-%m-%d'))


'''now = dt.datetime.date(self=)
str(now.strftime("Y-%m-%d"))
print(now)'''


# Estruttura para passar paginas de acordo com a quantidade de linhas
linhas = 10
total = 8
l = 1
currentPage = 1
paginas = int(total / linhas)
resto = int(total % linhas)

if resto != 0.0:
    paginas += 1

print(f"Paginas: {paginas}")

for y in range(1, paginas+1):
    print(f"Pagina {currentPage}")

    if y == paginas and resto != 0:
        linhas = resto
        print(f"Pagina do resto: {paginas}")

    for x in range(1, linhas+1):
        print(f"Foi adicinada a linha {l} no ficheiro!")
        l += 1

    currentPage += 1






