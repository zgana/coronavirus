
import numpy as np
import pandas as pd


def get_state_data(pop, state_name_mapping):
    print('Downloading state-level data from covidtracking.com ...')

    x = pd.read_html('https://docs.google.com/spreadsheets/u/2/d/e/'
                     '2PACX-1vRwAqp96T9sYYq2-i7Tj0pvTf6XVHjDSMIKBdZHXiCGGdNC0ypEU9NbngS8mxea55JuCFuua1MUeOj5'
                     '/pubhtml', skiprows=1, index_col=0)
    states = x[3][[
        'Date',
        'State',
        'Positive',
        'Negative',
        'Pending',
        'Recovered',
        'Deaths',
        'Data Quality Grade',
    ]]
    states = states[~states.Date.isna()]
    states = states.sort_values('Date State'.split(), ascending=True).reset_index(drop=True)
    states['Date'] = pd.to_datetime(states.Date.astype(str), format='%Y%m%d')
    states['datestr'] = states['Date'].astype(str)
    states['days'] = states.Date.map({d:i for (i,d) in enumerate(np.unique(states.Date.values))})

    # reorder and rename columns
    data = states[[
        'Date',
        'State',
        'Deaths',
        'Positive',
        'Negative',
        'Recovered',
        'Data Quality Grade',
        'datestr',
        'days',
    ]]
    data.columns = [
        'date',
        'state',
        'deaths',
        'positives',
        'negatives',
        'recoveries',
        'data_quality',
        'datestr',
        'days',
    ]

    # set up pop data for state-level
    pop = pop[pop.fips_county.eq(0)]
    pop = pop['state_name population land_area population_density population_weighted_density'.split()]
    pop = pop.merge(state_name_mapping, on='state_name')

    data = data.merge(pop, on='state')

    return data

def get_county_data(pop):

    print('Downloading county-level data from NYTimes github ...')

    data = pd.read_csv('https://github.com/nytimes/covid-19-data/blob/master/us-counties.csv?raw=true')

    # won't try to join data without fips code
    data = data[~data.fips.isna()]

    data['fips'] = data.fips.astype(int)
    data['datestr'] = data.date.astype(str)
    data['date'] = pd.to_datetime(data.date)
    data['days'] = data.date.map({d:i for (i,d) in enumerate(np.unique(data.date.values))})

    data = data.rename(columns={'cases':'positives', 'county':'county_name', 'state':'state_name'})
    data = data[[
        'date',
        'state_name',
        'county_name',
        'fips',
        'deaths',
        'positives',
        'datestr',
        'days',
    ]]

    pop = pop[pop.fips_county.ne(0)]
    pop = pop['fips population land_area population_density'.split()]
    data = data.merge(pop, on='fips')

    return data


state_name_mapping = pd.read_csv('data/geo/state_name_mapping.csv')
pop = pd.read_csv('data/pop/pop-estimates-2019.csv')

data = get_state_data(pop, state_name_mapping)
outfile = 'data/latest/covid19-latest-state.csv'
print(f'Writing {outfile} ...')
data.to_csv(outfile, index=False)

data = get_county_data(pop)
outfile = 'data/latest/covid19-latest-county.csv'
print(f'Writing {outfile} ...')
data.to_csv(outfile, index=False)
