import pandas as pd
import numpy as np
import re
import matplotlib as plot

ConDict  = {'China':'Asia', 
             'United States':'North America', 
            'Japan':'Asia', 
                      'United Kingdom':'Europe', 
                      'Russian Federation':'Europe', 
                      'Canada':'North America', 
                      'Germany':'Europe', 
                      'India':'Asia',
                      'France':'Europe', 
                      'South Korea':'Asia', 
                      'Italy':'Europe', 
                      'Spain':'Europe', 
                      'Iran':'Asia',
                      'Australia':'Australia', 
                      'Brazil':'South America'}

GDP = pd.read_csv('world_bank.csv',skiprows = [1,2,3],header=1)
GDP.replace(['Iran, Islamic Rep.','Hong Kong SAR, China','Korea, Rep.'],['Iran','Hong Kong','South Korea'],inplace = True)
col = ['Country Name','2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']
GDP1 = GDP
GDP1 = GDP1[col]

energy = pd.read_excel('Energy Indicators.xls',parse_cols=[2,3,4,5],header=8,skiprows=7,skip_footer=38)
energy = energy.rename(columns={'Unnamed: 0': 'Country','Energy Supply':'Energy Supply','Energy Supply per capita':'Energy Supply per Capita','Renewable Electricity Production':'% Renewable'})
energy.iloc[0]=np.nan
energy.replace('...', np.nan,inplace=True)
energy['Energy Supply'] = energy['Energy Supply']*1000000 
        
for names in list(energy['Country']):
    if '(' in str(names):
    	energy.Country[energy.Country==names] = names[:names.index('(')-1]
        
for names in list(energy['Country']):
    if bool(re.search(r'\d', str(names))):
        energy.Country[energy.Country==names] = re.sub("[^a-zA-Z\W]","", names)

energy.replace(['United Kingdom of Great Britain and Northern Ireland'],['United Kingdom'],inplace = True)
energy.replace(['Republic of Korea'],['South Korea'],inplace = True)
energy.replace(['United States of America'],['United States'],inplace = True)
energy.replace(['China, Hong Kong Special Administrative Region'],['Hong Kong'],inplace = True)
        
ScimEn = pd.read_excel('scimagojr-3.xlsx')

def answer_one() :
	return pd.merge(pd.merge(ScimEn[ScimEn.Rank<=15],energy,how = 'inner',on='Country'),GDP1,how= 'inner',left_on='Country',right_on='Country Name').drop('Country Name', 		 1).set_index('Country')
	
def answer_two() :
        c2 = len(pd.merge(energy,GDP1,how= 'inner',left_on='Country',right_on='Country Name').drop('Country Name', 1).set_index('Country').index)
        c3 = len(pd.merge(ScimEn,GDP1,how= 'inner',left_on='Country',right_on='Country Name').drop('Country Name', 1).set_index('Country').index)
        c4 = len(pd.merge(ScimEn,energy,how= 'inner',left_on='Country',right_on='Country').set_index('Country').index)
        d1 = len(energy.index)
        d2 = len(ScimEn.index)
        d3 = len(ScimEn.index)
        return int((d1+d2+d3)-(c2+c3+c4))

def answer_three():
    Top15 = answer_one()
    Top15['avgGDP'] = Top15[['2006','2007','2008','2009','2010','2011','2012','2013','2014','2015']].mean(axis=1)
    Top15.sort_values(['avgGDP'], ascending=[False], inplace=True)
    return Top15['avgGDP']
    
def answer_four():
    Top15 = answer_one()
    Top15['avgGDP'] = Top15[['2006','2007','2008','2009','2010','2011','2012','2013','2014','2015']].mean(axis=1)
    Top15.sort_values(['avgGDP'], ascending=[False], inplace=True)
    return Top15.iloc[5]['2015']-Top15.iloc[5]['2006']
    
def answer_five():
    Top15 = answer_one()
    return Top15['Energy Supply per Capita'].mean()
    
def answer_seven():
    Top15 = answer_one()
    Top15['ScTc'] = Top15['Self-citations']/Top15['Citations']
    return Top15['ScTc'].idxmax() ,Top15['ScTc'].max()
    
def answer_eight():
    Top15 = answer_one()
    Top15['population'] = Top15['Energy Supply']/Top15['Energy Supply per Capita']
    Top15.sort_values(['population'], ascending=[False], inplace=True)
    return Top15.index.values[2]
 
def answer_nine():
    Top15 = answer_one()
    Top15['PopEst'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']
    Top15['Citable docs per Capita'] = Top15['Citable documents'] / Top15['PopEst']
    return Top15['Citable docs per Capita'].corr(Top15['Energy Supply per Capita'])
        
def plot9():
    Top15 = answer_one()
    Top15['PopEst'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']
    Top15['Citable docs per Capita'] = Top15['Citable documents'] / Top15['PopEst']
    Top15.plot(x='Citable docs per Capita', y='Energy Supply per Capita', kind='scatter', xlim=[0, 0.0006])
    
def answer_ten():
    Top15 = answer_one()
    Top15['HighRenew'] = (Top15['% Renewable'] >=Top15['% Renewable'].median()).astype('int')
    Top15.sort_values(['Rank'], ascending=[True], inplace=True)
    return Top15['HighRenew']

def answer_eleven():
    Top15 = answer_one()
    Top15['size'] = 1
    Top15['sum'] = Top15['Energy Supply']/Top15['Energy Supply per Capita']
    grouped = Top15.groupby(ConDict).agg({'size':'count','sum':'sum'})
    grouped['mean'] = grouped['sum'] / grouped['size']
    grouped['std'] = grouped.std(axis=1)
    grouped['size'] = grouped['size'].astype(float)
    return grouped
        
def answer_twelve():
    ConDict  = {'China':'Asia', 
                      'United States':'North America', 
                      'Japan':'Asia', 
                      'United Kingdom':'Europe', 
                      'Russian Federation':'Europe', 
                      'Canada':'North America', 
                      'Germany':'Europe', 
                      'India':'Asia',
                      'France':'Europe', 
                      'South Korea':'Asia', 
                      'Italy':'Europe', 
                      'Spain':'Europe', 
                      'Iran':'Asia',
                      'Australia':'Australia', 
                      'Brazil':'South America'}
    Top15 = answer_one()
    group = ['1','2','3','4','5']
    Top15['% Renewable'] = pd.cut(Top15['% Renewable'], bins=5 ,labels=group)
    Top15['count'] = 1
    Top15 = Top15.groupby([ConDict ,'% Renewable']).agg({'count':'count'})
    return Top15
        
def answer_thirteen():
    Top15 = answer_one()
    Top15['PopEst'] = (Top15['Energy Supply']/Top15['Energy Supply per Capita']).map('{0:,}'.format)
    Top15.PopEst.apply(str)
    return Top15['PopEst']

def plot_optional():
    import matplotlib as plt

    Top15 = answer_one()
    ax = Top15.plot(x='Rank', y='% Renewable', kind='scatter', 
                    c=['#e41a1c','#377eb8','#e41a1c','#4daf4a','#4daf4a','#377eb8','#4daf4a','#e41a1c',
                       '#4daf4a','#e41a1c','#4daf4a','#4daf4a','#e41a1c','#dede00','#ff7f00'], 
                    xticks=range(1,16), s=6*Top15['2014']/10**10, alpha=.75, figsize=[16,6]);

    for i, txt in enumerate(Top15.index):
        ax.annotate(txt, [Top15['Rank'][i], Top15['% Renewable'][i]], ha='center')

    print("This is an example of a visualization that can be created to help understand the data. \
	This is a bubble chart showing % Renewable vs. Rank. The size of the bubble corresponds to the countries' \
	2014 GDP, and the color corresponds to the continent.")
 
plot_optional()