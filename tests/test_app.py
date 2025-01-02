import pytest
from pathlib import Path
from app import AudioProcessor, Config, Instrument
from unittest.mock import patch, MagicMock


@pytest.fixture
def audio_processor():
    config = Config(
        output_dir=Path("/tmp/output"),
        original_dir=Path("/tmp/original"),
        model_name="test_model"
    )
    return AudioProcessor(config)

@pytest.fixture
def mock_yt_dlp():
    with patch('yt_dlp.YoutubeDL') as mock:
        mock.return_value.__enter__.return_value.extract_info.return_value = {
            "requested_downloads": [{"filepath": "/tmp/original/test_song.mp3"}]
        }
        yield mock

@pytest.fixture
def setup_dirs():
    # Create necessary directories
    output_dir = Path("/tmp/output")
    original_dir = Path("/tmp/original")
    model_dir = output_dir / "test_model" / "test_song"
    
    output_dir.mkdir(exist_ok=True)
    original_dir.mkdir(exist_ok=True)
    model_dir.mkdir(parents=True, exist_ok=True)
    
    # Create dummy files
    (model_dir / "no_guitar.mp3").touch()
    (original_dir / "test_song.mp3").touch()
    
    yield
    
    # Cleanup
    import shutil
    shutil.rmtree(output_dir)
    shutil.rmtree(original_dir)

@pytest.fixture
def audio_processor(setup_dirs):
    config = Config(
        output_dir=Path("/tmp/output"),
        original_dir=Path("/tmp/original"),
        model_name="test_model"
    )
    return AudioProcessor(config)


@pytest.fixture
def mock_demucs():
    with patch('demucs.separate.main') as mock:
        yield mock

def test_process_audio_no_instruments(audio_processor, mock_yt_dlp):
    result = audio_processor.process_audio("https://youtube.com/watch?v=test")
    assert result.name == "test_song_final.mp3"
    mock_yt_dlp.assert_called_once()

def test_process_audio_with_instruments(audio_processor, mock_yt_dlp, mock_demucs):
    result = audio_processor.process_audio(
        "https://youtube.com/watch?v=test", 
        [Instrument.GUITAR.value]
    )
    assert result.name == "test_song_guitar_final.mp3"
    mock_demucs.assert_called_once()

def test_download_song_failure(audio_processor):
    with patch('yt_dlp.YoutubeDL') as mock:
        mock.return_value.__enter__.return_value.extract_info.return_value = {}
        with pytest.raises(ValueError, match="Download failed"):
            audio_processor._download_song("https://youtube.com/watch?v=test")

def test_strip_instrument(audio_processor, mock_demucs):
    result = audio_processor._strip_instrument(Path("test.mp3"), Instrument.DRUMS.value)
    assert result.name == "no_drums.mp3"
    mock_demucs.assert_called_once_with([
        "-o", str(audio_processor.config.output_dir),
        "--mp3", "--two-stems", "drums",
        "-n", audio_processor.config.model_name,
        "test.mp3"
    ])