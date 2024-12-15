# Minecraft-Stats-Folders-Adder
Sometimes, Minecraft does not save the game correctly, which can lead to the loss of statistics. This program is designed to merge the statistics from the `stats` folder of your last backup with the new one (in case you played for a while after the error and don't want to lose your latest changes).

**How to use:**  
You need to select two `stats` folders. The first one should be from your current game (the one you lost because you didn’t know how to save your little game properly), and the second one from your last backup. The order is important because if the backup game is from an earlier version, some `.json` statistic files may not be copied.

The result of the merged statistics is saved in a new folder called `statsMix` located in the path where the program was executed.

**How the code works:**  
The program opens two windows to select the `stats` folders to be merged. Once selected, the first `stats` folder is considered the most recent, and each `.json` file is iterated through. The program checks if the file exists in the second folder and, if so, merges their data by matching the keys in each pair. If the file does not exist in the second folder, it will keep the file from the first folder. That’s why the first folder must be the most recent.
