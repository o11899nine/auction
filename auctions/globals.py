# Function to sort the list
def Sort_Tuple(tup):

    # reverse = None (Sorts in Ascending order)
    # key is set to sort using first element of
    # sublist lambda has been used
    return (sorted(tup, key=lambda x: x[0]))

categories = (
    ('Instruments', 'Instruments'),
    ('Books', 'Books'),
    ('Gaming', 'Gaming'),
    ('Clothing', 'Clothing'),
    ('Appliances', 'Appliances'),
)

CATEGORIES = Sort_Tuple(categories)


PLACEHOLDER_IMG = "https://lh3.googleusercontent.com/EbXw8rOdYxOGdXEFjgNP8lh-YAuUxwhOAe2jhrz3sgqvPeMac6a6tHvT35V6YMbyNvkZL4R_a2hcYBrtfUhLvhf-N2X3OB9cvH4uMw=w1064-v0"

POST_ICON = '<i class="material-icons" style="font-size:1rem;color:white">send</i>'
BID_ICON = '<i class="material-icons" style="font-size:1rem;color:white">gavel</i>'