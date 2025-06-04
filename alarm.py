#!/usr/bin/env python3

import argparse
import datetime
import time
import os
import re
import numpy as np
import sounddevice as sd
from dateutil import parser, tz
import pygame

def parse_relative_time(time_str):
    """Parse relative time expressions like 'now + 10 seconds'."""
    now_pattern = r'now\s*\+\s*(\d+)\s*(second|minute|hour)s?'
    match = re.match(now_pattern, time_str.lower())
    if match:
        amount = int(match.group(1))
        unit = match.group(2)
        now = datetime.datetime.now(tz=tz.tzlocal())
        
        if unit == 'second':
            return now + datetime.timedelta(seconds=amount)
        elif unit == 'minute':
            return now + datetime.timedelta(minutes=amount)
        elif unit == 'hour':
            return now + datetime.timedelta(hours=amount)
    return None

def parse_datetime(datetime_str):
    """Parse the input datetime string into a datetime object."""
    try:
        # Try parsing as relative time first
        relative_time = parse_relative_time(datetime_str)
        if relative_time:
            return relative_time
            
        # If not relative time, parse as absolute time
        dt = parser.parse(datetime_str)
        
        # If the datetime is naive (no timezone), assume local timezone
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=tz.tzlocal())
            
        return dt
    except ValueError as e:
        raise argparse.ArgumentTypeError(f"Invalid datetime format: {e}")

def generate_tone(duration=1.0, frequency=1000):
    """Generate a simple sine wave tone."""
    sample_rate = 44100  # Sample rate in Hz
    
    # Generate the tone
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    tone = np.sin(frequency * t * 2 * np.pi)
    
    # Ensure that highest value is in 16-bit range
    audio = tone * (2**15 - 1) / np.max(np.abs(tone))
    # Convert to 16-bit data
    audio = audio.astype(np.int16)
    
    return audio, sample_rate

def play_alarm(sound_file=None):
    """Play the alarm sound repeatedly for 1 minute with increased volume."""
    try:
        if sound_file and os.path.exists(sound_file):
            # Initialize pygame mixer
            pygame.mixer.init()
            # Load the sound file
            sound = pygame.mixer.Sound(sound_file)
            # Set volume to maximum (1.0)
            sound.set_volume(1.0)
            
            end_time = time.time() + 60  # Play for 1 minute
            while time.time() < end_time:
                sound.play()
                # Wait for the sound to finish playing
                pygame.time.wait(int(sound.get_length() * 1000))
                # Add a small delay between plays to prevent overlapping
                time.sleep(0.1)
        else:
            # Generate and play a tone continuously
            audio, sample_rate = generate_tone(duration=1.0)
            # Play the tone continuously
            sd.play(audio, sample_rate, loop=True)
            # Keep the script running until interrupted
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                sd.stop()
    except Exception as e:
        print(f"Error playing sound: {e}")
    finally:
        if sound_file:
            pygame.mixer.quit()
        else:
            sd.stop()

def main():
    parser = argparse.ArgumentParser(description='Set an alarm to wake you up.')
    parser.add_argument('datetime', type=parse_datetime,
                      help='Date and time for the alarm. Examples:\n'
                           '- Absolute time: "2024-03-20 07:30" or "tomorrow 07:30"\n'
                           '- With timezone: "2024-03-20 07:30 EST" or "tomorrow 07:30 UTC"\n'
                           '- Relative time: "now + 10 seconds" or "now + 5 minutes"')
    parser.add_argument('--sound', '-s',
                      help='Path to the alarm sound file (optional, will use generated tone if not specified)')
    
    args = parser.parse_args()
    alarm_time = args.datetime
    
    # Calculate time until alarm (using timezone-aware datetime)
    now = datetime.datetime.now(tz=tz.tzlocal())
    time_until_alarm = (alarm_time - now).total_seconds()
    
    if time_until_alarm < 0:
        print("Error: The specified time has already passed!")
        return
    
    # Convert alarm time to local timezone for display
    local_alarm_time = alarm_time.astimezone(tz.tzlocal())
    
    print(f"Alarm set for: {local_alarm_time.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    if args.sound:
        print(f"Using sound file: {args.sound}")
    else:
        print("Using generated tone")
    
    # Countdown loop
    while time_until_alarm > 0:
        hours = int(time_until_alarm // 3600)
        minutes = int((time_until_alarm % 3600) // 60)
        seconds = int(time_until_alarm % 60)
        
        # Clear the current line and print the countdown
        print(f"\rTime until alarm: {hours:02d}:{minutes:02d}:{seconds:02d}", end="", flush=True)
        
        # Sleep for 1 second
        time.sleep(1)
        time_until_alarm -= 1
    
    # Play alarm sound
    print("\nWAKE UP! 🔔")
    play_alarm(args.sound)

if __name__ == "__main__":
    main() 