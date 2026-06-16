import pandas as pd
from mlxtend.frequent_patterns import fpgrowth, association_rules


# this is a surprise tool that will help us later
def get_season(date):
    month = date.month
    if month in [12, 1, 2]:
        return "Winter"
    elif month in [3, 4, 5]:
        return "Spring"
    elif month in [6, 7, 8]:
        return "Summer"
    else:
        return "Fall"


def main():

    columns = ["TransactionNo", "Items", "DateTime", "Daypart", "DayType"]

    # loading
    data = pd.read_csv(r"C:\Users\theco\Downloads\Bakery.csv", header=None, names=columns)

    # one-hot encoding on items
    binary_items = pd.get_dummies(data["Items"])
    data = pd.concat([data, binary_items], axis=1)

    # original Items column isn't useful anymore
    data = data.drop(columns=["Items"])

    # changing rows to be grouped by transaction number
    data = data.groupby(["TransactionNo", "DateTime", "Daypart", "DayType"]).max().reset_index()

    # TransactionNo is also useless now
    data = data.drop(columns=["TransactionNo"])

    # the last row of the database is recording column name for some reason
    data = data.drop(index=len(data) - 1)

    # binning datetime into seasons
    data["DateTime"] = pd.to_datetime(data["DateTime"])
    # here's that get_season function
    data["Season"] = data["DateTime"].apply(get_season)

    # and just like before, the original column is no longer useful
    data = data.drop(columns=["DateTime"])

    # now we do one-hot encoding on all the date/time stuff
    binary_days = pd.get_dummies(data[["DayType", "Daypart", "Season"]])
    data = pd.concat([data, binary_days], axis=1)

    # I think you know the deal by now, date/time columns aren't needed
    data = data.drop(columns=["Daypart", "DayType", "Season"])


    # FP-Growth

    frequent_itemsets = fpgrowth(data, min_support=0.01, use_colnames=True)

    rules = association_rules(frequent_itemsets, metric='lift', min_threshold=0)

    # this is so we don't get rules like "if it's a weekday, 35% of the time it's afternoon"
    # like yeah, no shit
    excluded_columns = ["DayType_Weekday", "DayType_Weekend", "Daypart_Afternoon", "Daypart_Evening", "Daypart_Morning", "Daypart_Night", "Season_Fall", "Season_Winter", "Season_Spring", "Season_Summer"]
    rules = rules[~rules["consequents"].apply(lambda x: any(item in excluded_columns for item in x))]

    # this is only for printing purposes (so we can choose what statistic to see instead of only seeing kulczynski)
    criteria = 'lift'  # the metric to sort by and print
    show = 50  # the number of rules to show

    # there are two print statements so that if lift is the metric (which it usually is) I can see both extremes
    print(rules[["antecedents", "consequents", "support", criteria]].sort_values(by=criteria, ascending=False).head(show).to_string())
    print(rules[["antecedents", "consequents", "support", criteria]].sort_values(by=criteria, ascending=True).head(show).to_string())

    rules.to_csv(r'D:\Desktop\CSULB\CECS 456\output.csv', index=False, header=True)


main()
