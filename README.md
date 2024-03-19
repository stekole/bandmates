# bandmates
Add in or remove your favorite bandmates from songs

# Introduction

Ever hate your bassist in your band? Use this script to download audio and remove instruments on the fly using [demuc](https://github.com/facebookresearch/demucs) and [yt-dlp](https://github.com/yt-dlp/yt-dlp).

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



## Examples

karaoke fridays at the officeeee
```python
python3 app.py --link "https://www.youtube.com/watch?v=dQw4w9WgXcQ" -r vocals
```

Download a default of a guitar-less track from a link
```python
python3 app.py --link "https://www.youtube.com/watch?v=tMDFv5m18Pw&ab_channel=OzzyOsbourneVEVO"
```

Remove more than one instrument
```python
python3 app.py --link "https://www.youtube.com/watch?v=tMDFv5m18Pw&ab_channel=OzzyOsbourneVEVO" -r guitar -r vocals
```
