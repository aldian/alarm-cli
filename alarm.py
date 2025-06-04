#!/usr/bin/env python3

import argparse
import datetime
import time
import os
import re
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

def play_alarm(sound_file):
    """Play the alarm sound repeatedly for 1 minute with increased volume."""
    if not os.path.exists(sound_file):
        print(f"Warning: {sound_file} not found. Please provide a valid sound file.")
        return
    
    try:
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
    except Exception as e:
        print(f"Error playing sound: {e}")
    finally:
        pygame.mixer.quit()

def main():
    parser = argparse.ArgumentParser(description='Set an alarm to wake you up.')
    parser.add_argument('datetime', type=parse_datetime,
                      help='Date and time for the alarm. Examples:\n'
                           '- Absolute time: "2024-03-20 07:30" or "tomorrow 07:30"\n'
                           '- With timezone: "2024-03-20 07:30 EST" or "tomorrow 07:30 UTC"\n'
                           '- Relative time: "now + 10 seconds" or "now + 5 minutes"')
    parser.add_argument('--sound', '-s', required=True,
                      help='Path to the alarm sound file')
    
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
    print(f"Using sound file: {args.sound}")
    
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