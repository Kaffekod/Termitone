import aubio
import numpy as np
import sounddevice as sd
from statistics import median

from termitone_cfg import (
    SAMPLE_RATE,
    FRAME_SIZE,
    SILENCE_THRESHOLD_DB,
    PITCH_BUFFER_SIZE,
    PITCH_TOLERANCE,
    BAR_RANGE_HZ,
    STANDARD_TUNING,
)

# Stops any existing audio streams (needed when switching strings in order to prevent crashing)
def stop_audio_stream():
    try:
        sd.stop()
        sd.abort()
    except Exception:
        pass

# ASCII bar to visualize the pitch offset of the selected string
def render_tuning_bar(observed_pitch, reference_pitch):
    scale_steps = 31                      # Width of the bar display
    center_index = scale_steps // 2       # Reference marker in the center, marker indicates where its in tune
    
    # Calculate pitch offset relative to reference
    relative_shift = int((observed_pitch - reference_pitch) * (scale_steps / (2 * BAR_RANGE_HZ)))
    marker_index = max(0, min(scale_steps - 1, center_index + relative_shift))
    bar = ["-"] * scale_steps             # Step indicators of the bar
    bar[center_index] = "|"               # Reference pitch marker
    bar[marker_index] = "X"               # Current pitch position
    return "[" + "".join(bar) + "]"

# Describes the pitch accuracy based on offset from the target frequency of the chosen string
def classify_pitch_offset(offset):
    deviation = abs(offset)
    if deviation <= PITCH_TOLERANCE:
        return "In tune"
    elif deviation <= 10:
        return "Slightly flat" if offset < 0 else "Slightly sharp"
    else:
        return "Too flat" if offset < 0 else "Too sharp"

# Suppresses readings near known harmonics of the reference pitch (This solved harmonic readings on laptop microphones with very sensitive microphones)
def detect_harmonic_overlap(pitch_freq, reference_freq):
    for multiple in [2, 3, 4]:  # Checks for the 2nd to 4th harmonics
        harmonic_freq = multiple * reference_freq
        threshold = PITCH_TOLERANCE + multiple * 3
        if abs(pitch_freq - harmonic_freq) < threshold:
            return True
    return False

# Handles live tuning session for a single string
def tune_string(string_name, target_pitch):
    stop_audio_stream()
    print(f"\nTuning string {string_name} ({target_pitch:.2f} Hz) | press Ctrl+C to go back to string selection.")

    # Initialize aubio pitch detection algorithm
    pitch_detector = aubio.pitch("yinfft", FRAME_SIZE * 2, FRAME_SIZE, SAMPLE_RATE)
    pitch_detector.set_unit("Hz")
    pitch_detector.set_silence(SILENCE_THRESHOLD_DB)

    pitch_buffer = []  # Stores recent pitch values for smoothing, this also ensures the pitch buffer gets reset at string change

    try:
        while True:
            # Record a short audio buffer from microphone
            recording = sd.rec(FRAME_SIZE, samplerate=SAMPLE_RATE, channels=1, blocking=True)
            sd.wait()

            # Extracts float samples from recorded signal
            input_signal = np.float32(recording[:, 0])
            detected_pitch = pitch_detector(input_signal)[0]

            # Filter out unusable pitches (too low or high)
            if detected_pitch < 40 or detected_pitch > 360:
                continue
            # Skip pitches that resemble harmonic artifacts
            if detect_harmonic_overlap(detected_pitch, target_pitch):
                continue

            # Store pitch for smoothing
            pitch_buffer.append(detected_pitch)
            if len(pitch_buffer) > PITCH_BUFFER_SIZE:
                pitch_buffer.pop(0)

            # Smooth pitch using median of recent values
            smoothed_pitch = median(pitch_buffer)

            # Determine pitch accuracy
            pitch_offset = smoothed_pitch - target_pitch
            pitch_status = classify_pitch_offset(pitch_offset)
            visual_bar = render_tuning_bar(smoothed_pitch, target_pitch)

            # Display tuning feedback
            print(
                f"{visual_bar}  {pitch_status.ljust(14)}  [{string_name}]  "
                f"Pitch: {smoothed_pitch:.2f} Hz | Target: {target_pitch:.2f} Hz",
                end="\r"
            )

    except KeyboardInterrupt:
        print("\nReturning to string selection")

# Prints the logo, welcome msg + instructions at startup
def print_intro_screen():
    print("")
    print(r"+=====================================================+")
    print(r"|                                                     |")
    print(r"|    _____                   _ _                      |")
    print(r"|   |_   _|__ _ __ _ __ ___ (_) |_ ___  _ __   ___    |")
    print(r"|     | |/ _ \ '__| '_ ` _ \| | __/ _ \| '_ \ / _ \   |")
    print(r"|     | |  __/ |  | | | | | | | || (_) | | | |  __/   |")
    print(r"|     |_|\___|_|  |_| |_| |_|_|\__\___/|_| |_|\___|   |")
    print(r"|                                                     |")
    print(r"|      A Terminal-based Guitar Tuner by KaffeKod      |")
    print(r"|       https://github.com/Kaffekod/Termitone/        |")
    print(r"|                      V. 0.1.0                       |")
    print(r"+=====================================================+")
    print("\nWelcome to Termitone! Your terminal-based guitar tuner.")
    print("Standard EADGBE tuning is supported for six-string guitars.")
    print("Select the string you'd like to tune from the list below.")
    print("Type 'q' or 'quit' to quit the tuner.\n")

# Presents the available strings and gets user input for string selection
def get_user_string_selection():
    print("Strings available for tuning:")
    for string in STANDARD_TUNING:
        print(f"  - {string} ({STANDARD_TUNING[string]:.2f} Hz)")
    print("\nEnter the name of the string you want to tune (E2, A2, etc.), or write 'q' or 'quit' to quit:")

    selection = input("Your selection: ").strip().upper()
    return selection

# Main menu loop to select which string to tune
def main():
    print_intro_screen()

    while True:
        selection = get_user_string_selection()

        if selection in {"Q", "QUIT"}:
            print("Quitting. Thank you for using Termitone!")
            break
        elif selection not in STANDARD_TUNING:
            print("Invalid choice. Please enter one of the listed string names.")
            continue

        tune_string(selection, STANDARD_TUNING[selection])

if __name__ == "__main__":
    main()
