# audio-refactor

Batch-process `.amr` audio files into cleaned `.wav` files by:

- converting AMR to WAV with `ffmpeg`
- reducing background noise with `noisereduce`
- removing long silence segments with `pydub`

## Requirements

- Windows (this guide is Windows-first)
- Python `3.11+`
- FFmpeg available in system `PATH`

## 1) Clone the repository

```powershell
git clone <your-repo-url>
cd audio-refactor
```

## 2) Create and activate virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

## 3) Install Python dependencies

This project uses dependencies declared in `pyproject.toml`.

```powershell
python -m pip install --upgrade pip
pip install -e .
```

Installed packages include:

- `librosa>=0.11.0`
- `noisereduce==2.0.1`
- `numpy>=2.4.6`
- `pydub>=0.25.1`
- `soundfile>=0.14.0`

## 4) Install FFmpeg (Windows)

You downloaded: `ffmpeg-release-essentials.zip` from:
`https://www.gyan.dev/ffmpeg/builds/`

Do this once:

1. Extract `ffmpeg-release-essentials.zip`.
2. Open the extracted folder, then open `bin`.
3. Copy the full path of that `bin` folder.
	 - Example: `C:\tools\ffmpeg-7.1-essentials_build\bin`
4. Add it to your PATH:
	 - Press `Win` key and search for: `Edit the system environment variables`
	 - Click `Environment Variables...`
	 - Under `User variables` (or `System variables`), select `Path` -> `Edit` -> `New`
	 - Paste the FFmpeg `bin` path and click `OK`.
5. Close and reopen terminal.

Verify:

```powershell
ffmpeg -version
```

If this prints version details, FFmpeg is configured correctly.

## 5) Configure input folder in code

Before running, update the `INPUT_FOLDER` path in `main.py` to your folder containing `.amr` files.

Current line in code:

```python
INPUT_FOLDER = r"D:\My Data\downloads\Experimental"
```

The script writes output to:

- `<INPUT_FOLDER>\processed`

## 6) Run the software

With virtual environment activated:

```powershell
python main.py
```

You should see logs like `Processing: ...` and finally:

`Done! Check 'processed' folder.`

## Troubleshooting

- `ffmpeg is not recognized`:
	- PATH is not set correctly, or terminal was not restarted after PATH update.
- No output files:
	- Confirm `INPUT_FOLDER` exists and contains `.amr` files.
- PowerShell activation blocked:
	- Run once in PowerShell as current user:
		`Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`
