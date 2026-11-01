"""Google Trends CSV to the two numbers the last slide needs.

Usage: python3 search_change.py <time_series_*.csv>
Prints the average weekly score per calendar year present in the file and
the % change, plus a first-half vs second-half split. A standard 12-month
export only holds ~13 weeks of the earlier year, so say exactly which
periods the bars compare ("Oct to Dec 2025" vs "Jan to Oct 2026"), never
"last year vs this year" as if they were full years. Round to whole numbers.
"""
import csv, sys
rows = list(csv.reader(open(sys.argv[1])))
hdr = next(i for i, r in enumerate(rows) if r and r[0] in ('Time', 'Week', 'Day', 'Month'))
term = rows[hdr][1]
d = [(r[0], int(r[1].replace('<1', '0'))) for r in rows[hdr + 1:] if len(r) > 1 and r[1]]
years = sorted({t[:4] for t, _ in d})
avg = {y: [v for t, v in d if t.startswith(y)] for y in years}
for y in years:
    print(f'{y}: {len(avg[y])} weeks, {d[[t[:4] for t,_ in d].index(y)][0]} onward, avg {sum(avg[y])/len(avg[y]):.1f}')
if len(years) == 2:
    a, b = (sum(avg[y]) / len(avg[y]) for y in years)
    print(f'"{term}": {years[0]} avg {round(a)} vs {years[1]} avg {round(b)} = {round((b / a - 1) * 100):+d}%')
h = len(d) // 2
a, b = sum(v for _, v in d[:h]) / h, sum(v for _, v in d[h:]) / (len(d) - h)
print(f'first {h} weeks avg {round(a)} vs last {len(d)-h} avg {round(b)} = {round((b / a - 1) * 100):+d}%')
print('peak', max(d, key=lambda x: x[1]))
