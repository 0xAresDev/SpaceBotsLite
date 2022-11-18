import csv
import datetime
import pandas as pd

data = dict({'Date': [], 'Close': []})

def formatDate(date):
    return date.split('-')

# @param date yyyy-mm-dd
def getBTC1h(startDate, endDate, filename='Bitstamp_BTCUSD_1h.csv'):
    [startYear, startMonth, startDay] = formatDate(startDate)
    [endYear, endMonth, endDay] = formatDate(startDate)
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        # unix, date, symbol, open, high, low, close, Volume BTC ,Volume USD
        for row in reader:
            # skip first 2 rows as those are headers
            if len(row) == 9 and row[0].isdigit():
                [currYear, currMon, day] = row[1].split('-')
                currDay = day.split(' ')[0]
                startDate = datetime.datetime(int(startYear),int(startMonth),int(startDay))
                currDate = datetime.datetime(int(currYear),int(currMon),int(currDay))
                test = currDate - startDate
                # get date of current row. If reached startDate, break loop
                toEnd = (currDate - startDate).days < 0
                
                if toEnd:
                    break
                else:
                    for i in range(0,9): # 9 columns
                        if (i == 1):
                            data['Date'].append(row[1])
                        elif (i == 6):
                            data['Close'].append(row[6])
        
        data['Date'].reverse()
        data['Close'].reverse()
        # print(data)
    
    return pd.DataFrame.from_dict(data)

if __name__ == "__main__":
    data = getBTC1h('2022-10-01','2022-10-26', filename='scripts/StoreData/Bitstamp_BTCUSD_1h.csv')
    print(data)
    data_indicator = data[data.index % 24 == 0]  # Selects every 3rd raw starting from 0
    data_indicator = data_indicator.reset_index()
    print(data_indicator)
    for index, row in data_indicator.iterrows():
        #print(row['c1'], row['c2'])
        if index > 14:# and index < 16:
            data_indicator_current = data_indicator.copy(deep=True)
            data_indicator_current = data_indicator_current.iloc[index-13:index+1]
            """for i in range(24):
                data_indicator_current = data_indicator.copy(deep=True)
                data_indicator_current = data_indicator_current.iloc[index-14:index]
                print(data_indicator_current)"""
            print(data_indicator_current)
            #print(data)
            for i in range(24):
                if index*24+i+1 < data.shape[0]:
                    price = data[index*24+i:index*24+i+1]["Date"]
                    print(price)