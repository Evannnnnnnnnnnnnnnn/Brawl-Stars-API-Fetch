if __name__ == '__main__' :
    print('\nStarting ...\n') # Clear Terminal

import csv
import os
import subprocess
import sys
from datetime import datetime

import dotenv # python-dotenv
import requests
from tqdm import tqdm

Club_path = "E:\Jutage\Brawl Stars API Fetch"

dotenv.load_dotenv()

#Check current Wifi
WIFIs = ['Chargement...', 'Freebox-31AE69']

current_wifi = str(subprocess.check_output("netsh wlan show interfaces"))
connected = False
for wifi in WIFIs :
    if wifi in  current_wifi:
        print(f'Connected to {wifi}\n')
        api_key = os.getenv(wifi)
        connected = True
        break
    else : continue

if not connected : sys.exit("Not connected to correct Wifi")

# For API
Club_Tag = '2CURLUUGQ'

api_url_club = f'https://api.brawlstars.com/v1/clubs/%23{Club_Tag}'

headers = {'Authorization': 'Bearer ' + api_key}
response_club = requests.get(api_url_club, headers=headers)

if not response_club.status_code == 200 :
    sys.exit(f'Club : Error{response_club.status_code}')
Infos_club = response_club.json()

date = datetime.now().strftime("%d/%m/%Y")
hour = datetime.now().strftime("%Hh %M")

# We check the first csv
if not os.path.exists(os.path.join(Club_path,'Club Member Infos.csv')):
    enough_data = False
    with open(os.path.join(Club_path,'Club Member Infos.csv'), mode='w', newline='', encoding="utf-8") as csv_file :
        csv_writer = csv.writer(csv_file)
else :
    with open(os.path.join(Club_path,'Club Member Infos.csv'), mode ='r', encoding="utf-8") as csv_file :
        Old_Club_csv = csv.reader(csv_file)
        Old_Club_List = []
        for line in Old_Club_csv :
            Old_Club_List.append(line)
    for i in Old_Club_List :
        if date == i[0] :
            sys.exit('Already made Today')
            pass
    # We check if there is enough data to do comparison
    check_counter = 0
    while check_counter != 2 :
        for i in range(len(Old_Club_List)) :
            if Old_Club_List[-(i+1)][0] == "Date" :
                check_counter += 1
                if check_counter == 2 :
                    enough_data = True
                    break
            enough_data = False


# We get the info
nb_of_brawlers = 0
i = 0
Club_List = []
Players_List = []

for member in tqdm(Infos_club['members'], desc = 'Getting info ') :
    Club_List.append([date + ' - '+hour, i+1, member['name'], member['role'], date, member['trophies'], 0, 0, member['tag']])

    Player_Tag = member['tag'].replace('#', '')
    api_url_player = f'https://api.brawlstars.com/v1/players/%23{Player_Tag}'
    response_player = requests.get(api_url_player, headers=headers)
    if not response_player.status_code == 200 :
        print(f'Player {member['name']} : Error{response_player.status_code}')
    Infos_player = response_player.json()
    Players_List.append(Infos_player)
    if len(Players_List[i]['brawlers']) > nb_of_brawlers :
        nb_of_brawlers = len(Players_List[i]['brawlers'])
        member_with_most_brawlers = member['name']
    

    Additional_Info = [Infos_player["3vs3Victories"],Infos_player["soloVictories"],Infos_player["duoVictories"],Infos_player["expPoints"],Infos_player["highestTrophies"]]

    for item in Additional_Info :
        Club_List[i].append(item)
    i += 1

# We get the list of all the brawlers (it is gotten by the member with the most brawlers)
Brawlers_List = []
for player in Players_List :
    if member_with_most_brawlers == player['name'] :
        for brawler in player['brawlers'] :
            Brawlers_List.append(brawler['name'])
        break

# We add the brawlers to the header of the csv
csv_list = ['Date', 'Rang', 'Nom', 'Role', 'Ancienneté', 'Trophées', 'Mégapig Fait', 'Tickets Utilisés','Player Tag', '3v3 Win', 'Solo Win', 'Duo Win', 'Tot Exp', 'Max Trophées']
for brawler in Brawlers_List :
    csv_list.append(brawler)

# We get the info of trophies of each brawlers for each players, if they don't have the brawler, it is 0
for i, player in enumerate(Players_List) :
    for j, brawler in enumerate(Brawlers_List) :
        for brawler_owned in player['brawlers'] :
            if brawler == brawler_owned['name'] :
                Club_List[i].append(brawler_owned['trophies'])
                owned = True
                break
            owned = False
        if not owned :
            Club_List[i].append(0)
        
if not enough_data :
    # We write the data to the csv
    with open('Club Member Infos.csv', 'a', newline='', encoding="utf-8") as csv_file :
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(csv_list)
        csv_writer.writerows(Club_List)
    sys.exit(0)




num_of_members = len(Club_List)
num_of_old_members = int(Old_Club_List[-1][1])

# We get the list of all the member that didn't change clan and the new members
kept_members_list = []
new_members = []
for player in Club_List :
    for i in range(num_of_old_members) :
        if player[2] == Old_Club_List[-(i+1)][2]:
            kept_members_list.append(Old_Club_List[-(i+1)][2])
            player[4] = Old_Club_List[-(i+1)][4]
            player[6] = Old_Club_List[-(i+1)][6]
            player[7] = Old_Club_List[-(i+1)][7]
            old_member = True
            break
        old_member = False
    if not old_member :
        new_members.append(player[2])


quitting_members = []
for i in range(num_of_old_members) :
    for member in kept_members_list :
        if member == Old_Club_List[-(i+1)][2] :
            member_kept = True
            break
        member_kept = False
    if not member_kept :
        quitting_members.append(Old_Club_List[-(i+1)][2])

tot_tr_now = Infos_club["trophies"]
tot_tr_old = 0
for i in range(num_of_old_members) :
    tot_tr_old += int(Old_Club_List[-(i+1)][5])
tot_tr_diff = tot_tr_now - tot_tr_old

# We write the data to the first csv
with open(os.path.join(Club_path,'Club Member Infos.csv'), 'a', newline='', encoding="utf-8") as csv_file :
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(csv_list)
    csv_writer.writerows(Club_List)

api_url_ranking_fr = 'https://api.brawlstars.com/v1/rankings/fr/clubs'
response_ranking_fr = requests.get(api_url_ranking_fr, headers=headers)

if not response_ranking_fr.status_code == 200 :
    sys.exit(f'Ranking FR : Error{response_ranking_fr.status_code}')
Infos_ranking_fr = response_ranking_fr.json()

for club in Infos_ranking_fr["items"] :
    if club['name'] == Infos_club["name"] :
        rank_fr = club["rank"]
        break
else : 
    rank_fr = rank_global = 'Unranked'

if not rank_fr == 'Unranked' :
    print('global')
    api_url_ranking_global = 'https://api.brawlstars.com/v1/rankings/global/clubs'
    response_ranking_global = requests.get(api_url_ranking_global, headers=headers)

    if not response_ranking_global.status_code == 200 :
        sys.exit(f'Ranking Global : Error{response_ranking_global.status_code}')
    Infos_ranking_global = response_ranking_global.json()

    for club in Infos_ranking_global["items"] :
        if club['name'] == Infos_club["name"] :
            rank_fr = club["rank"]
            break
    else : 
        rank_fr = rank_global = 'Unranked'

# We check the second csv
if not os.path.exists(os.path.join(Club_path,'Club Infos.csv')):
    with open('Club Infos.csv', mode='w', newline='', encoding="utf-8") as csv_file :
        csv_writer = csv.writer(csv_file)

# We write the data to the second csv
with open(os.path.join(Club_path,'Club Infos.csv'), 'a', newline='', encoding="utf-8") as csv_file :
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["Date", "Nom du Club", "Club Tag", "Description", "Trophées Total", "Nombre de membres", "Membres Sortant", "Membres Entrant", "Difference de TR", "Rang FR", "Rang Global", "Top Member", "Bot Member"])
    csv_writer.writerow([date+' - '+hour, Infos_club["name"], Infos_club["tag"], Infos_club["description"], Infos_club["trophies"], len(Infos_club["members"]), quitting_members, new_members, tot_tr_diff, rank_fr, rank_global, Infos_club['members'][0]["name"], Infos_club['members'][-1]["name"]])

