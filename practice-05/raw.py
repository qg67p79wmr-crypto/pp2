with open("Practice05/raw.txt", "r", encoding="utf-8") as file:
    text = file.read()

lines = text.split("\n")

for i in range(len(lines)):
    line = lines[i]

    if "БИН" in line:
        print("БИН:", line.replace("БИН", "").strip())

    if "Чек №" in line:
        print("Номер чека:", line.replace("Чек №", "").strip())

    if "ИТОГО:" in line:
        print("Итого:", lines[i + 1].strip())

    if "Время:" in line:
        print("Время:", line.replace("Время:", "").strip())

    if "г. Нур-султан" in line:
        print("Адрес:", line.strip())