#Wealthsimple CAD to USD conversion fee calculator
#Wealthsimple applies 1.5% conversion fee on all transactions that require conversion from CAD to USD. However, this 1.5% is done on their corperate rate, which seems to be higher than the actual conversion rate.
#I was unable to determine how WS determines what their corperate is, so I simply tested it by buying and selling a USD stock.
#This program is meant to visualize how this conversion fee can impact your potential returns. It also compares fees of WS to Questrade (QT), who charges $4.95 per buy and sell, as well as currency conversion fees.
#For comparing QT to WS, since QT has fixed $4.95 fee on each buy and sell, the program compares different initial investment values, as well as one where we assume no fee applied (essentially a really large investment).

import numpy as np
import matplotlib.pyplot as plt

WSCF = 0.01935 # 0.01935 WealthSimple total conversion fee (includes both their 1.5% fee plus the difference between their corperate rate and the actual exchange rate), true for both buy and sell
QTCF = 0.014 #Questrades total conversion fee, true for both buy and sell (0.014)
QTFF = 6.7 #Questrade fixed fee (assumed to be in CAD and no taxes applied)(the $4.95 fee advertised is actually USD)
IIA_points = [100, 200, 500, 1000, 3000, 10000] # initial investment amount in CAD (BP_CAD)

plt.figure(figsize=(10, 6))

return_no_fee = np.arange(0, 20, 0.2) / 100 #range from 0 to 1 in intervals of 0.002

WS_return_with_fee = ((return_no_fee + 1)*(1/(1+(2*WSCF))))-1
WS_return_loss = return_no_fee - WS_return_with_fee
   
plt.plot(return_no_fee * 100, WS_return_loss * 100, label="WS") # WealthSimple plot

for IIA in IIA_points:
    SP_CAD = (return_no_fee + 1)*IIA # sell price in CAD
    QT_return_with_fee = (((SP_CAD/(1+QTCF)) - QTFF) / ((IIA*(2 - (1/(1+QTCF)))) + QTFF)) - 1
    QT_return_loss = return_no_fee - QT_return_with_fee

    plt.plot(return_no_fee * 100, QT_return_loss * 100, label="$ {}".format(IIA)) # Questrade plot with $X initial investment

plt.xlabel('% Return (no fee)')
plt.ylabel('% Return Lost due to Conversion Fee')
plt.title('Impact of Currency Conversion Fee on Investment Returns')
plt.legend()
plt.grid(True)
plt.show()