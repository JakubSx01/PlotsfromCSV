import pandas as pd
import matplotlib.pyplot as plt
import os

def Tworzenie_Wykresow(df, csv_file_path, output_folder):
    csv_directory = os.path.dirname(csv_file_path)
    # Konwersja danych na liczbowe i usunięcie braków danych
    for i in df:
        df[i] = pd.to_numeric(df[i], errors='coerce')
    df = df.dropna()

    # Zmiana nazw kolumn (oprócz pierwszej)
    df.columns.values[0] = "t"
    for i, column_name in enumerate(df.columns[1:]):
        df.rename(columns={column_name: f"Ch{i+1}"}, inplace=True)

    # Obliczanie liczby podwykresów
    num_plots = len(df.columns) - 1


    # Rysowanie wykresów na podwykresach i zapisywanie do plików
    for i, column_name in enumerate(df.columns[1:]):
        # Tworzenie nowej figury dla każdego wykresu
        fig, ax = plt.subplots(figsize=(10, 6)) 

        ax.plot(df['t'], df[column_name], label=column_name, marker='o', markersize=1, linestyle='-')
        ax.set_xlabel('t [ms]')
        ax.set_ylabel('u [mV]')
        ax.set_title(f'{column_name}(t)')
        ax.grid(True, linestyle='--')
        ax.legend(loc='upper right')

        filename = os.path.join(output_folder, f"{column_name}(t).png")
        plt.savefig(filename)
        
        # Zamykanie figury po zapisaniu, aby zwolnić pamięć
        plt.close(fig)

    # Tworzenie figury z podwykresami dla zbiorczego wykresu
    fig, axs = plt.subplots(figsize=(10, 6))

    # Rysowanie wykresu zbiorczego i zapisywanie do pliku
    axs.plot(df['t'], df.drop(columns=['t']), marker='o', markersize=1, linestyle='-')
    axs.set_xlabel('t [ms]')
    axs.set_ylabel('u [mV]')
    axs.set_title('Wszystkie kanały')
    axs.grid(True, linestyle='--')
    axs.legend(df.columns[1:],loc='upper right')
    filename = os.path.join(output_folder, "Wszystkie kanały.png")
    plt.savefig(filename)
    plt.close()  # Zamknij ostatnią figurę
    excel_filename = os.path.join(output_folder, f"{os.path.splitext(os.path.basename(csv_file_path))[0]}.xlsx")
    df.to_excel(excel_filename, index=False)

def Odczyt_Zapis():
    script_directory = os.path.dirname(__file__)  # Get the directory of the script
    print(f'Searching for CSV files in: {script_directory}')

    # Initialize a list to store the output folder names
    output_folders = []

    for root, _, files in os.walk(script_directory):  # Search in the script's directory
        for file in files:
            if file.endswith('.csv'):
                csv_file_path = os.path.join(root, file)
                try:
                    df = pd.read_csv(csv_file_path)

                    # Data processing and renaming columns
                    df = df.apply(pd.to_numeric, errors='coerce').dropna()
                    df.columns = ["t"] + [f"Ch{i+1}" for i in range(len(df.columns) - 1)]

                    # Create output folder in the script's directory
                    csv_name = os.path.splitext(file)[0]
                    output_folder = os.path.join(script_directory, csv_name)  # Changed to script_directory
                    os.makedirs(output_folder, exist_ok=True)
                    output_folders.append(output_folder)  # Track the output folder

                    Tworzenie_Wykresow(df, csv_file_path, output_folder)
                except Exception as e:
                    print(f"Error processing {csv_file_path}: {e}")
    return output_folders

output_folders = Odczyt_Zapis()

# Check if any folders were created and print the message accordingly
if output_folders:
    print("Wykresy zostały zapisane w folderach:")
    for folder in output_folders:
        print(folder)
else:
    print("Nie znaleziono plików CSV do przetworzenia.")
