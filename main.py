import requests

from datetime import datetime, timezone


def get_channels():
    url = "https://api.sr.se/api/v2/channels?format=json"
    response = requests.get(url)
    data = response.json()
    channels = data['channels']
    
    return [(channel['id'], channel['name']) for channel in channels]

# hämta tablån för en specifik kanal
def get_schedule(channel_id):
    
    url = f"https://api.sr.se/api/v2/scheduledepisodes?channelid={channel_id}&format=json&size=10"
    response = requests.get(url)
    data = response.json()
    episodes = data['schedule']
    
    return episodes

# omvandla UNIX-tidsstämpeln från API till ett läsbart format
def convert_time(time_string):
    
    timestamp = int(time_string[6:-2]) // 1000
    readable_time = datetime.fromtimestamp(timestamp, tz=timezone.utc).strftime('%H:%M')
    return readable_time

def main():
    channels = get_channels()
    
    print("Menu – Choose a radio station:")
    for i, (channel_id, channel_name) in enumerate(channels, 1):
        print(f"{i}. {channel_name}")

    choice = int(input("\n### Choice? "))
    if 1 <= choice <= len(channels):
        chosen_channel_id, chosen_channel_name = channels[choice - 1]
        print(f"\nShowing the next 10 programs for {chosen_channel_name}:\n")

        episodes = get_schedule(chosen_channel_id)
        for episode in episodes:
            start_time = convert_time(episode['starttimeutc'])
            title = episode['title']
            print(f"* {start_time} – {title}")
    else:
        print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
