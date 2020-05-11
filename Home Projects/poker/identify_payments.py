from decimal import *
import pandas as pd
import os


# Assumption: if no "Name" column, first column of data contains player names
# Requires: "Net" column
def get_data():
    getcontext().prec = 106
    path = input("Enter the path of your file: ")
    split_path = path.rsplit("\\", 1)
    filename = split_path[-1]
    directory = "".join(split_path[:-1]) + "\\"
    assert os.path.exists(path), "No file could be discovered at " + path
    xl = pd.ExcelFile(path)
    sheets = xl.sheet_names
    df = xl.parse(sheets[0])
    if "Net" not in df:
        print("'Net' column missing from data")
        return
    if "Name" not in df:
        if df.columns.get_loc("Net") == 0:
            print("Name column missing and Net is first column in data")
            return
        df.rename(columns={list(df)[0]: "Name"}, inplace=True)
    df_trunc = df[["Name", "Net"]]  # new dataframe with only player names, net amounts
    df_trunc = df_trunc.reindex(df_trunc["Net"].abs().sort_values(ascending=False).index)
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
    payers.sort()
    receivers.sort()
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


get_data()
