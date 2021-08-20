
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('C:\\Users\\a6384\\Dropbox\\python\\EOLT\\121250_example.CSV')
# plt.figure()
df.plot()
plt.legend(loc='best')

plt.savefig('121250_example.png')
plt.show()
print(df.describe(percentiles=None,))
# df.info()
# print(df.shape)
count = df.iloc[:50, 1:19].diff(axis=0, periods=1).abs().max().to_frame().T
print(count)

# count.info()
# noise = count.diff(axis=0, periods=1).abs().max().to_frame().T
# print(noise)
# print(noise.max().to_frame().T)
# noise.to_csv('noise.csv', sep=',')
