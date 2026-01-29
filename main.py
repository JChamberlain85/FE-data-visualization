import pandas as pd

testdata = pd.read_csv('fe_sample.csv')

time = testdata['Time']

x = time.count()

print(x)