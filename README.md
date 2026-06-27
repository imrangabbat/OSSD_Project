# 🚗 Parking Management System

A simple and efficient parking management system built with Python and Tkinter. This project helps manage parking spots, track vehicle entry/exit, calculate parking fees, and maintain transaction history.

## Features

✅ **Parking Spot Management** - Track 20 parking spots with real-time status
✅ **Vehicle Entry/Exit** - Simple interface to park and remove vehicles
✅ **Automatic Fee Calculation** - Calculate fees based on duration and settings
✅ **Transaction History** - View all past transactions with filtering
✅ **Daily Revenue Tracking** - Monitor revenue for each day
✅ **Configurable Settings** - Adjust hourly rates, free minutes, and max daily charge
✅ **Receipt Generation** - Generate unique receipts for each transaction

## Project Structure

```
parking-management-system/
├── main.py              # Main application entry point
├── database.py          # Database operations (SQLite)
├── dialogs.py           # UI dialog windows
├── requirements.txt     # Python dependencies
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## Prerequisites

- Python 3.7 or higher
- Tkinter (usually comes with Python)
- SQLite3 (built-in with Python)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/parking-management-system.git
cd parking-management-system
```

2. Install dependencies (if needed):
```bash
pip install -r requirements.txt
```

## How to Run

Simply execute the main script:

```bash
python main.py
```

Or if using Python 3:

```bash
python3 main.py
```

## Usage

### Main Dashboard
- View all 20 parking spots with real-time status
- Green spots = Available
- Red spots = Occupied
- See today's revenue and occupancy stats

### Parking a Vehicle
1. Click on an available (green) spot
2. Enter the vehicle number
3. Receive a receipt with parking details

### Removing a Vehicle
1. Click on an occupied (red) spot
2. Review parking duration
3. System calculates fee automatically
4. Confirm exit and receive exit receipt

### Settings
- **Hourly Rate**: Cost per hour (default: $5.00)
- **Free Minutes**: Complimentary parking duration (default: 15 min)
- **Max Daily Charge**: Maximum fee per day (default: $40.00)

### View Transactions
- See all completed transactions
- Filter by date (YYYY-MM-DD format)
- View vehicle number, duration, fee, and receipt details

## Database

The system uses SQLite3 database stored in `parking_system.db` with three tables:

- **spots**: Parking spot information and status
- **transactions**: Vehicle entry/exit records and fees
- **settings**: Configuration settings

## Default Settings

- Total Parking Spots: 20
- Hourly Rate: $5.00
- Free Parking Duration: 15 minutes
- Max Daily Charge: $40.00

## Features Included

- Auto-refresh every 30 seconds
- Live clock display
- Menu-based navigation
- Duplicate vehicle check (prevents parking same vehicle twice)
- Input validation
- User-friendly error messages

## Future Enhancements

- Multi-level parking support
- Reserved spots feature
- Email receipt option
- Vehicle owner database
- Annual pass support
- Admin panel with detailed reports
- SMS notifications

## License

This project is open source and available under the MIT License.

## Author

Your Name / OSSD Project

## Support

For issues or suggestions, please open an issue on GitHub.
