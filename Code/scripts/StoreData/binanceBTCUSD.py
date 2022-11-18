import csv
import datetime
import pandas as pd

data = dict({'Close': []})

def formatDate(date):
    return date.split('-')

# @param date yyyy-mm-dd
def getBTC1m(filename_base='BTCBUSD-1m-2022-00.csv'):
    #[startYear, startMonth, startDay] = formatDate(startDate)
    #[endYear, endMonth, endDay] = formatDate(startDate)
    #filename = filename_base
    for n in range(1,10):
        #filename[17] = str(n)
        with open(filename_base[0:-5]+str(n)+filename_base[-4:], 'r') as csvfile:
            reader = csv.reader(csvfile)
            # unix, date, symbol, open, high, low, close, Volume BTC ,Volume USD
            for row in reader:
                # skip first 2 rows as those are headers
                #row = row.split(",")
                data['Close'].append(row[1])
            
            #data['Date'].reverse()
            
            # print(data)
    
    #data['Close'].reverse()
    return pd.DataFrame.from_dict(data)

if __name__ == "__main__":
    print(getBTC1m())
    """data = getBTC1h('2022-10-01','2022-10-26', filename='scripts/StoreData/Bitstamp_BTCUSD_1h.csv')
    print(data)
    data_indicator = data[data.index % 24 == 0]  # Selects every 3rd raw starting from 0
    data_indicator = data_indicator.reset_index()
    print(data_indicator)
    for index, row in data_indicator.iterrows():
        #print(row['c1'], row['c2'])
        if index > 14:# and index < 16:
            data_indicator_current = data_indicator.copy(deep=True)
            data_indicator_current = data_indicator_current.iloc[index-13:index+1]
            print(data_indicator_current)
            #print(data)
            for i in range(24):
                if index*24+i+1 < data.shape[0]:
                    price = data[index*24+i:index*24+i+1]["Date"]
                    print(price)"""