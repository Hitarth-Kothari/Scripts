import os
import sys
from prettytable import PrettyTable
from concurrent.futures import ThreadPoolExecutor, as_completed

def get_size_in_mb(size_bytes):
    """
    Convert size from bytes to MB.
    """
    return round(size_bytes / (1024 * 1024), 2)

def calculate_file_size(file_path):
    """
    Get the size of a single file.
    """
    return os.path.getsize(file_path)

def calculate_folder_size(folder):
    """
    Calculate the total size of a folder and count the number of files in it.
    """
    total_size = 0
    num_files = 0
    for dirpath, _, filenames in os.walk(folder):
        for file in filenames:
            file_path = os.path.join(dirpath, file)
            if os.path.isfile(file_path):
                total_size += calculate_file_size(file_path)
                num_files += 1
    return total_size, num_files

def process_item(item_path, file_count):
    """
    Process a single item (file or folder), returning its size and number of files.
    """
    if os.path.isfile(item_path):
        size = calculate_file_size(item_path)
        file_count[0] += 1
        sys.stdout.write(f"\rNumber of files read: {file_count[0]}")
        sys.stdout.flush()
        return os.path.basename(item_path), 1, size, "File"
    elif os.path.isdir(item_path):
        size, num_files = calculate_folder_size(item_path)
        file_count[0] += num_files
        sys.stdout.write(f"\rNumber of files read: {file_count[0]}")
        sys.stdout.flush()
        return os.path.basename(item_path), num_files, size, "Folder"
    return None

def rank_files_and_folders_by_size(directory):
    """
    Ranks all files and folders in the specified directory by their sizes.
    """
    if not os.path.isdir(directory):
        print("The provided path is not a valid directory.")
        return [], 0
    
    items = []
    file_count = [0]  # Shared counter for tracking files read
    
    # Multithreaded processing of items
    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(process_item, os.path.join(directory, item), file_count)
            for item in os.listdir(directory)
        ]
        for future in as_completed(futures):
            result = future.result()
            if result:
                items.append(result)
    
    # Print a final newline after the counter
    print()
    
    # Sort items by size in descending order
    ranked_items = sorted(items, key=lambda x: x[2], reverse=True)
    
    return ranked_items, file_count[0]

def display_table_and_summary(ranked_items, total_size):
    """
    Displays the table and total size summary.
    """
    table = PrettyTable()
    table.field_names = ["Rank", "File/Folder", "Number of Files", "Total Size (MB)"]
    
    for i, (name, num_files, size, item_type) in enumerate(ranked_items, start=1):
        table.add_row([i, name, num_files, get_size_in_mb(size)])
    
    print("\nSummary:")
    print(table)
    print(f"\nTotal size of the directory: {get_size_in_mb(total_size)} MB")

def main():
    """
    Main function to handle the ranking, dive-in, and backtrack functionality.
    """
    directory_path = input("Enter the directory path: ").strip()
    history = [directory_path]  # Keeps track of the navigation history
    
    while True:
        ranked_items, total_files = rank_files_and_folders_by_size(directory_path)
        
        if ranked_items:
            total_size = sum(item[2] for item in ranked_items)
            display_table_and_summary(ranked_items, total_size)
            
            # Ask if the user wants to dive deeper or backtrack
            dive_in = input("\nDo you wish to dive deeper into a folder, backtrack, or exit? (d/b/e): ").strip().lower()
            if dive_in == "d":
                try:
                    rank = int(input("Enter the rank of the folder to dive into: ").strip())
                    if 1 <= rank <= len(ranked_items):
                        selected_item = ranked_items[rank - 1]
                        if selected_item[3] == "Folder":
                            history.append(directory_path)  # Save current directory to history
                            directory_path = os.path.join(directory_path, selected_item[0])
                        else:
                            print("Error: Selected item is not a folder.")
                    else:
                        print("Error: Invalid rank number.")
                except ValueError:
                    print("Error: Please enter a valid number.")
            elif dive_in == "b":
                if len(history) > 1:
                    directory_path = history.pop()  # Backtrack to the previous directory
                else:
                    print("You are already at the top-level directory.")
            elif dive_in == "e":
                break
            else:
                print("Invalid choice. Please enter 'd', 'b', or 'e'.")
        else:
            print("No items found in the directory or the path is invalid.")
            break

if __name__ == "__main__":
    main()
