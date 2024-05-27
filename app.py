from __future__ import unicode_literals
import demucs.separate
import os
import shutil
import sys
import json
import yt_dlp
import click


@click.command()
@click.option('--link', help='link of the youtubezzz')
@click.option('-r','--remove', help='what instrument do you want to strip? (example: `--remove guitar` or `-r bass -r drums -r vocals -r piano`)', multiple=True)


def main(link,remove):

    dir = 'original'
    if not os.path.exists(dir):
        os.mkdir(dir)
    finishdir = 'final'
    if not os.path.exists(finishdir):
        os.mkdir(finishdir)

    print("Your link is:  "+link)

    songFileName = downloadSong(link,dir) #songFileName="Nirvana_-_The_Man_Who_Sold_The_World_MTV_Unplugged.mp3"
    print(songFileName)

    songfolderName = get_file_name(songFileName)
    print("Original Download: "+songFileName)
    processedFolder="./final/htdemucs_6s/"+songfolderName
    print("Processed folder: "+processedFolder)

    count=0
    finishedIInstrumeent=[]
    if remove: 
        instumentToRemove = list(remove)
        print("..... .... ... .. ... . ... ... .. .. . .. .")
        for index,item in enumerate(instumentToRemove):
            if index == 0 and item not in finishedIInstrumeent:
                print("INPUT: "+songFileName)
                finishSongPath=stripInstrumentFromSong(songFileName,item)
                finishedIInstrumeent.append(item)
                prev=index
            else:
                print(prev, instumentToRemove[prev])
                inputsong=processedFolder+'/no_'+instumentToRemove[prev]+'.mp3' #input previous file
                print("INPUT: "+inputsong)
                finishSongPath=stripInstrumentFromSong(inputsong,item)
                finishedIInstrumeent.append(item)
                prev=index
        songFileNameNoExtention=os.path.splitext(os.path.basename(songFileName))[0]
        fileExtention=os.path.splitext(os.path.basename(songFileName))[1]
        print(songFileNameNoExtention)
        finalSong='_'.join(instumentToRemove)
        fileName="./"+finishdir+"/"+songFileNameNoExtention+"_"+finalSong+"_final.mp3"

    else:
        songFileNameNoExtention=os.path.splitext(os.path.basename(songFileName))[0]
        print(songFileNameNoExtention)
        fileName="./"+finishdir+"/"+songFileNameNoExtention+"_final.mp3"
        finishSongPath = songFileName
    
    print("After move: "+finishSongPath)
    shutil.copyfile(finishSongPath, './'+fileName)

def stripInstrumentFromSong(fileName,type):

    demucs.separate.main(["-o","./final/","--mp3", "--two-stems", type, "-n", "htdemucs_6s", fileName])
    # get foldername
    file_path = fileName
    folderName = get_file_name(file_path)
    finishSongPath="./final/htdemucs_6s/"+folderName+"/no_"+type+".mp3"
    print("Finished path:"+finishSongPath)
    return finishSongPath

def downloadSong(link,dir):
    AUDIO_EXTENSION = 'mp3'
    ydl_opts = {
        'format': 'm4a/bestaudio/best',
        'restrictfilenames': True,
        # See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
        'postprocessors': [{  # Extract audio using ffmpeg
            'key': 'FFmpegExtractAudio',
            'preferredcodec': AUDIO_EXTENSION,
        }],
        'outtmpl':dir + '/%(title)s.%(ext)s',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(link, download=True)
        info_with_audio_extension = dict(info)
        # Return filename with the correct extension
        info_with_audio_extension['ext'] = AUDIO_EXTENSION

        for k in info_with_audio_extension.keys():
            if k == 'requested_downloads':
                #print("Requested downloads: ")
                requested_downloads=info_with_audio_extension.get("requested_downloads")
                #print(requested_downloads)
                for f in requested_downloads:
                    filename=f.get("filepath")
    return filename


def get_file_name(file_path):
    file_path_components = file_path.split('/')
    file_name_and_extension = file_path_components[-1].rsplit('.', 1)
    return file_name_and_extension[0]



if __name__ == '__main__':
    main()
