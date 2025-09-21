import requests
from datetime import date, datetime
from itertools import product

token = "your token"
origin = "MOW"
destination = "TAS"
start = date(2025, 9, 1)
end = date(2025, 9, 30)
min_stay = 3
max_stay = 10
currency = "rub"

url = "https://api.travelpayouts.com/aviasales/v3/prices_for_dates"

def months_between(start, end):
    months = []
    y, m = start.year, start.month
    while (y, m) <= (end.year, end.month):
        months.append(f"{y:04d}-{m:02d}")
        m += 1
        if m == 13:
            y, m = y + 1, 1
    return months

def fetch_month_pair(dep_month, ret_month):
    params = {
        "origin": origin,
        "destination": destination,
        "departure_at": dep_month,
        "return_at": ret_month,
        "one_way": "false",
        "sorting": "price",
        "limit": 1000,
        "cy": currency,
        "token": token,
    }
    r = requests.get(url, params=params, headers={"Accept-Encoding": "gzip, deflate"})
    r.raise_for_status()
    js = r.json()
    if not js.get("success", False):
        raise RuntimeError(js.get("error") or "some error")
    return js.get("data", [])

def to_date(iso) -> date:
    return datetime.fromisoformat(iso.replace("Z", "")).date()

def within_window(d) -> bool:
    return start <= d <= end

def stay_days(dep_iso: str, ret_iso: str) -> int:
    dep_d, ret_d = to_date(dep_iso), to_date(ret_iso)
    return (ret_d - dep_d).days

def main():
    months = months_between(start, end)
    seen = set()
    results = []

    for dep_m, ret_m in product(months, months):
        for f in fetch_month_pair(dep_m, ret_m):
            dep_d = to_date(f["departure_at"])
            ret_d = to_date(f["return_at"])
            if not (within_window(dep_d) and within_window(ret_d)):
                continue

            stay = (ret_d - dep_d).days
            if stay < 0:
                continue
            if not (min_stay <= stay <= max_stay):
                continue

            key = (f.get("airline"), f.get("price"), dep_d, ret_d, f.get("link"))
            if key in seen:
                continue
            seen.add(key)

            results.append({
                "price": f.get("price"),
                "currency": currency.upper(),
                # "airline": f.get("airline"),
                # "flight_number": f.get("flight_number"),
                "departure_at": f["departure_at"],
                "return_at": f["return_at"],
                "stay_days": stay,
                "duration": f.get("duration"),
                "transfers": f.get("transfers"),
            })

    for row in results:
        print("{price:>6} {currency}  {dep} - {ret}  stay: {stay}d  transfers: {transfers}".format(
            price=row["price"], currency=row["currency"],
            dep=row["departure_at"][:10], ret=row["return_at"][:10],
            stay=row["stay_days"], transfers=row["transfers"]))
    # import csv
    # with open("aviasales_roundtrips_with_stay.csv", "w", newline="", encoding="utf-8") as f:
    #     w = csv.DictWriter(f, fieldnames=results[0].keys())
    #     w.writeheader(); w.writerows(results)

if __name__ == "__main__":
    main()
