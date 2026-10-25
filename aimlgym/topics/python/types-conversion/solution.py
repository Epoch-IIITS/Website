r"""Reference solution for PY-03 Types and Conversion.

Each text is converted with the function for its target type. The total is computed with
floats, then rounded only for display, so `total` keeps full precision. `str(quantity)` turns
the number back into text before it is joined with `" items"`.
"""
price_text = "19.99"
quantity_text = "3"
discount_text = "0.1"

price = float(price_text)
quantity = int(quantity_text)
discount = float(discount_text)
total = price * quantity * (1 - discount)
total_rounded = round(total, 2)
label = str(quantity) + " items"

print(f"Total: {total_rounded}")
print(f"price is {type(price).__name__}")
print(f"quantity is {type(quantity).__name__}")
print(label)
