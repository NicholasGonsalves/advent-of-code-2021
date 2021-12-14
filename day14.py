"""Day 14."""


def read_file(file_name: str):
    """Read file and parse input."""
    with open(file_name) as f:
        inputs = f.read().splitlines()
    lines = [i for i in inputs]
    template = lines[0]
    rules = [rule.split(' -> ') for rule in lines[2:]]
    return template, rules


def get_pairs(polymer):
    """For a list of characters (a polymer), split into overlapping pairs."""
    pairs = []
    for i in range(len(polymer)-1):
        pairs.append(f"{polymer[i]}{polymer[i+1]}")
    return pairs


def insert_base(pair, base):
    """Given a polymer pair, return the new polymer of length 3."""
    return f"{pair[0]}{base}{pair[1]}"


def update_base_count(base, count, base_counts):
    """Increase the 'base_count' for the given 'base' by 'count'."""
    if base not in base_counts:
        base_counts[base] = count
    else:
        base_counts[base] += count
    return base_counts


def update_polymer_count(count, new_polymer, new_polymers):
    """Update the number of each base pair in the polymer after the new polymer is added."""
    for new_pair in get_pairs(new_polymer):
        if new_pair not in new_polymers:
            new_polymers[new_pair] = count
        else:
            new_polymers[new_pair] += count
    return new_polymers


def step(polymer_counts, base_counts, rules):
    """A single step in the simulation."""
    new_polymers_counts = {}

    for pair, count in polymer_counts.items():
        new_base = rules.get(pair)
        new_polymer = insert_base(pair, new_base)
        base_counts = update_base_count(new_base, count, base_counts)
        new_polymers_counts = update_polymer_count(count, new_polymer, new_polymers_counts)

    return new_polymers_counts, base_counts


def run_simulation(num_steps, rules, template):
    # Initialise rules lookup
    rules = {rule[0]: rule[1] for rule in rules}

    # Initialise base counts (the count of each character in the full polymer)
    base_counts = {}
    for base in template:
        base_counts = update_base_count(base, 1, base_counts)

    # Initialise polymer counts (the count of each pair in the full polymer)
    polymer_counts = {}
    for pair in get_pairs(template):
        polymer_counts = update_polymer_count(1, pair, polymer_counts)

    # Run simulation for num_steps
    for _ in range(num_steps):
        polymer_counts, base_counts = step(polymer_counts, base_counts, rules)

    # Return difference between number of most common and least common bases
    return max(base_counts.values()) - min(base_counts.values())


def part_one(template, rules):
    return run_simulation(10, rules, template)


def part_two(template, rules):
    return run_simulation(40, rules, template)


if __name__ == "__main__":
    data1, data2 = read_file("day14.txt")

    print(part_one(data1, data2))
    print(part_two(data1, data2))
