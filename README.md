# Poker Finder
Poker Finder is a project for automated fetching and analysis of poker tournament data, aiming to provide users with convenient tournament information lookup and basic data statistics functions.

## Features

- Tournament Search: Find poker tournaments based on filter criteria.
- Tournament Details: Display tournament registration fees, prizes, start time, location, and other information.
- Real-time Updates: Offer real-time tournament data update functionality.
- Simple Interface: Intuitive user interface for easy browsing and selecting tournaments.

## Installation

1. Clone this repository:
   git clone https://github.com/nami-mera/poker-finder.git

2. Install dependencies:
   cd poker-finder
   pip install -r requirements.txt

## Usage

1. Run the fetch script:
   python scheduler.py

2. Query tournament information:
   python server.py

## Project Structure

- `scheduler.py`: Data fetching script
- `ai_agent.py`: Tournament data statistics and analysis
- `server.py`: Information query entry
- `data/`: Stores raw and processed data
- `README.md`: Project documentation

## Contribution

Contributions are welcome via issues or pull requests to improve this project. Please follow coding standards and contribution guidelines.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

If you have any questions or suggestions, please contact the project maintainers.
