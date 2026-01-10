import pandas as pd
import random
from concurrent.futures import ProcessPoolExecutor as Pool

words = ['A', 'B', 'C', 'D']

def generate_csv_files(filename, size, count_rows):
    data = []
    for index in range(size):
        for i in range(count_rows):
            number_word = random.randint(0, 3)
            number_float = round(random.uniform(0.0, 10.0), 3)
            data.append({
                'Категория': words[number_word],
                'Значение': number_float
            })
        df = pd.DataFrame(data)
        df.to_csv(f"{filename}_{index}.csv", index=False)

def process_single_file(args):
    filename, index = args
    data = []
    df = pd.read_csv(f"{filename}_{index}.csv")
    for word in words:
        value = df[df['Категория'] == word]['Значение']
        if not value.empty:
            med = value.median()
            std = value.std()
            std = 0.0 if pd.isna(std) else std
            data.append({
                'Категория': word,
                'Медиана': round(med, 3),
                'Отклонение': round(std, 3)
            })
    df_new = pd.DataFrame(data)
    df_new.to_csv(f"{filename}_first_processing_{index}.csv", index=False)

def get_median_std(filename, size):
    with Pool() as executor:
        executor.map(process_single_file, [(filename, i) for i in range(size)])

def get_total_processing_file(filename, size):
    dict_info = {}
    for word in words:
        dict_info[word] = []
    for index in range(size):
        df = pd.read_csv(f"{filename}_first_processing_{index}.csv")
        for word in words:
            value = df[df["Категория"] == word]["Медиана"]
            if not value.empty:
                dict_info[word].append(value.values[0])
    total_dict = []
    for word in words:
        med_std = dict_info[word]
        total_dict.append({
            "Категория": word,
            "Медиана медиан": round(pd.Series(med_std).median(), 3),
            "Медиана отклонений": round(pd.Series(med_std).std(), 3)
        })
    total_df = pd.DataFrame(total_dict)
    total_df.to_csv(f"{filename}_total_processing.csv", index=False)

if __name__ == "__main__":
    generate_csv_files("filename", 5, 15)
    get_median_std("filename", 5)
    get_total_processing_file("filename", 5)

