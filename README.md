# Brawl Stars API Fetch

This project is a Python-based tool that fetches and tracks statistics from the Brawl Stars API for a specific club and its members.

## Features

- Fetches detailed club information
- Tracks individual player statistics
- Records brawler information for each player
- Monitors club member changes (joining/leaving)
- Tracks club rankings (French and Global)
- Exports data to CSV files for analysis

## Requirements

- Python 3.x
- Required Python packages:
  - requests
  - python-dotenv
  - tqdm
- Brawl Stars dev account

## Setup

1. Clone this repository
2. Install required packages:

   ```bash
   pip install requests python-dotenv tqdm
   ```

3. Create a `.env` file with your Brawl Stars API key (https://developer.brawlstars.com/#/):

   ```env
   wifi_name = 'Your Brawl Stars API key'
   ```

## Usage

Run the main script to fetch and update club statistics:

```bash
python GetInfo.py
```

The script will:

- Check if you're connected to the configured WiFi network
- Fetch current club data
- Update player statistics
- Track member changes
- Save all information to CSV files

## Output Files

The script generates two CSV files:

1. `Club Member Infos.csv`: Detailed information about each club member including:
   - Date and time
   - Player rank
   - Name
   - Role
   - Trophies
   - Victory statistics
   - Experience points
   - Individual brawler trophies

2. `Club Infos.csv`: Overall club statistics including:
   - Date and time
   - Club name and tag
   - Total trophies
   - Member count
   - Member changes
   - French and Global rankings
   - Top and bottom members

## Notes

- The script prevents multiple runs on the same day to avoid duplicate data
- Requires a valid Brawl Stars API key
- Tracks historical data for comparison
