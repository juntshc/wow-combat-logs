# World of Warcraft Combat Log Parser

This project provides a set of tools for parsing World of Warcraft combat logs. It includes functionality to read combat logs, extract meaningful events, filter events for specific characters, and analyze damage per second (DPS).

## Features

- Read combat log files.
- Parse log entries into structured events.
- Filter events for specific characters or classes.
- Analyze DPS for filtered events.
- Visualize combat damage over time.
- Visualize the sequence of attacks in a grid scatter plot.
- Visualize total damage by spell.

## Getting Started

### Prerequisites

- Python 3.x
- Pandas library
- Matplotlib library

You can install the required packages using pip:

```
pip install pandas matplotlib
```

### Installation
Clone the repository to your local machine:

```
git clone https://github.com/juntshc/wow-combat-logs.git
cd wow-combat-logs
```

### Usage
First you need to enable combat logs in WoW.
1. Login to WoW
2. Type `/combatlog` in chat
3. Update the log file name in the wow_logs.py file to match your log file.
4. Run the script with the path to your combat log file:

```
python wow_logs.py
```

You can edit the main function within the wow_logs.py script to point to the correct location of your combat log file:

```
def main():
    log_location = 'path_to_your_combat_log.txt'
    # ... rest of the code
```

### Visualizations
The script provides three key visualizations:

- Combat Damage Over Time: Shows the damage done over the course of the combat session, with each spell and swing as different series.
- Attack Sequence Grid Scatter Plot: Displays the sequence of attacks over time, helping to identify the most used rotations.
- Total Damage by Spell: Provides a bar chart with the total damage done by each spell for easy comparison.

### Contributing
Contributions to this project are welcome. To contribute:

1. Fork the repository.
2. Create a new branch (git checkout -b feature-branch).
3. Commit your changes (git commit -am 'Add some feature').
4. Push to the branch (git push origin feature-branch).
5. Open a new Pull Request.


### License
This project is licensed under the MIT License - see the LICENSE.md file for details.

### Acknowledgments
Thanks to all the contributors who have helped with the development of this project.
Special thanks to the World of Warcraft community for their continuous support and feedback.

Remember to replace `https://github.com/your-username/wow-log-parser.git` with the actual URL of your Git repository. Additionally, ensure all the paths and commands are correctly mentioned as per your project's structure and requirements.

Save this content in a file named `README.md` in the root directory of your project. GitHub will automatically display this file's content on the main page of your repository.
