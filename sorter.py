import audio_metadata
import os
import re as regex
from pathlib import Path

# global library root
libRoot = ""
libFiles = []

# formats a string to be only alphanumeric characters, no spaces (they're a pain)
def formatString(string):
    return regex.sub("[^a-zA-Z0-9]", "", str(string))

# build the master file path list
def buildMasterList():

    global libFiles

    for (root, dirs, files) in os.walk(libRoot, topdown = True):
        for file in files:
            filePath = Path.joinpath(Path(root), file)
            libFiles.append(filePath)

# gets the required metadata from each file
def getMetadata():

    global libFiles

    for filePath in libFiles:
        
        # for debugging
        print("trying: " + str(filePath))

        # try to parse track data, break on failure
        try:
            currentFile = audio_metadata.load(filePath)
            currentFileExt = Path(filePath).suffix

            # get and return needed metadata from the file
            filePath = {
                "path":filePath,
                "ext":Path(filePath).suffix,
                "artist":formatString(currentFile.tags.artist),
                "album":formatString(currentFile.tags.album),
                "song":formatString(currentFile.tags.title),
                "track":formatString(currentFile.tags.tracknumber),
            }
            
        except:
            print(str(filePath) + " is not an audio file or is an unsupported format")

def moveRenameFiles():

    print("Renaming files")
    global libRoot, libFiles

    for metadata in libFiles:

        # try to setup correct paths
        try:
            correctDir = Path.joinpath(libRoot, metadata.get("artist"))
            correctDir = Path.joinpath(correctDir, metadata.get("album"))
            correctPath = Path.joinpath(correctDir, metadata.get("track") + "_" + metadata.get("song") + metadata.get("ext"))

        # this will run if not an audio file i.e. cover art
        except:
            print("FIX ME")
            return

        # do nothing if the file already exists
        if Path.is_file(correctPath):
            print("file exists")
            return

        # mkdirs if needed
        if not Path.exists(correctDir):
            os.makedirs(correctDir)

        # move the file
        Path.rename(Path(metadata.get("filePath")), correctPath)

def main():

    global libRoot, libFiles

    # set the library root
    while (True):
        libRoot = input("Enter the root directory of your music library: ")
        if Path(libRoot).exists():
            break

    # build the master list of file paths
    buildMasterList()

    # get the requisite data from each audio file
    getMetadata()

    # move/rename files to new locations
    moveRenameFiles()

if __name__ == "__main__":
    main()
    

        



