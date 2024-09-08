import random
import string
import json

# Function to generate a single coupon code
def generate_coupon_code(length=8):
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

# Generate 1000 unique coupon codes
coupon_codes = [generate_coupon_code() for _ in range(1000)]

# Structure it as a JSON list
coupon_data = {"coupons": coupon_codes}

# Write the result to a JSON file (optional, or just copy the output)
with open('coupons.json', 'w') as json_file:
    json.dump(coupon_data, json_file, indent=4)

# If you just need to copy/paste, print the list
print(json.dumps(coupon_data, indent=4))
