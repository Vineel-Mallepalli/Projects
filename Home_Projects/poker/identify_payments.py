from decimal import *
from _collections import defaultdict
from requests import get
from bs4 import BeautifulSoup
import json

import pandas as pd
import os


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
    payouts = _apply_alg(nets)
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


# make sure header in csv file
def parse_log_pokernow(url="", path=""):
    parsed_log = _read_pokernow_log(url, path)
    # identify only cash-in/out events
    cash_flow_events = reversed([event for event in parsed_log if "quits" in event or "created" in event
                                 or "approved" in event or "updated" in event or "queued" in event])
    net_amts = _analyze_cash_flow_events(cash_flow_events)
    net_amts = _condense_player_net_amts(net_amts)
    instructions = _create_instructions(net_amts)
    net = _calc_net_amt_unaccounted(instructions)
    print(*_order_instructions(instructions), sep="\n")
    print("net amt unaccounted for: {}".format(net))
    return


# Input example: "Vineel = 10 70.75; Liam = 20 9.20"
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


# Does not require list to be sorted, but helps with efficiency.
# Requires: list amounts are net-zero
def _apply_alg(nets):
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


def _condense_player_net_amts(player_net_dict):
    new_player_net_dict = defaultdict(lambda: (0, False))
    for player, amt_status_tup in player_net_dict.items():
        new_player_net_dict[player.partition(" @")[0]] = new_player_net_dict[player.partition(" @")[0]][0] + \
                                                         amt_status_tup[0], amt_status_tup[1]
    return new_player_net_dict


def _order_instructions(instructions):
    unrecorded_instructions = [instruction for instruction in instructions if "has NOT been recorded" in instruction]
    new_instructions = [instruction for instruction in instructions if instruction not in unrecorded_instructions]
    new_instructions.extend(unrecorded_instructions)
    return new_instructions


def _read_pokernow_log(url="", path=""):
    # if url[:8] != 'https://':
    #     print("ERROR: provided url does not begin with 'https://'")
    #     return
    # partition = url[8:].partition('/')
    # print("Partition: " + str(partition))
    # path = '/' + partition[2] + '/log?after_at=&before_at=&mm=false'
    # print("Path: " + path)
    # Path: /games/X9_g14w8Lh5C0FWBWiOcU0KCI/log?after_at=&before_at=&mm=false
    if url != "":  # download log file from url, save locally, and record saved path.
        if url[-1] != '/':
            url += '/'
        url += "log?after_at=&before_at=&mm=false"
        print(url)
        # LOL remove if-none-match header and it works! RIP only if website still works in browser. time limit>
        # which headers are variable across time, games, devices ???
        headers = {'authority': 'www.pokernow.club', 'method': 'GET',
                   'path': '/games/X9_g14w8Lh5C0FWBWiOcU0KCI/log?after_at=&before_at=&mm=false', 'scheme': 'https',
                   'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,'
                             'application/signed-exchange;v=b3;q=0.9',
                   'accept-encoding': 'gzip, deflate, br', 'accept-language': 'en-US,en;q=0.9,la;q=0.8',
                   'cache-control': 'max-age=0',
                   'cookie': '_ga=GA1.2.950321394.1584684318; npt=0UOAghgzdRJUrFy8jyWS7Es7_VFRFwyHd9vcOajxyqQXlzYfjE; '
                             '_gid=GA1.2.38041500.1591509743',
                   # 'if-none-match': 'W/"2cd7-bIjRNkdg9Hyq+FLIxgYKUAN6eeQ"',
                   'sec-fetch-dest': 'document',
                   'sec-fetch-mode': 'navigate', 'sec-fetch-site': 'none', 'sec-fetch-user': '?1',
                   'upgrade-insecure-requests': '1',
                   'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                 'Chrome/81.0.4044.138 Safari/537.36'}
        r = get(url, headers=headers)  # stream = True ?
        # print(r.headers)
        print(r.content)
        soup = BeautifulSoup(r.content, 'html.parser')
        if len(soup.text) == 0:
            print("Website contains no content. Table may have expired. You may also need to refresh.")
            return
        dict_log = json.loads(soup.text)
        parsed_log = [log_item.get('msg') for log_item in dict_log["logs"]]
        print(dict_log['infos'])
        print(len(parsed_log))
    else:
        if path == "":
            path = input("Enter the path of your file: ")
        assert os.path.exists(path), "No file could be discovered at " + path
        csv = pd.read_csv(path)
        parsed_log = list(csv[csv.keys()[0]])
    return parsed_log


def _analyze_cash_flow_events(cash_flow_events):
    net_amts = defaultdict(lambda: (0, False))  # format = player : tuple(net, quit_status)
    for cash_flow_event in cash_flow_events:
        cash_in = True if "created" in cash_flow_event or "approved" in cash_flow_event else False
        cash_out = True if "quits the" in cash_flow_event else False
        queued_update = True if "queued" in cash_flow_event else False
        updating = True if "updated" in cash_flow_event else False
        player = cash_flow_event.split("\"")[1]
        if queued_update:  # potential error: player stack was modified while in play.
            print("WARNING: {} stack was modified mid play. Check manually. {}.".format(player, cash_flow_event))
        elif updating:  # adjust player stack if owner manually updates it
            split = cash_flow_event.rsplit(" ", 3)
            net_amts[player] = net_amts[player][0] - (int(split[3][:-1]) - int(split[1])), False
        else:
            amount = int(cash_flow_event.rsplit(" ", 1)[-1][:-1])
            if cash_in:
                net_amts[player] = net_amts[player][0] - amount, False
            if cash_out:
                net_amts[player] = net_amts[player][0] + amount, True
    return net_amts


def _create_instructions(net_amts):
    instructions = []
    for player, amt_status_tup in net_amts.items():
        keyword = "Pay "
        if amt_status_tup[1]:  # player has quit
            if amt_status_tup[0] < 0:
                keyword = "Request "
                amt_status_tup = -amt_status_tup[0], amt_status_tup[1]
            instructions.append(keyword + player + " " + str(amt_status_tup[0]))
        else:
            instructions.append("{} has a current net of {}. End amt has NOT been recorded in log."
                                .format(player, amt_status_tup[0]))
    return instructions


def _calc_net_amt_unaccounted(instructions):
    net = 0
    for instruction in instructions:
        if "End amt has NOT been recorded" in instruction:
            continue
        multiplier = 1 if "Request" in instruction else -1
        amt = int(instruction.rsplit(" ", 1)[-1])
        net += multiplier * amt
    return net


parse_log_pokernow(path="C:\\Users\\vinee\\PycharmProjects\\Home_Projects\\poker\\muthu_log.csv")
