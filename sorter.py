
import audio_metadata
import os
import re as regex
from pathlib import Path

# build the file path list
def buildMasterList(rootDir):

    #  file path list to export
    libFiles = []

    for (root, dirs, files) in os.walk(rootDir, topdown = True):
        for i in files:
            k = Path.joinpath(root, i)
            libFiles.append(k)
    
    return libFiles

def formatString(string):
    
    # wanted to use isalnum() for this but it was always evaluating false
    # for any file containing spaces? gotta look into this

    # for char in string:
    #     if char.isalnum():
    #         newString += char
    newString = regex.sub("[^a-zA-Z0-9]", "", str(string))

    return newString

def parseData(filePath):
    print("trying: " + filePath)

    # try to parse track data, break on failure
    try:
        currentFile = audio_metadata.load(filePath)
        currentFileExt = Path(filePath).suffix

        # get metadata
        currentArtist = formatString(currentFile.tags.artist)
        currentAlbum = formatString(currentFile.tags.album)
        currentSong = formatString(currentFile.tags.title)
        currentTrack = formatString(currentFile.tags.tracknumber)

        # setup correct paths
        correctDir = Path.joinpath(rootDir, currentArtist)
        correctDir = Path.joinpath(correctDir, currentAlbum)
        correctPath = Path.joinpath(correctDir, currentTrack + "_" + currentSong + currentFileExt)
        # print(correctDir)
        # print(correctPath)
    
    except:
        print(filePath + " is not an audio file or is an unsupported format")
        return

def moveFiles(filePath, correctPath):
    # do nothing if the file already exists
    if Path.is_file(correctPath):
        print("file exists")
        return

    # make new directories if needed
    if not Path.exists(correctDir):
        os.makedirs(correctDir)

    Path.rename(Path(filePath), correctPath)

def main():
    # set the library root
    libRoot = input("Enter the root directory of your music library: ")

    # build the master list of file paths
    libFiles = buildMasterList(libRoot)

    # go to each one in sequence
    for filePath in libFiles:
        parseData(filePath)

if __name__ == __main__:
    main()
    

        



