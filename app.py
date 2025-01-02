from pathlib import Path
from typing import List, Optional, Dict
import demucs.separate
import yt_dlp
import click
from dataclasses import dataclass
from enum import Enum

class Instrument(str, Enum):
    GUITAR = 'guitar'
    BASS = 'bass'
    DRUMS = 'drums'
    VOCALS = 'vocals'
    PIANO = 'piano'

@dataclass
class Config:
    output_dir: Path = Path("final")
    original_dir: Path = Path("original")
    model_name: str = "htdemucs_6s"

class AudioProcessor:
    def __init__(self, config: Config = Config()):
        self.config = config
        self.config.output_dir.mkdir(exist_ok=True)
        self.config.original_dir.mkdir(exist_ok=True)
        
    def process_audio(self, link: str, instruments: Optional[List[str]] = None) -> Path:
        song_file = self._download_song(link)
        if not instruments:
            return self.config.output_dir / f"{song_file.stem}_final.mp3"
        
        current_file = song_file
        for instrument in instruments:
            current_file = self._strip_instrument(current_file, instrument)
            
        return current_file.rename(self.config.output_dir / f"{song_file.stem}_{'_'.join(instruments)}_final.mp3")

    def _strip_instrument(self, file_name: Path, instrument_type: str) -> Path:
        demucs.separate.main([
            "-o", str(self.config.output_dir),
            "--mp3", "--two-stems", instrument_type,
            "-n", self.config.model_name,
            str(file_name)
        ])
        return self.config.output_dir / self.config.model_name / file_name.stem / f"no_{instrument_type}.mp3"

    def _download_song(self, link: str) -> Path:
        ydl_opts: Dict = {
            'format': 'm4a/bestaudio/best',
            'restrictfilenames': True,
            'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3'}],
            'outtmpl': str(self.config.original_dir / '%(title)s.%(ext)s'),
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=True)
            if downloads := info.get("requested_downloads"):
                return Path(downloads[0]["filepath"])
        raise ValueError("Download failed")

@click.command()
@click.option('--link', required=True, help='YouTube video link')
@click.option('-r', '--remove', type=click.Choice([i.value for i in Instrument]), multiple=True, help='The -r/--remove flag can be used multiple times to remove several instruments. Valid options are: guitar, bass, drums, vocals, piano. example: `-r guitar -r drums`')
def main(link: str, remove: tuple) -> None:
    AudioProcessor().process_audio(link, list(remove))

if __name__ == '__main__':
    main()

