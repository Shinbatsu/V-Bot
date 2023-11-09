from riotwatcher import LolWatcher #'pip install riotwatcher' in Anaconda prompt
import os

##--------- LOAD CONFIG DATA ---------##
# You can replace this with your API key, I just keep mine outside of repo directory
api_key = "RGAPI-c6eb0375-41f7-4dc7-8538-00a6703241f1"

lol_watcher = LolWatcher(api_key) #Tell Riot Watcher to use LoL functions with the API key


##--------- SET PLAYER PARAMETERS ---------##
player_name= 'nnif'
player_region= 'RU'.lower() #[BR1, EUN1, EUW1, JP1, KR, LA1, LA2, NA1, OC1, TR1, RU]  
player_routing= 'americas'

##--------- CREATE PLAYER OBJECT ---------##
# This is equivalent to going to /riot/account/v1/accounts/by-riot-id/
summoner= lol_watcher.summoner.by_name(player_region, player_name)
print('Player info= \n',summoner)