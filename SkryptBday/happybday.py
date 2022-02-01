import pyautogui 

#print(pyautogui.position())

pyautogui.moveTo(471,1045,1)
pyautogui.click()

file = open("wishes.txt", "r", encoding = "utf-8")

for line in file:
    line = line.strip()
    if len(line) > 0:
        pyautogui.write(line)
        pyautogui.press("enter")
