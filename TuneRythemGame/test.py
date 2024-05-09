from pydub import AudioSegment

def raise_pitch(input_path, output_path, semitones):
    """Raises the pitch of a WAV audio file by the specified number of semitones."""
    # Load the audio file into an AudioSegment object
    audio = AudioSegment.from_wav(input_path)

    # Calculate the pitch shift ratio from the semitones value
    pitch_ratio = 2 ** (semitones / 12)

    # Apply the pitch shift using the pydub API
    shifted = audio._spawn(audio.raw_data, overrides={"frame_rate": int(audio.frame_rate * pitch_ratio)})
    shifted = shifted.set_frame_rate(audio.frame_rate)

    # Export the shifted audio to the output file
    shifted.export(output_path, format="wav")

raise_pitch("./input.wav", "output.wav", 1)