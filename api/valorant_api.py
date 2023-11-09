# Get the most recent Ranked match in a user's history,
# and print the ranks of every player in the match. If
# there isn't a Ranked match in the history, the program
# will exit. **This example requires an API Key with access
# to the match endpoint. You need to apply for that from
# the Riot Games Developer Portal.**

# # 1rvVEjMUHyndj1R0sILDbfueVJLmJkFuhGntYszq2udSoWcG5eJmxGsrZoZ8AlL5Ked-zo63tmItHA
# # zwI-vGXN9grKVLVS0CkcNVMwv8pmURAgd6JiirGl-FD6uBf6Hgm2SODjEEaltwousG4TeAtHKK-1TA
# Get a user by name and tagline.

import os
import valorant


client = valorant.Client("RGAPI-c6eb0375-41f7-4dc7-8538-00a6703241f1", locale="en-US")

# Get a user by name and tagline.
account = client.get_user_by_name("frissyn#6969")

# Find their most recent Ranked match.
# This will raise an error if your API Key does not have match access.
match = account.matchlist().history.find(queueId="competitive")

# Check if the match exists.
if match == None:
    print("No Ranked match in recent history!")
    exit(1)
else:
    match = match.get()

# Print everyone's ranks.
for team in match.teams:
    print(f"{team.teamId} Team's Ranks: ")

    # Find all the players on the same team.
    players = match.players.get_all(teamId=team.teamId)

    for player in players:
        print(f"\t{player.gameName} - {player.rank}")