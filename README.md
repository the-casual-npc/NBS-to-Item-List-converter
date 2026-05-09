# NBS-to-Item-List-converter
A Python Script that takes a .NBS file, and generates an item list for each instrument and tone. This tool was created for the M.A.E.S.T.R.O Note block player by jazziired and others.
Check the original project here: https://modrinth.com/modpack/maestro

How to use:
1. Download "script.py" and place it into an empty folder. This is where the output will be generated

2. Rename your .nbs file to "track.nbs" and place it into the folder alongside the script

3. Run the script. The script will read the .nbs file and generate the itemlist with the following structure:
   - A subfolder is created alongside the script, named after the track name (taken from the song header)
   - Inside this folder, subfolders for each used instrument are created
   - For each instrument, the script creates .txt files for each used tone
   - In each .txt file, the items are organised into shulkers. In each shulker a list of items is written in the order they should be loaded into shulker boxes

Note:
  - Pauses in the song are indicated by "NONE". For these pauses, filler items stackable to 64 should be used. Make sure to use a different filler item for each pause (as to not mix when being decoded)
  - This tool has been created with Vanilla notes only in mind (if anyone would be interested in custom notes or notes beyond the normal minecraft range, I am open to adding that feature)
