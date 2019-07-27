# toolkit for caculate annual percentage yield of cash secured short put strategy
from futu import OpenQuoteContext, RET_OK, OptionType, OptionCondType, set_futu_debug_model
from datetime import datetime, timedelta, timezone
import sys, os, time, math

set_futu_debug_model(False)

TIMEZONE_OFFSET = timedelta(hours = -12) # North American Eastern Time Zone, known as ET (EDT is UTC-4, EST is UTC-5)
quote_ctx = OpenQuoteContext(host = '127.0.0.1', port = 11111)

options_codes = sys.argv[1].split(',')

# get snapshots and caculate APY
stock_price = 0
sort_options = []
page_size = 300 # futu api level2 limit
now = datetime.now() + TIMEZONE_OFFSET
today = datetime(now.year, now.month, now.day)
page_options_codes = []

while len(options_codes) > 0:
    page_options_codes.append(options_codes.pop(0))
    if len(page_options_codes) == page_size or len(options_codes) == 0: # full pagination or last page
        while True: # insure this pagination request processing successfully
            ret_code, snapshots = quote_ctx.get_market_snapshot(page_options_codes)
            if ret_code != RET_OK:
                print("get_market_snapshot, ret_code: %s, error: %s" % (ret_code, snapshots))
                time.sleep(1.5) # error before maybe because of futu api level2 limit, 20 snapshots requests per 30s
                continue

            page_options_codes.clear()
            for i, snapshot in snapshots.iterrows(): # here each row is a tuple
                if snapshot["option_valid"] == False:
                    stock_price = snapshot["last_price"]
                    continue
                price = snapshot["bid_price"]
                strike_time = snapshot["strike_time"]
                strike_price = snapshot["option_strike_price"]
                contract_size = snapshot["option_contract_size"]
                days = (datetime.strptime(strike_time, '%Y-%m-%d') - today).days + 1
                option = {}
                option["code"] = snapshot.code
                option["strike_time"] = strike_time
                option["strike_price"] = strike_price
                option["stock_price"] = stock_price
                option["apy"] = (price * contract_size - 2) / days * 365 / (strike_price * contract_size ) * 100 # Annual Percentage Yield, handing fee is about 2 dollar
                option["out"] = abs(stock_price - strike_price) / stock_price * 100
                option["price"] = price
                option["oi"] = snapshot["option_open_interest"]
                option["iv"] = snapshot["option_implied_volatility"]
                option["premium"] = snapshot["option_premium"]
                option["delta"] = snapshot["option_delta"]
                option["volume"] = snapshot["volume"]
                sort_options.append(option)
            break

# sort options snapshots
def getSortKey(ele):
    return ele["apy"] # sort desc by APY

sort_options.sort(reverse = True, key = getSortKey)
for o in sort_options:
    print(o["code"], "%.2f" % o["apy"], o["price"], "%.0f" % o["oi"], "%.2f%%" % o["iv"], "%.2f" % o["premium"], o["delta"], o["stock_price"], "%.2f" % o["out"], o["volume"])

quote_ctx.close()