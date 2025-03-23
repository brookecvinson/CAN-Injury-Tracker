from collections import Counter


class InjuryPriorityMultiset:
    def __init__(self):
        # counter to maintain the multiset
        self.counter = Counter()
        # list of items in order of priority, from highest to lowest
        self.priority_order = ['Open Wound', 'Closed Wound', 'Bruise', 'Redness', 'Other']

    def add(self, item):
        # adds an injury to the set
        if item in self.priority_order:
            self.counter[item] += 1
        else:
            raise ValueError(f"Invalid item: {item}")

    def remove(self, item):
        # removes an injury from the set
        if self.counter[item] > 0:
            self.counter[item] -= 1
        else:
            raise ValueError(f"Item not found: {item}")

    def get_highest_priority(self):
        # returns the injury with the highest priority, e.g., the one determining the color of the button
        for item in self.priority_order:
            if self.counter[item] > 0:
                return item
        return None  # If the multiset is empty


# Example usage:
"""
multiset = InjuryPriorityMultiset()
multiset.add('bruise')
multiset.add('open wound')
multiset.add('bruise')

print(multiset.get_highest_priority())  # Output: 'open wound'

multiset.remove('open wound')
print(multiset.get_highest_priority())  # Output: 'bruise'
"""