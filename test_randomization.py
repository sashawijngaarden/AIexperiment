import random

C_ATTR_ID = ['Price', 'Quality', 'Sustainability', 'Nudge']

def test_attribute_order():
    remaining_attrs = [attr for attr in C_ATTR_ID if attr not in ['Price', 'Nudge']]
    random.shuffle(remaining_attrs)

    price_pos = random.choice([1, len(remaining_attrs)-1])
    remaining_attrs.insert(price_pos, 'Price')

    if random.choice([True, False]):
        final_attrs = ['Nudge'] + remaining_attrs
    else:
        final_attrs = remaining_attrs + ['Nudge']

    return final_attrs

# Run it 10 times to see the randomizations
for i in range(10):
    print(f"Trial {i+1}: {test_attribute_order()}")
    