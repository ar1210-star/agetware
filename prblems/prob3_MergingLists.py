def get_overlap(a, b):
    leftA, rightA = a["positions"]
    leftB, rightB = b["positions"]
    overlap = min(rightA, rightB) - max(leftA, leftB)
    lengthA = rightA - leftA
    lengthB = rightB - leftB
    return overlap, lengthA, lengthB

def combine_lists(list1, list2):
    combined = []
    used = set()

    for i, a in enumerate(list1):
        merged = False
        for j, b in enumerate(list2):
            if j in used:
                continue
            overlap, lenA, lenB = get_overlap(a, b)
            if overlap > lenA / 2 or overlap > lenB / 2:
                new_item = {
                    "positions": a["positions"] if a["positions"][0] <= b["positions"][0] else b["positions"],
                    "values": a["values"] + b["values"]
                }
                combined.append(new_item)
                used.add(j)
                merged = True
                break
        if not merged:
            combined.append(a)

    for j, b in enumerate(list2):
        if j not in used:
            combined.append(b)

    combined.sort(key=lambda x: x["positions"][0])
    return combined

list1 = [
    {"positions": [10, 50], "values": ["A"]},
    {"positions": [60, 100], "values": ["B"]}
]

list2 = [
    {"positions": [20, 40], "values": ["X"]},
    {"positions": [70, 90], "values": ["Y"]},
    {"positions": [110, 130], "values": ["Z"]}
]

result = combine_lists(list1, list2)
print(result)
