import tkinter as tk
import pandas as pd

class Application(tk.Frame):
    def __init__(self, master=None, csv_file='sve-dict.csv'):
        #Initierar tk frame:n
        tk.Frame.__init__(self, master)

        #Hämtar lexikonet med alla svenska ord formaterat i en csv-fil
        self.df = pd.read_csv(csv_file)
        self.dict_results = []
        self.results_to_save = []

        #Hämtar index i index-filen
        with open('index.txt') as file:
            self.index = int(file.read())
        self.words_left_string = tk.StringVar()
        self.words_left_string.set(f'{self.index}/24 261 ({(self.index/24216)*100:.2f}%)')

        self.word_from_dict = tk.StringVar()
        self.word_from_dict.set(self.df.iloc[self.index][1])

        self.grid()
        self.createWidgets()

        #Bindar knapparna till tangentbordet
        self.focus_set()
        self.bind('<Right>', self.positive)
        self.bind('<Left>', self.negative)
        self.bind('<Up>', self.neutral)


    def createWidgets(self):
        #Skapar widgetsarna
        self.word_to_assess = tk.Label(self, textvariable=self.word_from_dict, borderwidth=30, font=('Courier', 22), width=20)

        self.positive_button = tk.Button(self, text='Positiv', bg='#000fff000', width=15, command=self.positive)
        self.neutral_button = tk.Button(self, text='Neutral', bg='darkgrey', height=3, width=15, command=self.neutral)
        self.negative_button = tk.Button(self, text='Negativ', bg='red', width=15, command=self.negative)
        self.save_button = tk.Button(self, text='Spara', bg='darkgrey', width=30, command=self.save_dataframe)

        self.words_left_label = tk.Label(self, textvariable=self.words_left_string, font=('Courier', 10))

        #Placerar ut widgetsarna på griden.
        self.word_to_assess.grid(column=0, row=1, columnspan=3)

        self.positive_button.grid(column=2, row=2)
        self.neutral_button.grid(column=1, row=2)
        self.negative_button.grid(column=0, row=2)
        self.save_button.grid(row=3, columnspan=3, pady=10)

        self.words_left_label.grid(row=0, columnspan=3, sticky='W')

    def positive(self, event=None):
        print('Positivt ord')
        self.next_word(self.word_from_dict.get(), 'positivt')

    def negative(self, event=None):
        print('Negativt ord')
        self.next_word(self.word_from_dict.get(), 'negativt')

    def neutral(self, event=None):
        print('Neutralt ord')
        self.next_word(self.word_from_dict.get(), 'neutralt')

    def next_word(self, word, assessment):
        self.dict_results.append({'word': word, 'assessment': assessment})

        self.index += 1
        self.word_from_dict.set(self.df.iloc[self.index][1])
        self.words_left_string.set(f'{self.index}/24 261 ({(self.index/24216)*100:.2f}%)')

    def save_dataframe(self):
        print('Sparar dataframe')

        #Öppnar tidigare resultaten och kombinerar de med de nya
        self.old_df = pd.read_csv('sve-dict-assessed.csv')
        self.old_list_of_dicts = self.old_df.to_dict(orient='records')

        self.results_to_save = self.old_list_of_dicts + self.dict_results

        #Sparar dataframen i ett .csv
        self.df_results = pd.DataFrame(data=self.results_to_save, columns=['word', 'assessment'])

        self.df_results.to_csv('sve-dict-assessed.csv', index=False)
        print('vi klarade att spara df')


        #Spara index i en .txt-fil
        with open('index.txt', 'w') as file:
            file.write(str(self.index))
        print('vi klarade index saven, index: ' + str(self.index))


app = Application()
app.master.title('Dictionary Assesser')
print(app.winfo_height)
print(app.winfo_width)


app.mainloop()