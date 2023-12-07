import json
from datetime import datetime, timedelta

# Accept an argument which is the customer check-in date with the format: YYYY-MM-DD
input = input("Please enter your desired check-in date in YYYY-MM-DD format: ")
input_date=datetime.strptime(input,"%Y-%m-%d") #convert input string to date format


# Load the input.json file
input_file = open("input.json","r")
input_data = json.load(input_file)


# Filter Function
def filter_offers(input_date, input_data):
    valid_category_id = {1,2,4} #Restaurant, Retail or Activity
    filtered_offers = []

    for offer in input_data["offers"]:
        valid_to=datetime.strptime(offer["valid_to"],"%Y-%m-%d") #convert valid_to string to date format
        # filter Offers with valid category and Offer needs to be valid till checkin date + 5 days.
        if (offer["category"] in valid_category_id and input_date <= valid_to + timedelta(days=5)):
            # If an offer is available in multiple merchants, only select the closest merchant
            offer["merchants"] = sorted(offer["merchants"], key=lambda x:x["distance"], reverse=False)
            offer["merchants"] = offer["merchants"][:1]
            filtered_offers.append(offer)

    # Return 2 offers in different categories. If there are multiple offers in the same category give priority to the closest merchant offer.
    sorted_filtered_offers = sorted(filtered_offers, key = lambda x:(x["category"], x["merchants"][0]["distance"]), reverse=False)    
    final_offers = []
    categories = set()

    for offer in sorted_filtered_offers:
        if len(final_offers) == 2:
            break
        if offer["category"] not in categories:
            final_offers.append(offer)
            categories.add(offer["category"])

    return {"offers": final_offers}

# save the filtered offers to a file output.json (stored at the root of the project)
output_data = json.dumps(filter_offers(input_date,input_data), indent=1)
f = open("output.json", "x")
f.write(output_data)

# print(output_data)