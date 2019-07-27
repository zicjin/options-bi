抓关注股的期权代码清单
time python3 find_concerned_stocks.py active | awk '/^US/{print $1}' | while read line; do start=$(echo "`gdate +%s.%3N`" | bc); python3 find_options.py $line all; s=$(echo "3 - (`gdate +%s.%3N` - $start)" | bc); if [ $s > 0 ] ; then sleep $s;  fi;  done |  awk '/^US/' > options_codes.active.txt

抓期权具体信息
time cat options_codes.active.txt  | while read line; do python3 find_snapshots.py $line all; done | awk '/^US/' > concerned_stocks_options.active.txt

过滤和输出
cat concerned_stocks_options.active.txt  | sort -k 2 -r -n | awk -F'[1,2]' '{print $0, $1}' | awk 'function abs(x){return ((x < 0.0) ? -x : x)};$2>50 && $4>0 && $6 > 8 && $9 > 8 && abs($7) > 0 && abs($7) < 0.4'  | awk 'BEGIN{printf "%-22s%-10s%-10s%-10s%-10s%-10s%-10s%-10s%-10s%-10s\n", "code", "sell_apy", "premium", "out", "price", "op_buy", "volume", "oi", "iv", "delta"}{printf "%-22s%-10s%-10s%-10s%-10s%-10s%-10s%-10s%-10s%-10s\n", $1, $2"%", $6"%", $9"%", "$"$8, "$"$3,  $10,  $4,  $5,  $7}'

合并最后两步
time cat options_codes.active.txt  | while read line; do python3 find_snapshots.py $line all; done | awk '/^US/'   | sort -k 2 -r -n | awk -F'[1,2]' '{print $0, $1}' | awk 'function abs(x){return ((x < 0.0) ? -x : x)};$2>50 && $4>0 && $6 > 8 && $9 > 8 && abs($7) > 0 && abs($7) < 0.4'  | awk 'BEGIN{printf "%-22s%-10s%-10s%-10s%-10s%-10s%-10s%-10s%-10s%-10s\n", "code", "sell_apy", "premium", "out", "price", "op_buy", "volume", "oi", "iv", "delta"}{printf "%-22s%-10s%-10s%-10s%-10s%-10s%-10s%-10s%-10s%-10s\n", $1, $2"%", $6"%", $9"%", "$"$8, "$"$3,  $10,  $4,  $5,  $7}'