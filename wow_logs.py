import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
from collections import defaultdict
from datetime import datetime

def read_combat_log(filename):
    with open(filename, 'r') as file:
        return file.readlines()
    
def parse_timestamp(timestamp_str):
    # Adjust the format string to match the format of your timestamp
    return datetime.strptime(timestamp_str, '%m/%d %H:%M:%S.%f')

def parse_log_lines(lines):
    events = []
    for line in lines:
        timestamp, log = tuple(line.split('  '))
        parts = log.split(',')
        event = {
            'timestamp': timestamp,
            'event_type': parts[0] if len(parts) > 1 else None,
            'source_guid': parts[1] if len(parts) > 2 else None,
            'source_name': parts[2] if len(parts) > 3 else None,
            'source_flags': parts[3] if len(parts) > 4 else None,
            'destination_guid': parts[4] if len(parts) > 5 else None,
            'destination_name': parts[5] if len(parts) > 6 else None,
            'destination_flags': parts[6] if len(parts) > 7 else None,
            'spell_id': parts[7] if len(parts) > 8 else None,
            'spell_unknown': parts[8] if len(parts) > 9 else None,
            'spell_school': parts[9] if len(parts) > 10 else None,
            'spell_name': parts[10].replace('"', '') if len(parts) > 11 else None,
            'spell_dmg': parts[26] if len(parts) > 25 else None,
            'additional_data': parts[11:] if len(parts) > 12 else None
        }
        # fixup spell damage
        if event["event_type"] == 'SPELL_DAMAGE':
            event["spell_dmg"] = float(parts[29]) if len(parts) > 28 else None
        events.append(event)
    return events

def filter_for_self(events, character_name='Junts'):
    return [e for e in events if character_name in e['source_name']]


def process_damage_data(events):
    damage_data = defaultdict(list)  # Store individual damage events
    for event in events:
        if event['event_type'] in ['SPELL_DAMAGE', 'SWING_DAMAGE'] and event['spell_dmg']:
            timestamp = parse_timestamp(event['timestamp'])
            spell_name = event['spell_name'] if event['event_type'] == 'SPELL_DAMAGE' else 'Swing'
            damage_amount = float(event['spell_dmg'])
            damage_data[spell_name].append((timestamp, damage_amount))  # Store each damage event individually

    return damage_data


def plot_damage_over_time(damage_data):
    plt.figure(figsize=(15, 8))
    colors = plt.cm.tab20.colors  # Using a colormap that provides 20 distinct colors
    spell_color = dict()

    for spell_name, data_points in damage_data.items():
        if spell_name not in spell_color:
            spell_color[spell_name] = colors[len(spell_color) % len(colors)]

        timestamps, damages = zip(*data_points)
        plt.scatter(timestamps, damages, color=spell_color[spell_name], label=spell_name)

    # Format and beautify the plot
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d %H:%M'))
    plt.gca().xaxis.set_major_locator(mdates.MinuteLocator(interval=5))
    plt.gcf().autofmt_xdate()
    plt.xlabel('Time', fontsize=14)
    plt.ylabel('Damage', fontsize=14)
    plt.title('Individual Combat Damage Events Over Time for lvl 37 Warrior', fontsize=18)
    plt.legend(title='Spell Name', fontsize=12)
    plt.grid(True)
    plt.tight_layout()

    plt.show()


def plot_attack_sequence(events):
    spell_times = defaultdict(list)
    base_time = None

    for event in events:
        if event['event_type'] in ['SPELL_CAST_SUCCESS', 'SPELL_DAMAGE']:
            timestamp = parse_timestamp(event['timestamp'])
            if base_time is None:
                base_time = timestamp
            time_diff = (timestamp - base_time).total_seconds() / 60
            spell_name = event['spell_name']
            spell_times[spell_name].append(time_diff)

    plt.figure(figsize=(12, 8))
    for spell_name, times in spell_times.items():
        plt.scatter(times, [spell_name] * len(times), label=spell_name)

    plt.xlabel('Time (minutes from start)')
    plt.ylabel('Spell Name')
    plt.title('Attack Sequence Over Time')
    plt.grid(True)
    plt.show()

def plot_total_damage_by_spell(events):
    spell_damages = defaultdict(list)

    for event in events:
        if event['event_type'] in ['SPELL_DAMAGE', 'SWING_DAMAGE'] and event['spell_dmg']:
            spell_name = event['spell_name'] if event['event_type'] == 'SPELL_DAMAGE' else 'Swing'
            damage_amount = float(event['spell_dmg'])  # assuming the damage can be a float
            spell_damages[spell_name].append(damage_amount)

    # Plot each spell's damage as a separate point
    plt.figure(figsize=(15, 8))
    for i, (spell_name, damages) in enumerate(spell_damages.items()):
        # Scatter plot for individual damage points
        y = damages
        x = [i] * len(damages)  # Same x value for the same spell
        plt.scatter(x, y, label=spell_name)

    # Create a legend and label the axes
    plt.legend(title='Spell Name')
    plt.xlabel('Spell')
    plt.ylabel('Damage Amount')
    plt.title('Individual Damage by Spell')
    
    # Set the x-axis ticks to the spell names
    plt.xticks(range(len(spell_damages)), list(spell_damages.keys()), rotation=45)
    
    plt.tight_layout()
    plt.show()



def main():
    log_location = '/Applications/World of Warcraft/_classic_era_/Logs/WoWCombatLog-010724_124228.txt'
    log_lines = read_combat_log(log_location)
    events = parse_log_lines(log_lines)
    self_events = filter_for_self(events)

    # Plotting
    damage_data = process_damage_data(self_events)
    plot_damage_over_time(damage_data)
    plot_attack_sequence(self_events)
    plot_total_damage_by_spell(self_events)

if __name__ == "__main__":
    main()
