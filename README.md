# My Python Scripts Repository

Welcome to my repository of simple Python scripts! This collection contains scripts that I've written for various tasks and utilities. Each script is designed to be straightforward and useful, and I regularly add new ones as I create them.

## Index

- [Rank Files by Size](#rank-files-by-size)

---

### Rank Files by Size

**Script Name**: `rank_files_by_size.py`

This script ranks all the files and folders within a given directory based on their size. It allows you to dive deeper into subfolders for detailed analysis and backtrack to previous directories for easier navigation.

#### Features
- **File and Folder Ranking**: Displays all files and folders sorted by size in descending order.
- **Real-Time File Count**: Tracks and updates the number of files read while the script is running.
- **Detailed Table Output**: Outputs a table with the rank, name, number of files, and total size for each file or folder.
- **Dive-In Functionality**: Allows the user to dive into a folder and rerun the ranking script within it.
- **Backtracking**: Lets the user backtrack to the previous directory if they have navigated deeper.

#### How to Use
1. Run the script:
   ```bash
   python rank_files_by_size.py
2. Enter the directory path when prompted.
3. View the ranked table:
   - **Rank**: The rank of the file or folder based on size.
   - **File/Folder**: The name of the file or folder.
   - **Number of Files**: The number of files in the folder (or 1 for a file).
   - **Total Size (MB)**: The size of the file or folder in megabytes.
4. Options after the table is displayed:
   - **Dive Deeper**: Type `d` when prompted to dive into a folder. Enter the rank of the folder you want to explore. The script will rerun in that folder.
   - **Backtrack**: Type `b` to go back to the previous directory if you've navigated deeper.
   - **Exit**: Type `e` to exit the script.

#### Example Output
##### Initial Run:
```bash
Enter the directory path: /path/to/directory

Number of files read: 15

Summary:
+------+--------------+----------------+-----------------+
| Rank | File/Folder  | Number of Files | Total Size (MB) |
+------+--------------+----------------+-----------------+
|  1   | folder_a     |       10       |      25.32      |
|  2   | file_b.txt   |       1        |      15.78      |
|  3   | file_c.txt   |       1        |       5.43      |
+------+--------------+----------------+-----------------+

Total size of the directory: 46.53 MB
```
##### Dive Deeper
```bash
Do you wish to dive deeper into a folder, backtrack, or exit? (d/b/e): d
Enter the rank of the folder to dive into: 1

Number of files read: 10

Summary:
+------+--------------+----------------+-----------------+
| Rank | File/Folder  | Number of Files | Total Size (MB) |
+------+--------------+----------------+-----------------+
|  1   | subfile_1    |       1        |       5.00      |
|  2   | subfile_2    |       1        |       3.50      |
+------+--------------+----------------+-----------------+

Total size of the directory: 8.50 MB
```
##### Backtracking
```bash
Do you wish to dive deeper into a folder, backtrack, or exit? (d/b/e): b

Number of files read: 15

Summary:
+------+--------------+----------------+-----------------+
| Rank | File/Folder  | Number of Files | Total Size (MB) |
+------+--------------+----------------+-----------------+
|  1   | folder_a     |       10       |      25.32      |
|  2   | file_b.txt   |       1        |      15.78      |
|  3   | file_c.txt   |       1        |       5.43      |
+------+--------------+----------------+-----------------+

Total size of the directory: 46.53 MB
```