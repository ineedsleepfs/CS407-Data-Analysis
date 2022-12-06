#used for calculating the standard deviation
import numpy as n
countryData = [1404.57 /24 , 757.86 / 24, 1201.2 / 24, 905.8 / 24, 475.2 / 24 , 1534/ 24, 418 / 24, 1276.33 / 24, 2662 / 24, 720 /24]
sizeData = [60.61, 44.09, 51.47, 68.35, 72.33, 51.58, 78.6]
industry = [70, 26, 58, 51, 61]
revenue = [30, 35.28, 18.68]
countrystd = n.std(countryData)
sizestd = n.std(sizeData)
industrystd = n.std(industry)
revenuestd = n.std(revenue)

print(countrystd , countrystd / n.average(countryData))
print(sizestd , sizestd / n.average(sizeData))
print(industrystd , industrystd / n.average(industry))
print(revenuestd , revenuestd / n.average(revenue))
