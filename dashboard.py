import hashlib
from datetime import datetime

blockchain = []

blocked_transactions = 0
flagged_transactions = 0
total_transactions = 0


def calculate_risk(amount, tx_count, new_wallet, mixer_used, country_risk):
    risk_score = 0

    if amount > 10000:
        risk_score += 25

    if tx_count > 10:
        risk_score += 20

    if new_wallet == "yes":
        risk_score += 15

    if mixer_used == "yes":
        risk_score += 30

    if country_risk == "high":
        risk_score += 20

    return min(risk_score, 100)


def detect_fraud(risk_score):
    global blocked_transactions
    global flagged_transactions

    if risk_score >= 70:
        blocked_transactions += 1
        return "HIGH RISK - BLOCKED"

    elif risk_score >= 40:
        flagged_transactions += 1
        return "MEDIUM RISK - FLAGGED"

    else:
        return "LOW RISK - APPROVED"


def create_block(sender, receiver, amount, risk_score, status):
    previous_hash = blockchain[-1]["hash"] if blockchain else "0"
    timestamp = str(datetime.now())

    block_data = (
        sender + receiver + str(amount) + str(risk_score)
        + status + previous_hash + timestamp
    )

    block_hash = hashlib.sha256(block_data.encode()).hexdigest()

    block = {
        "transaction_id": len(blockchain) + 1,
        "sender": sender,
        "receiver": receiver,
        "amount": amount,
        "risk_score": risk_score,
        "status": status,
        "time": timestamp,
        "previous_hash": previous_hash,
        "hash": block_hash
    }

    blockchain.append(block)


def display_dashboard():
    print("\n==============================================")
    print(" CRYPTOCURRENCY FRAUD ANALYTICS DASHBOARD")
    print("==============================================")
    print("Total Transactions :", total_transactions)
    print("Blocked Transactions :", blocked_transactions)
    print("Flagged Transactions :", flagged_transactions)

    if total_transactions > 0:
        detection_rate = (
            (blocked_transactions + flagged_transactions)
            / total_transactions
        ) * 100
        print("Suspicious Detection Rate :", round(detection_rate, 2), "%")

    print("\nRecent Transactions")
    print("----------------------------------------------")

    for block in blockchain:
        print("Transaction ID :", block["transaction_id"])
        print("Sender         :", block["sender"])
        print("Receiver       :", block["receiver"])
        print("Amount         :", block["amount"], "USDT")
        print("Risk Score     :", block["risk_score"])
        print("Status         :", block["status"])
        print("----------------------------------------------")


while True:
    print("\nCryptocurrency Fraud Detection using DLA")

    sender = input("Enter Sender Wallet Address: ")
    receiver = input("Enter Receiver Wallet Address: ")
    amount = float(input("Enter Transaction Amount: "))
    tx_count = int(input("Number of transactions in last hour: "))

    new_wallet = input(
        "Is sender wallet newly created? yes/no: "
    ).lower()

    mixer_used = input(
        "Was crypto mixer used? yes/no: "
    ).lower()

    country_risk = input(
        "Country risk low/high: "
    ).lower()

    total_transactions += 1

    risk = calculate_risk(
        amount, tx_count, new_wallet, mixer_used, country_risk
    )

    result = detect_fraud(risk)

    create_block(
        sender, receiver, amount, risk, result
    )

    print("\nTransaction Analysis")
    print("Risk Score :", risk)
    print("Decision :", result)
    print("Transaction Hash :", blockchain[-1]["hash"][:25])

    choice = input(
        "\nDo you want to analyse another transaction? yes/no: "
    ).lower()

    if choice != "yes":
        break


display_dashboard()