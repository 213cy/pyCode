import requests
import pandas as pd

myprefix = 1
def stock_zh_a_hist(
    symbol: str = "000001",
    period: str = "daily",
    start_date: str = "19700101",
    end_date: str = "20500101",
    adjust: str = "",
) -> pd.DataFrame:
    """
    东方财富网-行情首页-沪深京 A 股-每日行情
    http://quote.eastmoney.com/concept/sh603777.html?from=classic
    :param symbol: 股票代码
    :type symbol: str
    :param period: choice of {'daily', 'weekly', 'monthly'}
    :type period: str
    :param start_date: 开始日期
    :type start_date: str
    :param end_date: 结束日期
    :type end_date: str
    :param adjust: choice of {"qfq": "前复权", "hfq": "后复权", "": "不复权"}
    :type adjust: str
    :return: 每日行情
    :rtype: pandas.DataFrame
    """

    adjust_dict = {"qfq": "1", "hfq": "2", "": "0"}
    period_dict = {"daily": "101", "weekly": "102", "monthly": "103"}
    url = "http://push2his.eastmoney.com/api/qt/stock/kline/get"
    params = {
        "fields1": "f1,f2,f3,f4,f5,f6",
        "fields2": "f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61,f116",
        "ut": "7eea3edcaed734bea9cbfc24409ed989",
        "klt": period_dict[period],
        "fqt": adjust_dict[adjust],
        "secid": f"{myprefix}.{symbol}",
        "beg": start_date,
        "end": end_date,
        "_": "1623766962675",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    if not (data_json["data"] and data_json["data"]["klines"]):
        return pd.DataFrame()
    temp_df = pd.DataFrame(
        [item.split(",") for item in data_json["data"]["klines"]]
    )

    temp_df[0] = pd.to_datetime(temp_df[0])

    for k in temp_df.columns[1:] :
         temp_df[k] = pd.to_numeric(temp_df[k])
         
    temp_df.columns = [
        'date', #"日期",
        'open', #"开盘",
        'close', #"收盘",
        'high', #"最高",
        'low', #"最低",
        'volume', #"成交量",
        'amount', # 'sum' "成交额",
        "振幅",
        'change_percent', #"涨跌幅",
        'change', #"涨跌额",
        "换手率",
    ]


##    temp_df["开盘"] = pd.to_numeric(temp_df["开盘"])
##    temp_df["收盘"] = pd.to_numeric(temp_df["收盘"])
##    temp_df["最高"] = pd.to_numeric(temp_df["最高"])
##    temp_df["最低"] = pd.to_numeric(temp_df["最低"])
##    temp_df["成交量"] = pd.to_numeric(temp_df["成交量"])
##    temp_df["成交额"] = pd.to_numeric(temp_df["成交额"])
##    temp_df["振幅"] = pd.to_numeric(temp_df["振幅"])
##    temp_df["涨跌幅"] = pd.to_numeric(temp_df["涨跌幅"])
##    temp_df["涨跌额"] = pd.to_numeric(temp_df["涨跌额"])
##    temp_df["换手率"] = pd.to_numeric(temp_df["换手率"])

    return temp_df


#raise SystemExit



'''HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH'''


'''HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH'''
