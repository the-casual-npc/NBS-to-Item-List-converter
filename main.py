import time
from math import ceil
import pynbs
from pathlib import Path

song = pynbs.read("track.nbs")
decodedSong = {}
instrumentNames = ["Harp", "Double Bass","Bass Drum", "Snare Drum", "Clicks","Guitar", "Flute", "Bell", "Chime", "Xylophone", "Iron Xylophone", "Cowbell", "Didgeridoo", "Bit", "Banjo", "Pling"]
discNames = ["NONE", "13", "cat", "blocks", "chirp", "far", "mall", "mellohi", "stall", "strad", "ward", "11 OR Creator (Music Box)", "wait OR Creator", "Pigstep OR Precipice", "otherside OR Relic", "5"]

print("NBS to Item List converter")
print("Version: 1.0")
print("Tool created by: casual_npc")
print("Github: https://github.com/the-casual-npc/NBS-to-Item-List-converter")
print("M.A.E.S.T.R.O Note block player by: jazziired")
print("Modrinth: https://modrinth.com/modpack/maestro")
print("Thank you for using this tool! The decoding process will start in a few moments...")
time.sleep(3)

print()
print("Step 1: Decoding notes")
time.sleep(0.5)
#Decode the song into decodedSong = {instrumentName: {keyNumber: [notes]}, instrumentName: ...}
for note in song.notes:
    #Adjusting the notes into 0-24
    note.key -= 33

    #Sorting the notes into decodedSong
    try:
        if decodedSong[note.instrument] == None:
            print()
    except:
        decodedSong[note.instrument] = {}
        print(" Found instrument: ", instrumentNames[note.instrument])

    try:
        decodedSong[note.instrument][note.key].add(note.tick)
    except:
        decodedSong[note.instrument][note.key] = set()
        decodedSong[note.instrument][note.key].add(note.tick)
        print("     " + instrumentNames[note.instrument] + "Found new tone: ", note.key)

    print("         " + instrumentNames[note.instrument] + ": " + str(note.key) + ": Added note")

print()
print("Step 2: Creating itemlists")
time.sleep(0.5)
totalTacts = ceil(song.header.song_length / 4)

if Path(song.header.song_name).is_dir():
    print("WARNING: Directory with the name of yor song already exists. Please delete or move it and try again")
    quit()

for instrument in decodedSong:
    #make a folder for this instrument
    instrumentDirectory = Path(song.header.song_name) / str(instrumentNames[instrument])
    instrumentDirectory.mkdir(parents=True, exist_ok=True)
    print(" Creating itemlist for instrument: " + str(instrumentNames[instrument]))

    for key in decodedSong[instrument]:

        print("     " + instrumentNames[instrument] + ": Creating itemlist for key: " + str(key))
        print("         " + instrumentNames[instrument] + ": " + str(key) + ": Transcribing notes into music disc values")

        #Transcribe notes into items
        rawItems = []
        for tact in range(0, totalTacts):
            bits = [False, False, False, False]

            for i in range(0, 4):
                tick = (tact * 4) + i

                if tick in decodedSong[instrument][key]:
                    bits[i] = True
                else:
                    bits[i] = False

            signalStrength = 0
            for bit in bits:
                signalStrength = (signalStrength << 1) | bit

            rawItems.append(discNames[signalStrength])


        print("         " + instrumentNames[instrument] + ": " + str(key)+ ": Grouping items")

        #Group items ("NONE"s only) into stacks
        groupedItems = []
        itemCount = 0
        lastDisc = True

        for item in rawItems:
            if item == "NONE":
                if itemCount >= 64:
                    groupedItems.append(item + " x" + str(itemCount))
                    itemCount = 0
                else:
                    itemCount += 1

                lastDisc = False

            else:
                if not lastDisc:
                    groupedItems.append("NONE x" + str(itemCount))
                    itemCount = 0

                groupedItems.append(item)
                lastDisc = True

        print("         " + instrumentNames[instrument] + ": " + str(key) + ": Separating items into shulker boxes")

        #Sort items into shulker boxes
        shulkers = [[]]
        currentSlot = 1
        currentShulker = 0
        for item in groupedItems:
            if currentSlot > 27:

                shulkers.append([])

                currentShulker += 1
                currentSlot = 1

            shulkers[currentShulker].append(item)
            currentSlot += 1

        #Write file
        print("         " + instrumentNames[instrument] + ": " + str(key) + ": Writing item list to file")
        keyFile = instrumentDirectory / f"{key}.txt"
        with open(keyFile, "w") as f:
            for i, shulker_contents in enumerate(shulkers):
                f.write(f"\n--- SHULKER BOX #{i + 1} ---\n")

                if not shulker_contents:
                    continue

                visual_groups = []
                if shulker_contents:
                    current_item = shulker_contents[0]
                    count = 0

                    for item in shulker_contents:
                        if item == current_item:
                            count += 1
                        else:
                            display_name = f"{current_item} x{count}" if count > 1 else current_item
                            visual_groups.append(display_name)

                            current_item = item
                            count = 1

                    display_name = f"{current_item} x{count}" if count > 1 else current_item
                    visual_groups.append(display_name)

                for line in visual_groups:
                    f.write(line + ", ")
print()
print("Itemlists created successfully for song: " + song.header.song_name)
quit()