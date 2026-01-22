import json

summary = {
    "asset_cost_rule": "largest numeric value >= 5 digits",
    "horsepower_rule": "regex (XX HP)",
    "dealer_location": "upper half of document",
    "signature_location": "lower half",
    "stamp_location": "lower-right quadrant"
}

with open("../pseudo_labels/summary_stats.json", "w") as f:
    json.dump(summary, f, indent=2)

print("Summary rules written.")
