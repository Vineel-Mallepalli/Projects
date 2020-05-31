from decimal import *
from _collections import defaultdict
import pandas as pd
import os


# Parse result data from poker2 app and write instructions to excel file.
# Assumption: if no "Name" column, first column of data contains player names
# Requires: "Net" column
def get_data_poker2(path=""):
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
    # print("Before: ", player_net_dict)
    new_player_net_dict = defaultdict(lambda: (0, False))
    for player, amt_status_tup in player_net_dict.items():
        new_player_net_dict[player.partition(" @")[0]] = new_player_net_dict[player.partition(" @")[0]][0] + \
                                                         amt_status_tup[0], amt_status_tup[1]
    # print("After: ", new_player_net_dict)
    return new_player_net_dict


def order_instructions(instructions):
    unrecorded_instructions = [instruction for instruction in instructions if "has NOT been recorded" in instruction]
    new_instructions = [instruction for instruction in instructions if instruction not in unrecorded_instructions]
    new_instructions.extend(unrecorded_instructions)
    return new_instructions


# need to check what log and program do if owner manually changes player's stack.
def get_data_pokernow(path=""):
    if path == "":
        path = input("Enter the path of your file: ")
    assert os.path.exists(path), "No file could be discovered at " + path
    csv = pd.read_csv(path)
    game_history = list(csv[csv.keys()[0]])
    buy_in_out_list = [event for event in game_history
                       if "quits the game" in event or "created the game" in event or "approved the player" in event]
    # print(buy_in_out_list, len(buy_in_out_list), sep="\n")
    # print([event for event in buy_in_out_list if "vaid" in event])
    player_net_dict = defaultdict(lambda: (0, False))  # player : tuple(net, has_quit)
    for i in range(len(buy_in_out_list) - 1, -1, -1):
        buy_in_out_event = buy_in_out_list[i]
        earnings = 1 if "quits the" in buy_in_out_event else -1
        quitting = True if "quits the" in buy_in_out_event else False
        amount = int(buy_in_out_event.rsplit(" ", 1)[-1][:-1])
        player = buy_in_out_event.split("\"")[1]
        # check what happens if player has quit before but is now buying back in. does NOT provide player a new @ hash.
        if player_net_dict[player][1] and quitting:  # error check: player has already quit and is trying to quit again.
            print("Error: player %s has quit and is now performing %s event %d" % (player, buy_in_out_event, i))
            return
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


get_data_pokernow("C:\\Users\\vinee\\PycharmProjects\\Home Projects\\poker\\poker_test_log_2.csv")
data = "Vineel = 10 70.75; Liam = 20 9.20; Muthu = 20 10.28; Will = 20 0; Eric = 7 13.03; Varun = 20 1.62; " \
       "Vaidya = 10 3.36; Cole = 10 15.90; Nolan = 7 paid; Liam = 35 0; Vineel = 15 51.69; Cole = 30 29.75; " \
       "Will = 15 31.94; Connor = 10 10.62; Jacob = 10 1.0; Vaidya = 10 0;"
# single_banker(data)
