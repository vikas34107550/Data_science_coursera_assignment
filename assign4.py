import pandas as pd
import numpy as np
from scipy.stats import ttest_ind

# Use this dictionary to map state names to two letter acronyms
states = {
	  'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 		  'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 		  'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 
	  'PR': 'Puerto 	Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 		   'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida',   		   'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 		    'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'
	  }

def get_list_of_university_towns():
    '''Returns a DataFrame of towns and the states they are in from the 
    university_towns.txt list. The format of the DataFrame should be:
    DataFrame( [ ["Michigan", "Ann Arbor"], ["Michigan", "Yipsilanti"] ], 
    columns=["State", "RegionName"]  )
    
    The following cleaning needs to be done:
    
    1. For "State", removing characters from "[" to the end.
    2. For "RegionName", when applicable, removing every character from " (" to the end.
    3. Depending on how you read the data, you may need to remove newline character '\n'. '''
    import re
    file = open('university_towns.txt')
    unitwn = file.readlines()
    states = []
    for line in unitwn :
        if '[edit]' in line :
            states.append(line.split('[edit]')[0])
    
    unitwn = [ x.split(' (')[0] for x in unitwn]
    unitwn = '\n'.join(unitwn) + '\n'
    s_p = '\[edit\]\n|'.join(states) + '\[edit\]\n'
    
    unitwn = re.split(s_p, unitwn)[1:]
    cllg_dict = []
    for state in range(len(states)):
        for collage in unitwn[state].split('\n'):
            if collage != '\n' and collage != '':
                cllg_dict.append({"State":states[state], "RegionName":collage})              
    df = pd.DataFrame(cllg_dict)    
    df1 =  df.iloc[:,::-1]

    return df1
    
def get_recession_start():
    '''Returns the year and quarter of the recession start time as a 
    string value in a format such as 2005q3'''
    gdp = pd.read_excel('gdplev.xls',skiprows=5).iloc[2:,[4,5]]
    gdp = gdp.rename(index = str, columns = {'Unnamed: 4':'Quarter',
                                                 'GDP in billions of current dollars.1':'GDP (billions)'})
    gdp = gdp[gdp.Quarter >= '2000q1']
    gdp['Next Quater GDP'] = list(gdp['GDP (billions)'].iloc[1:]) + [np.NaN] 
    gdp['Second Next Quater GDP'] = list(gdp['GDP (billions)'].iloc[2:]) + 2*[np.NaN]
    gdp['Recession Start'] = (gdp['GDP (billions)'] > gdp['Next Quater GDP']) & (gdp['Next Quater GDP'] > gdp['Second Next Quater GDP'] )
    reces = gdp[gdp['Recession Start'] == True]
    
    return reces.iloc[0]['Quarter']
    
def get_recession_end():
    '''Returns the year and quarter of the recession end time as a 
    string value in a format such as 2005q3'''
    rec_start = get_recession_start()
    gdp = pd.read_excel('gdplev.xls',skiprows=5).iloc[2:,[4,6]]
    gdp = gdp.rename(index = str, columns = {'Unnamed: 4':'Quarter',
                                                 'GDP in billions of chained 2009 dollars.1':'GDP (billions)'})
    gdp = gdp[gdp.Quarter >= '2000q1']
    gdp['Previous Quater GDP'] = [np.NaN]  + list(gdp['GDP (billions)'].iloc[:-1]) 
    gdp['Second Previous Quater GDP'] = 2*[np.NaN]  + list(gdp['GDP (billions)'].iloc[:-2]) 
    gdp['Recession End'] = (gdp['GDP (billions)'] > gdp['Previous Quater GDP']) & (gdp['Previous Quater GDP'] > gdp['Second Previous Quater GDP'] ) & (gdp['Quarter'] > rec_start)
    reces = gdp[gdp['Recession End'] == True]  
    return reces.iloc[0]['Quarter']
    
def get_recession_bottom():
    '''Returns the year and quarter of the recession bottom time as a 
    string value in a format such as 2005q3'''
    rec_start = get_recession_start()
    rec_end = get_recession_end()
    gdp = pd.read_excel('gdplev.xls',skiprows=5).iloc[2:,[4,6]]
    gdp = gdp.rename(index = str, columns = {'Unnamed: 4':'Quarter',
                                                 'GDP in billions of chained 2009 dollars.1':'GDP (billions)'})
    gdp = gdp[(gdp.Quarter >= rec_start) & (gdp.Quarter <= rec_end)]
    return gdp.loc[gdp['GDP (billions)'].idxmin()]['Quarter']
    
def convert_housing_data_to_quarters():
    '''Converts the housing data to quarters and returns it as mean 
    values in a dataframe. This dataframe should be a dataframe with
    columns for 2000q1 through 2016q3, and should have a multi-index
    in the shape of ["State","RegionName"].
    
    Note: Quarters are defined in the assignment description, they are
    not arbitrary three month periods.
    
    The resulting dataframe should have 67 columns, and 10,730 rows.
    '''
    house_data = pd.read_csv('City_Zhvi_AllHomes.csv')
    for year in range(2000,2017) :
        for qrtr in range(1,5) :
            if (qrtr==4) and (year==2016) :
                break;

            quarter_col = '{0}q{1}'.format(year, qrtr)
            bmon = (qrtr-1)*3 + 1
            emon = qrtr*3
            begin_column = '{0}-{1:02d}'.format(year,bmon)
            end_column = '{0}-{1:02d}'.format(year,emon)

            if (qrtr==3) and (year==2016) :
                quarter_col = '{0}q{1}'.format(year, qrtr)
                bmon = (qrtr-1)*3 + 1
                emon = qrtr*3-1
                begin_column = '{0}-{1:02d}'.format(year,bmon)
                end_column = '{0}-{1:02d}'.format(year,emon)

            house_data[quarter_col] = house_data.loc[:,begin_column:end_column].mean(axis=1)


    house_data['State'] = house_data['State'].apply(lambda x: states[x])
    house_data.set_index(['State','RegionName'],inplace = True)
    house_data.drop(house_data.columns[0:249], axis=1, inplace=True)
    return house_data
    
    
def run_ttest():
    '''First creates new data showing the decline or growth of housing prices
    between the recession start and the recession bottom. Then runs a ttest
    comparing the university town values to the non-university towns values, 
    return whether the alternative hypothesis (that the two groups are the same)
    is true or not as well as the p-value of the confidence. 
    
    Return the tuple (different, p, better) where different=True if the t-test is
    True at a p<0.01 (we reject the null hypothesis), or different=False if 
    otherwise (we cannot reject the null hypothesis). The variable p should
    be equal to the exact p value returned from scipy.stats.ttest_ind(). The
    value for better should be either "university town" or "non-university town"
    depending on which has a lower mean price ratio (which is equivilent to a
    reduced market loss).'''
    rec_start = get_recession_start()
    rec_end = get_recession_end()
    house_data = convert_housing_data_to_quarters()
    uni_twn = get_list_of_university_towns()
    begin_recession = house_data[rec_start]
    end_recession = house_data[rec_end]
    house_data['price_ratio'] = begin_recession/end_recession
    uni_twn = uni_twn.set_index(['State', 'RegionName'])
    uni_twn_ratio = house_data.loc[list(uni_twn.index)]['price_ratio'].dropna()
    not_uni_twn_ratio_index = set(house_data.index) - set(uni_twn_ratio.index)
    not_uni_twn_ratio = house_data.loc[list(not_uni_twn_ratio_index),:]['price_ratio'].dropna()
    stat, p = tuple(ttest_ind(uni_twn_ratio, not_uni_twn_ratio))

    val = stat < 0
    
    different = p < 0.05
    
    better = ["non-university town", "university town"]
    
    return (different, p, better[val])
    
