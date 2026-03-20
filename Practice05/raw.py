import re

with open("raw.txt", "r", encoding="utf-8") as file:
    text = file.read()

bin_match = re.search(r"БИН\s+(\d+)", text)
check_match = re.search(r"Чек №(\d+)", text)
time_match = re.search(r"Время:\s*([\d.: ]+)", text)
total_match = re.search(r"ИТОГО:\s*\n([\d ]+,\d+)", text)
payment_match = re.search(r"Банковская карта:\s*\n([\d ]+,\d+)", text)

print("BIN:", bin_match.group(1) if bin_match else "Not found")
print("Check number:", check_match.group(1) if check_match else "Not found")
print("Time:", time_match.group(1) if time_match else "Not found")
print("Total:", total_match.group(1) if total_match else "Not found")
print("Paid by card:", payment_match.group(1) if payment_match else "Not found")