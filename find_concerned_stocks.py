# toolkit for caculate annual percentage yield of cash secured short put strategy
from futu import OpenQuoteContext, RET_OK, OptionType, OptionCondType, set_futu_debug_model
from datetime import datetime, timedelta, timezone
import sys

set_futu_debug_model(False)

TIMEZONE_OFFSET = timedelta(hours = -12) # North American Eastern Time Zone, known as ET (EDT is UTC-4, EST is UTC-5)
quote_ctx = OpenQuoteContext(host = '127.0.0.1', port = 11111)

group_name = sys.argv[1]
ret_code, stocks = quote_ctx.get_user_security(group_name)
if ret_code != RET_OK:
    print("get_user_security, ret_code: %s, error: %s" % (ret_code, stocks))
    sys.exit()

#print(stocks)
for i, stock in stocks.iterrows():
    code = stock["code"]
    name = stock["name"]
    print(code, name)

quote_ctx.close()