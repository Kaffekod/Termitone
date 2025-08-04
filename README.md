# Termitone: Terminal-Based Guitar Tuner

**Termitone** is a lightweight guitar tuner built for simplicity and accuracy straight from your terminal. It supports standard EADGBE tuning and gives live feedback using an ASCII pitch bar that tracks your tuning in real time. Whether you're on Linux, macOS, or Windows, Termitone delivers fast performance with minimal setup, powered by Python.

## Features
- Standard EADGBE tuning for six-string guitars  
- ASCII pitch bar visualization with real-time feedback
- Median pitch smoothing for consistent readings  
- Harmonic filtering to reduce false detections  
- Fine-tune Termitone via a user-accessible config file; Adjust pitch buffers, silence thresholds, etc.
- Runs directly from the terminal without a GUI  

## Requirements
- A microphone for audio input
- Python **3.7 or newer**
- Required Python packages:
  - `numpy` – signal handling and pitch smoothing
  - `sounddevice` – real-time audio input
  - `aubio` – pitch detection (YIN FFT algorithm)

## Installing Python and Packages
If you already have Python **3.7+** and the required packages installed you can skip to [**Running Termitone**](#running-termitone).

If not, follow the steps below to get set up.

### Step 1 - Method 1: Install Python with Package Manager (Linux)

#### Debian/Ubuntu (APT)
```bash
sudo apt update
sudo apt install python3 python3-pip
```

#### Fedora (DNF)
```bash
sudo dnf install python3 python3-pip
```

#### Arch (Pacman)
```bash
sudo pacman -S python python-pip
```
---

### Step 1 - Method 2: Install Python with winget (Windows)

If you're using Windows 10 or later with winget available, you can install Python from the command line:

```bash
winget install python
```
---

### Step 2 - Python version and Python packages

After installing Python you could check that you have a supported version via the command below:
```bash
python3 --version
```
If it returns Python 3.7 or higher you're good to go.

Install the following Python packages:

```bash
pip install numpy
pip install sounddevice
pip install aubio
```
These packages enables microphone input, pitch detection, and numerical processing. Compatible with most microphones and USB audio interfaces.

## Running Termitone

Once Python is installed and the required packages are set up, you can launch Termitone from your terminal.
To get started, clone the Termitone GitHub repository to your local machine. Open your terminal and run:

```bash
git clone https://github.com/your-username/termitone.git
cd termitone
```

If you cloned the GitHub repository or downloaded the application in another way, navigate to its directory and run Termitone:
```bash
cd termitone
python3 termitone.py
```

And there you go, enjoy terminal-based guitar tuning!

## How to use it?

- Select a string from the menu to begin tuning.
- Play the string and watch the pitch bar respond.
- The visual bar displays if you're flat, sharp, or in tune.
- Press `Ctrl+C` to cancel or return to the string selection menu at any time.
- Enter `q` or `quit` in the string menu selection to exit the program.

Works best in quiet environments. Background noise can interfere with pitch detection.

## Troubleshooting
#### **No sound detected?**
  - Check that your microphone is correctly set as the input device.
  - Try running the script with administrative privileges.

#### **Python errors?**
  - Double-check that you're running Python 3.7+
  - Ensure all packages are installed: `numpy`, `sounddevice`, `aubio`

#### **Incorrect pitch readings?**
  - Tune in a quiet room.
  - Use a microphone with low latency and good frequency response.
  - If the frequency readings are jittery or inaccurate, consider changing the `PITCH_BUFFER_SIZE` variable to a higher value for more stability. Default is `10`. `15` or `20` have been tested and works well, too. (note that increasing this value will reduce responsiveness).

#### **Tuning not accurate enough?**
  - By default the `PITCH_TOLERANCE` for what is considered to be in tune is set to `2.0 Hz`. This could easily be changed to fit your need.

## License
Termitone is released under the GNU GPLv3 License. See `LICENSE` for details.

## Contribution & Contact

Contributions are welcome! Feel free to submit issues, feature requests, or pull requests via GitHub.

For questions, feedback, or collaboration inquiries, reach out via Discord: **Kaffekod**  
Direct messages are welcome and will be responded to as time permits.





