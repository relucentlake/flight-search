# flight-search
A script for finding all round-trip flights within a date window and a variable stay length in Aviasales.

**Example input:**  
token = "your token"  
origin = "MOW"  
destination = "TAS"  
start = date(2025, 9, 1)  
end = date(2025, 9, 30)  
min_stay = 3  
max_stay = 10  
currency = "rub"  

**Example output:**  
21752 RUB  2025-09-24 - 2025-09-29  stay: 5d  C6  transfers: 0  
21793 RUB  2025-09-21 - 2025-09-27  stay: 6d  U6  transfers: 0  
21922 RUB  2025-09-23 - 2025-09-26  stay: 3d  DP  transfers: 0  
21930 RUB  2025-09-23 - 2025-09-28  stay: 5d  DP  transfers: 1  
21934 RUB  2025-09-25 - 2025-09-28  stay: 3d  DP  transfers: 0  
21962 RUB  2025-09-21 - 2025-09-24  stay: 3d  U6  transfers: 0  
22129 RUB  2025-09-21 - 2025-09-28  stay: 7d  HH  transfers: 0
