import pandas as pd
import prince

from sklearn import preprocessing


#data = pd.read_csv('datawithcat2.csv')

data = pd.read_csv('Data_16nov.csv')


# Deleting the first columns of sequence number
#data.drop(data.columns[0],axis=1,inplace=True)

# Printing basic info of dataset
print ('Number of records:',data.shape[0])
print ('Number of attributes:',data.shape[1])


# Printing Column names
print([a for a in data.columns])

raw_data = data.drop(['timestamp','group'],axis=1)

# Stadardizing the dataset
#std_rawdata = preprocessing.StandardScaler().fit_transform(raw_data)
"""
mca = prince.MCA(n_components =2, n_iter=3,copy=True,engine='auto')
mca = mca.fit(raw_data)
"""

groups ={'physical':['disengaged','looking','talking','intTech','intRes','intExt'],'logs':['Accessed','Create','Open','Update']}



mfa = prince.MFA(groups=groups,n_components = 2)
mfa = mfa.fit(raw_data)


#mcadf = mca.row_coordinates(raw_data)
#mcadf.to_csv('mcaresult.csv')

mfadf = mfa.row_coordinates(raw_data)
mfadf.to_csv('mfaresult2.csv')