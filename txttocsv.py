import csv
import pandas as pd


with open('sve-dict.txt') as file:
    full_text = file.read()


full_text_list = full_text.split()

df = pd.DataFrame(data=full_text_list, columns=['ord'])
df.to_csv('sve-dict.csv')