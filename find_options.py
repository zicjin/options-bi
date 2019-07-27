# toolkit for caculate annual percentage yield of cash secured short put strategy
from futu import OpenQuoteContext, RET_OK, OptionType, OptionCondType, set_futu_debug_model
from datetime import datetime, timedelta, timezone
import sys, os, time

set_futu_debug_model(False)

TIMEZONE_OFFSET = timedelta(hours = -12) # North American Eastern Time Zone, known as ET (EDT is UTC-4, EST is UTC-5)
quote_ctx = OpenQuoteContext(host = '127.0.0.1', port = 11111)
stock_code = sys.argv[1]
option_type = sys.argv[2]
if option_type == 'p':
    option_type = OptionType.PUT
elif option_type == 'c':
    option_type = OptionType.CALL
else:
    option_type = OptionType.ALL

start = None
end = None
if len(sys.argv) >= 4 and sys.argv[3] == 'last':
    now = datetime.now() + TIMEZONE_OFFSET
    start_time = datetime(now.year, now.month, now.day)
    start = start_time.strftime("%Y-%m-%d")
    end_time = start_time + timedelta(days = 7)
    end = end_time.strftime("%Y-%m-%d")



# get options codes of this stock
while True:
    ret_code, options = quote_ctx.get_option_chain(stock_code, start, end, option_type, OptionCondType.OUTSIDE)
    if ret_code != RET_OK: # error maybe because of futu api level2 limit, 10 options requests per 30s
        print("get_option_chain of %s, ret_code: %s, error: %s" % (stock_code, ret_code, options))
        time.sleep(1)
        continue
    break
if options.size == 0:
    os._exit(0)   
options_codes = [stock_code]
for i, row in options.iterrows(): # here row is a tuple
    options_codes.append(row['code'])

print(','.join(options_codes))

quote_ctx.close()