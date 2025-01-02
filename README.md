
# bandmates
Add in or remove your favorite bandmates from songs

![image](https://github.com/stekole/bandmates/assets/30674956/4b9942e2-7f7f-4d21-94d0-329309348993)

# Introduction

Ever hate the bassist in your band? Use this script to download audio and remove instruments on the fly using [demuc](https://github.com/facebookresearch/demucs) and [yt-dlp](https://github.com/yt-dlp/yt-dlp).

Remove any of the following supported instruments in the model
- bass
- vocal
- guitar
- piano
- drums

## Pre-req

```bash
brew install python3 pyenv ffmpeg
```

```python
pyenv install 3.10
python3 -m venv env
source env/bin/activate
python3 -m pip install -r requirements.txt
```

## Usage

````
Options:
  --link TEXT                     YouTube video link
  -r, --remove
      The -r/--remove flag can be used multiple times to remove several instruments. Valid options are: guitar, bass, drums, vocals, piano
  --help
```

## Examples

Download a song from a link (no removals)
```python
python3 app.py --link "https://www.youtube.com/watch?v=tMDFv5m18Pw&ab_channel=OzzyOsbourneVEVO"
```

karaoke fridays at the officeeee
```python
python3 app.py --link "https://www.youtube.com/watch?v=dQw4w9WgXcQ" -r vocals
```

Remove a guitar
```python
python3 app.py --link "https://www.youtube.com/watch?v=tMDFv5m18Pw&ab_channel=OzzyOsbourneVEVO" -r guitar
```

Remove more than one instrument
```python
python3 app.py --link "https://www.youtube.com/watch?v=tMDFv5m18Pw&ab_channel=OzzyOsbourneVEVO" -r guitar -r vocals
```

## Tests

```
python -m pytest tests/
```

# Output

Output files are always in MP3 format. The script will automatically convert input audio from YouTube to MP3.

Processed files are stored in:
 - `original/:` Original downloaded audio files
 - `final/:` Processed audio files with removed instruments

The final output filename will include which instruments were removed.

Example:
```
 ./final/Ozzy_Osbourne_-_Mama_I_m_Coming_Home_A440_Standard_Tuning_guitar_vocals_final.mp3
 ```

