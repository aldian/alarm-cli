# Alarm CLI

A simple command-line alarm program that helps you wake up at a specified time.

## Installation

1. Make sure you have Python 3.6+ installed
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the program with a date and time argument:

```bash
# Using a custom sound file (plays for 1 minute)
python alarm.py "2024-03-20 07:30" --sound alarm.mp3

# Using the default generated tone (plays continuously until interrupted)
python alarm.py "2024-03-20 07:30"
```

You can also use natural language time expressions:
```bash
python alarm.py "tomorrow 07:30" --sound alarm.mp3
python alarm.py "next monday 08:00"  # Uses generated tone
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
python alarm.py "tomorrow 07:30 PST"  # Uses generated tone

# Using UTC
python alarm.py "2024-03-20 07:30 UTC" --sound alarm.mp3

# Using offset
python alarm.py "2024-03-20 07:30 +0200" --sound alarm.mp3
```

If no timezone is specified, the program will use your local timezone.

### Features

- Real-time countdown display with hours, minutes, and seconds
- Support for various time formats and timezones
- Optional custom alarm sound or built-in tone generator
- Custom sound files play for 1 minute
- Generated tone plays continuously until interrupted (Ctrl+C)
- Maximum volume playback

## Notes

- If no sound file is specified, the program will use a generated 1000Hz tone that plays continuously
- To stop the generated tone, press Ctrl+C
- The sound file must be in a format supported by pygame (MP3, WAV, etc.)
- The program will continue running until the alarm time is reached
- All times are converted to your local timezone for display 