from decimal import *
from _collections import defaultdict
from requests import get
from bs4 import BeautifulSoup
import json

import pandas as pd
import os


# Does not require list to be sorted, but helps with efficiency.
# Requires: list amounts are net-zero
def apply_alg(nets):
    if not nets or len(nets) == 0:
        return []
    payers = []
    receivers = []
    payouts = []
    for i in range(len(nets)):
        if nets[i] <= 0:
            payers.append(i)
        else:
            receivers.append(i)
    curr_rec = 0
    for payer in payers:
        payout = [payer, []]
        payer_amt = -1 * nets[payer]
        while payer_amt != 0:
            if payer_amt <= nets[receivers[curr_rec]]:
                payout[1].append((receivers[curr_rec], payer_amt))
                nets[receivers[curr_rec]] -= payer_amt
                payer_amt -= payer_amt
            else:
                payout[1].append((receivers[curr_rec], nets[receivers[curr_rec]]))
                payer_amt -= nets[receivers[curr_rec]]
                nets[receivers[curr_rec]] -= nets[receivers[curr_rec]]
            if nets[receivers[curr_rec]] == 0:
                curr_rec += 1
        payouts.append(payout)
    return payouts


# Parse result data from poker2 app and write instructions to excel file.
# Assumption: if no "Name" column, first column of data contains player names
# Requires: "Net" column
def parse_log_poker2(path=""):
    getcontext().prec = 106
    if path == "":
        path = input("Enter the path of your file: ")
    split_path = path.rsplit("\\", 1)
    filename = split_path[-1]
    directory = "".join(split_path[:-1]) + "\\"
    assert os.path.exists(path), "No file could be discovered at " + path
    xl = pd.ExcelFile(path)
    sheets = xl.sheet_names
    df = xl.parse(sheets[0])
    if "Net" not in df:
        print("No 'Net' column in data.")
        return
    if "Name" not in df:
        if df.columns.get_loc("Net") == 0:
            print("Name column missing and Net is first column in data")
            return
        df.rename(columns={list(df)[0]: "Name"}, inplace=True)
    df_trunc = df[["Name", "Net"]]  # new dataframe with only player names, net amounts
    print(df_trunc)
    df_trunc = df_trunc.reindex(df_trunc["Net"].abs().sort_values(ascending=False).index)
    print(df_trunc)
    names = [i for i in df_trunc["Name"].tolist()]
    nets = [Decimal(j).quantize(Decimal(".01"), rounding=ROUND_HALF_UP) for j in df_trunc["Net"].tolist()]
    if sum(nets) != 0:
        print("ERROR: amounts are not net-zero. sum = " + str(sum(nets)))
        return
    payouts = apply_alg(nets)
    out_payers = [names[payout[0]] for payout in payouts]
    out_rec_amts = [[names[rec_amt[0]] + "-" + str(rec_amt[1]) for rec_amt in payout[1]] for payout in payouts]
    instructions = []
    for i in range(len(out_payers)):
        for j in range(len(out_rec_amts[i])):
            instructions.append(out_payers[i] + " pays " + out_rec_amts[i][j].split("-")[0] + " $" + out_rec_amts[i][j].
                                split("-")[1])
    out_df = pd.DataFrame({"   Instructions": instructions})
    writer = pd.ExcelWriter(directory + "Results" + filename)
    out_df.to_excel(writer, 'Sheet1', index=False)
    writer.save()
    print("Number of Transactions = " + str(len(instructions)))
    return


def condense_player_net_dict(player_net_dict):
    new_player_net_dict = defaultdict(lambda: (0, False))
    for player, amt_status_tup in player_net_dict.items():
        new_player_net_dict[player.partition(" @")[0]] = new_player_net_dict[player.partition(" @")[0]][0] + \
                                                         amt_status_tup[0], amt_status_tup[1]
    return new_player_net_dict


def order_instructions(instructions):
    unrecorded_instructions = [instruction for instruction in instructions if "has NOT been recorded" in instruction]
    new_instructions = [instruction for instruction in instructions if instruction not in unrecorded_instructions]
    new_instructions.extend(unrecorded_instructions)
    return new_instructions


# noinspection PyArgumentList
def parse_log_pokernow(url="", path=""):
    if url != "":  # download log file from url, save locally, and record saved path.
        if url[-1] != '/':
            url += '/'
        url += "log?after_at=&before_at=&mm=false"
        print(url)
        headers = {'authority': 'www.pokernow.club', 'method': 'GET',
                   'path': '/games/X9_g14w8Lh5C0FWBWiOcU0KCI/log?after_at=&before_at=&mm=false', 'scheme': 'https',
                   'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,'
                             'application/signed-exchange;v=b3;q=0.9',
                   'accept-encoding': 'gzip, deflate, br', 'accept-language': 'en-US,en;q=0.9,la;q=0.8',
                   'cache-control': 'max-age=0', 'cookie': '_ga=GA1.2.950321394.1584684318; '
                                                           'npt=0UOAghgzdRJUrFy8jyWS7Es7_VFRFwyHd9vcOajxyqQXlzYfjE; '
                                                           '_gid=GA1.2.38041500.1591509743',
                   'if-none-match': 'W/"2a5d-wIKyH1EWNp0ckVm8/tdeEbzF/gc"', 'sec-fetch-dest': 'document',
                   'sec-fetch-mode': 'navigate', 'sec-fetch-site': 'none', 'sec-fetch-user': '?1',
                   'upgrade-insecure-requests': '1',
                   'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                 'Chrome/81.0.4044.138 Safari/537.36'}
        r = get(url, stream=True, headers=headers)
        print(r.headers)
        print(r.content)
        print(json.detect_encoding(r.content))
        print(len(r.content))
        soup = BeautifulSoup(r.content, 'html.parser')
        print(soup.findAll(text=True))

        # links = soup.findAll('a')
        # csv_links = [url + link['href'] for link in links]
        # print(csv_links)
        return

    # obtain path if not given, and read file at given path
    if path == "":
        path = input("Enter the path of your file: ")
    assert os.path.exists(path), "No file could be discovered at " + path
    csv = pd.read_csv(path)
    game_history = list(csv[csv.keys()[0]])
    # identify only cash-in/out events
    buy_in_out_list = [event for event in game_history if "quits the game" in event or "created the game" in event
                       or "approved the player" in event or "updated the " in event
                       or "stand up" in event or "sit back" in event or "admin queued the " in event]
    print(buy_in_out_list, len(buy_in_out_list), sep="\n")
    print([event for event in buy_in_out_list if "connahh " in event])
    player_net_dict = defaultdict(lambda: (0, False))  # format = player : tuple(net, quit_status)
    for i in range(len(buy_in_out_list) - 1, -1, -1):
        buy_in_out_event = buy_in_out_list[i]
        earnings = 1 if "quits the" in buy_in_out_event else -1
        rebuying = True if "approved the" in buy_in_out_event else False
        standing = True if "stand up" in buy_in_out_event else False
        sitting = True if "sit back" in buy_in_out_event else False
        queued_update = True if "admin queued the " in buy_in_out_event else False
        quitting = True if "quits the" in buy_in_out_event else False
        updating = True if "updated the " in buy_in_out_event else False
        player = buy_in_out_event.split("\"")[1]
        # if player[:6] == "connah":
        #     print(player, player_net_dict[player], quitting, buy_in_out_event)
        if queued_update:  # potential error: player stack was modified while in play.
            print("%s event %d." % (buy_in_out_event, i))
            continue
        if updating:  # adjust player stack if owner manually updates it
            split = buy_in_out_event.rsplit(" ", 3)
            old_amt, new_amt = int(split[1]), int(split[3][:-1])
            player_net_dict[player] = player_net_dict[player][0] - (new_amt - old_amt), quitting
            continue
        amount = int(buy_in_out_event.rsplit(" ", 1)[-1][:-1])
        if standing:  # set quit_status to true
            player_net_dict[player] = player_net_dict[player][0] + amount, True
            continue
        if sitting:
            player_net_dict[player] = player_net_dict[player][0] - amount, False
            continue
        if rebuying or not player_net_dict[player][1]:
            player_net_dict[player] = player_net_dict[player][0] + earnings * amount, quitting
    player_net_dict = condense_player_net_dict(player_net_dict)
    instructions = []
    for player, amount_status_tup in player_net_dict.items():
        keyword = "Pay "
        if amount_status_tup[1]:  # player has quit
            if amount_status_tup[0] < 0:
                keyword = "Request "
                amount_status_tup = -amount_status_tup[0], amount_status_tup[1]
            instructions.append(keyword + player + " " + str(amount_status_tup[0]))
        else:
            instructions.append("%s has a current net of %d. End amt has NOT been recorded in log."
                                % (player, amount_status_tup[0]))
    print(*order_instructions(instructions), sep="\n")
    return


def single_banker(player_data):
    list_player_data = player_data.split(";")[:-1]
    player_net_dict = {}
    for player_data in list_player_data:
        partition = player_data.partition("=")
        if partition[0].strip() not in player_net_dict:
            player_net_dict[partition[0].strip()] = [partition[2].strip()]
        else:
            val = player_net_dict[partition[0].strip()]
            val.append(partition[2].strip())
            player_net_dict[partition[0].strip()] = val
    # print(player_net_dict)
    for key, value_lst in player_net_dict.items():
        net = Decimal(0)
        for value in value_lst:
            if "paid" not in value:
                net += Decimal(value.partition(" ")[2]).quantize(Decimal(".01"), rounding=ROUND_HALF_UP) - \
                       Decimal(value.partition(" ")[0]).quantize(Decimal(".01"), rounding=ROUND_HALF_UP)
        player_net_dict[key] = net
    # print(player_net_dict)

    for key, value in player_net_dict.items():
        if isinstance(value, Decimal):
            keyword = "Pay "
            if value < 0:
                keyword = "Request "
                value = -value
            print(keyword + key + " " + str(value))
    return


parse_log_pokernow(url="https://www.pokernow.club/games/X9_g14w8Lh5C0FWBWiOcU0KCI")
# path="C:\\Users\\vinee\\PycharmProjects\\Home_Projects\\poker"
#      "\\poker_now_log_1kiOADt36erZKUvuixvj5f58N (5).csv")
# data = "Vineel = 10 70.75; Liam = 20 9.20; Muthu = 20 10.28; Will = 20 0; Eric = 7 13.03; Varun = 20 1.62; " \
#        "Vaidya = 10 3.36; Cole = 10 15.90; Nolan = 7 paid; Liam = 35 0; Vineel = 15 51.69; Cole = 30 29.75; " \
#        "Will = 15 31.94; Connor = 10 10.62; Jacob = 10 1.0; Vaidya = 10 0;"
# single_banker(data)
# <button class="button-1 show-log-button small-button dark-gray" type="button">Log</button>
# <button type="button" class="button-1 green small-button">Download Full Log</button>
# https://www.pokernow.club/games/lO84l_qsLt0THXYxJW4dlsvpo/log?after_at=&before_at=&mm=false
# https://www.pokernow.club/games/lO84l_qsLt0THXYxJW4dlsvpo/log?after_at=&before_at=&mm=false
