import os
import json
from tkinter import Tk, filedialog, messagebox

def select_folder(title):
    """Abre un cuadro de diálogo para seleccionar una carpeta."""
    return filedialog.askdirectory(title=title)

def merge_stats(stats1, stats2):
    """Combina las estadísticas de dos estructuras JSON."""
    merged_stats = stats1.copy()
    
    for category, substats in stats2.items():
        if category not in merged_stats:
            merged_stats[category] = substats
        else:
            for key, value in substats.items():
                if key in merged_stats[category]:
                    merged_stats[category][key] += value
                else:
                    merged_stats[category][key] = value

    return merged_stats

def merge_json_files(file1, file2):
    """Combina los contenidos de dos archivos JSON, sumando las estadísticas."""
    try:
        with open(file1, 'r') as f1, open(file2, 'r') as f2:
            data1 = json.load(f1)
            data2 = json.load(f2)
        
        # Combinar `stats`
        merged_data = {
            "stats": merge_stats(data1.get("stats", {}), data2.get("stats", {})),
            "DataVersion": max(data1.get("DataVersion", 0), data2.get("DataVersion", 0)),
        }

        return merged_data
    except json.JSONDecodeError as e:
        print(f"Error al leer JSON: {e}")
        return None

def process_folders(folder1, folder2, output_folder):
    """Procesa las carpetas y mezcla archivos JSON con el mismo nombre."""
    if not os.path.exists(folder1) or not os.path.exists(folder2):
        messagebox.showerror("Error", "Una de las carpetas seleccionadas no existe.")
        return

    # Crear carpeta de salida si no existe
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(folder1):
        file1_path = os.path.join(folder1, filename)
        file2_path = os.path.join(folder2, filename)
        output_path = os.path.join(output_folder, filename)

        if os.path.isfile(file1_path) and os.path.isfile(file2_path):
            if filename.endswith('.json'):
                merged_data = merge_json_files(file1_path, file2_path)
                if merged_data is not None:
                    with open(output_path, 'w') as output_file:
                        json.dump(merged_data, output_file, indent=4)
                        print(f"Archivo combinado guardado: {output_path}")
            else:
                print(f"Se encontró un archivo no JSON con el mismo nombre: {filename}")
        else:
            # Si el archivo no tiene equivalente, copiarlo directamente a la carpeta de salida
            if os.path.isfile(file1_path):
                with open(file1_path, 'rb') as src, open(output_path, 'wb') as dest:
                    dest.write(src.read())
                print(f"Archivo copiado sin cambios: {output_path}")

def main():
    root = Tk()
    root.withdraw()  # Ocultar la ventana principal

    folder1 = select_folder("Selecciona la primera carpeta")
    if not folder1:
        messagebox.showerror("Error", "No seleccionaste la primera carpeta.")
        return

    folder2 = select_folder("Selecciona la segunda carpeta")
    if not folder2:
        messagebox.showerror("Error", "No seleccionaste la segunda carpeta.")
        return

    # Crear la carpeta de salida "statsMix" en la misma ubicación que folder1
    output_folder = os.path.join(os.path.dirname(folder1), "statsMix")

    process_folders(folder1, folder2, output_folder)
    messagebox.showinfo("Finalizado", f"El procesamiento ha terminado. Los archivos combinados están en: {output_folder}")

if __name__ == "__main__":
    main()
