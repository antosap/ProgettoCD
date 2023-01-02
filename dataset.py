# import random
#
# # Apri il file di output in modalità di scrittura
# with open("Dataset1.txt", "w") as f:
#   # Genera 1000 righe di stringhe casuali
#   for _ in range(3000):
#     # Genera una stringa casuale di lunghezza 10
#     s = ''.join(random.choices(['G', 'A', 'T', 'C'], k=24))
#     # Scrivi la stringa nel file di output, aggiungendo un a capo alla fine
#     f.write(s + "\n")
#

#
# def check_duplicate_lines(filename):
#   # Apri il file in modalità di lettura
#   with open(filename, "r") as file:
#     # Crea una lista delle righe del file
#     lines = file.readlines()
#
#   # Crea un set per memorizzare le righe uniche
#   unique_lines = set()
#
#   # Itera su ogni riga del file
#   for line in lines:
#     # Rimuovi gli spazi vuoti all'inizio e alla fine della riga
#     line = line.strip()
#
#     # Se la riga è già presente nel set, significa che è una riga duplicata
#     if line in unique_lines:
#       return True
#
#     # Altrimenti, aggiungi la riga al set
#     unique_lines.add(line)
#
#   # Se il ciclo è terminato e non è stato trovata alcuna riga duplicata, significa che il file non ha righe duplicate
#   return False
#
# # Esempio di utilizzo
# duplicate_found = check_duplicate_lines("Dataset4.txt")
# if duplicate_found:
#   print("Il file ha righe duplicate")
# else:
#   print("Il file non ha righe duplicate")
