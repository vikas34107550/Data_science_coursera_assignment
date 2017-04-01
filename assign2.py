import pandas as pd

		######## Part 1 #########

df = pd.read_csv('olympics.csv', index_col=0, skiprows=1)

for col in df.columns:
    if col[:2]=='01':
        df.rename(columns={col:'Gold'+col[4:]}, inplace=True)
    if col[:2]=='02':
        df.rename(columns={col:'Silver'+col[4:]}, inplace=True)
    if col[:2]=='03':
        df.rename(columns={col:'Bronze'+col[4:]}, inplace=True)
    if col[:1]=='№':
        df.rename(columns={col:'#'+col[1:]}, inplace=True)

names_ids = df.index.str.split('\s\(') # split the index by '('

df.index = names_ids.str[0] # the [0] element is the country name (new index) 
df['ID'] = names_ids.str[1].str[:3] # the [1] element is the abbreviation or ID (take first 3 characters from that)

df = df.drop('Totals')
df.head()

def answer_zero():
    # This function returns the row for Afghanistan, which is a Series object. The assignment
    # question description will tell you the general format the autograder is expecting
    return df.iloc[0]

def answer_one():
    return df['Gold'].idxmax()
    
def answer_two():
    df1 =df[(df['Gold'] > 0) | (df['Gold.1'] > 0)]
    df1['Maxdiff'] = df1['Gold'] - df1['Gold.1']
    return df1['Maxdiff'].idxmax()
    
def answer_three():
    df1 =df[(df['Gold'] > 0) & (df['Gold.1'] > 0)]
    df1['Maxdiff'] = df1['Gold'] - df1['Gold.1']
    df1['Maxdiff'] =df1['Maxdiff']/df1['Gold.2']
    return df1['Maxdiff'].idxmax()
    
def answer_four():
    df['Points'] = df['Gold.2']*3 + df['Silver.2']*2 + df['Bronze.2']*1
    return df['Points']
    
		######## Part 2 #########
	
census_df = pd.read_csv('census.csv')
census_df.head()

def answer_five():
    census_df12 = pd.DataFrame(columns=('STATE','STNAME','TotalSum'))
    for st in list(census_df.STATE.unique()):
        census_df12.loc[len(census_df12)] = [st,census_df[census_df.STATE == st].STNAME.unique(),len(census_df[(census_df['STATE']==st) & (census_df['SUMLEV']==50)].index)]
    return census_df12.get_value(census_df12['TotalSum'].idxmax() , 'STNAME')[0]
    
def answer_six():
    census_df11 = census_df.copy()
    census_df11 = census_df11[(census_df['STNAME']!=census_df['CTYNAME'])]
    census_df13 = pd.DataFrame(columns=('STNAME','TotalSum'))
    census_df11.sort_values(['STNAME','CENSUS2010POP'], ascending=[True ,False], inplace=True)
    census_df11 = census_df11.set_index(['STNAME'])
    for name in list(census_df11.index.unique()):
        census_df13.loc[len(census_df13)] = [name,census_df11.loc[name][:3]['CENSUS2010POP'].sum()]
    return list(census_df13['STNAME'][census_df13['TotalSum'].nlargest(3).index.get_values()])
    
def answer_seven():
    global census_df
    census_df = census_df[(census_df['STNAME']!=census_df['CTYNAME'])]
    census_df['Maxdiff'] = abs(census_df['POPESTIMATE2015']-census_df[['POPESTIMATE2010','POPESTIMATE2011','POPESTIMATE2012','POPESTIMATE2013','POPESTIMATE2014','POPESTIMATE2015']].min(axis=1))
    return census_df.get_value(census_df['Maxdiff'].idxmax(),'CTYNAME',False)
    
    
def answer_eight():
    return census_df[((census_df.REGION == 1) | (census_df.REGION == 2)) & (census_df['CTYNAME'].str.contains('Washington')==True) & (census_df.POPESTIMATE2015 >census_df.POPESTIMATE2014)][['STNAME','CTYNAME']]