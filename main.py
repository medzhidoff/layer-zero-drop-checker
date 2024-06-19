import csv
import requests

wallets_csv = csv.DictReader(open('./wallets.csv'))

result = []

for wallet in wallets_csv:
    wallet_address = wallet['wallet_address']
    url = f"https://www.layerzero.foundation/api/allocation/{wallet_address}"
    response = requests.get(url)
    if response.status_code in [404, 400]:
        comment = "NOT ELIGIBLE"
        amount = 0
    else:
        data = response.json()
        comment = "ELIGIBLE" if data['isEligible'] else "NOT ELIGIBLE"
        amount = float(data['zroAllocation']['asString'])
    result.append(dict(
        wallet_address=wallet_address,
        comment=comment,
        amount=amount
    ))

with open('result.csv', 'w') as csvfile:
    # creating a csv dict writer object
    writer = csv.DictWriter(csvfile, fieldnames=[
        'wallet_address',
        'comment',
        'amount',
    ])
    writer.writeheader()
    writer.writerows(result)
