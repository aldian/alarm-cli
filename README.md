# Alarm CLI

A simple command-line alarm program that helps you wake up at a specified time.

## Installation

1. Make sure you have Python 3.6+ installed
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the program with a date and time argument and a sound file:

```bash
python alarm.py "2024-03-20 07:30" --sound alarm.mp3
```

You can also use natural language time expressions:
```bash
python alarm.py "tomorrow 07:30" --sound alarm.mp3
python alarm.py "next monday 08:00" --sound alarm.mp3
```

Or use the short form for the sound argument:
```bash
python alarm.py "now + 5 minutes" -s alarm.mp3
```

### Timezone Support

The program supports timezone-aware alarms. You can specify the timezone in several ways:

```bash
# Using timezone abbreviations
python alarm.py "2024-03-20 07:30 EST" --sound alarm.mp3
python alarm.py "tomorrow 07:30 PST" --sound alarm.mp3

# Using UTC
python alarm.py "2024-03-20 07:30 UTC" --sound alarm.mp3

# Using offset
python alarm.py "2024-03-20 07:30 +0200" --sound alarm.mp3
```

If no timezone is specified, the program will use your local timezone.

### Features

- Real-time countdown display with hours, minutes, and seconds
- Support for various time formats and timezones
- Customizable alarm sound
- Maximum volume playback
- Plays alarm sound for 1 minute when triggered

## Notes

- The sound file must be in a format supported by pygame (MP3, WAV, etc.)
- The program will continue running until the alarm time is reached
- You can stop the program at any time by pressing Ctrl+C
- All times are converted to your local timezone for display 