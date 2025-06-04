# Alarm CLI

A simple command-line alarm program that helps you wake up at a specified time.

## Installation

1. Make sure you have Python 3.6+ installed
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Add an alarm sound file named `alarm.mp3` in the same directory as the script

## Usage

Run the program with a date and time argument:

```bash
python alarm.py "2024-03-20 07:30"
```

You can also use natural language time expressions:
```bash
python alarm.py "tomorrow 07:30"
python alarm.py "next monday 08:00"
```

### Timezone Support

The program supports timezone-aware alarms. You can specify the timezone in several ways:

```bash
# Using timezone abbreviations
python alarm.py "2024-03-20 07:30 EST"
python alarm.py "tomorrow 07:30 PST"

# Using UTC
python alarm.py "2024-03-20 07:30 UTC"

# Using offset
python alarm.py "2024-03-20 07:30 +0200"
```

If no timezone is specified, the program will use your local timezone.

## Notes

- Make sure to add an `alarm.mp3` file in the same directory as the script
- The program will continue running until the alarm time is reached
- You can stop the program at any time by pressing Ctrl+C
- All times are converted to your local timezone for display 