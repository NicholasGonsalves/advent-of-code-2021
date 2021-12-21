"""Day 16."""


def read_file(file_name: str):
    """Read file and parse input."""
    with open(file_name) as f:
        inputs = f.read()
    return inputs


def get_literal_packet_value(packet_data):
    binary_str = ""
    remaining_packet = ""
    for i in range(0, len(packet_data), 5):
        binary_str += packet_data[i+1:i+5]
        if packet_data[i] == '0':
            remaining_packet = packet_data[i+5:]
            break
    return int(binary_str, 2), remaining_packet


def apply_operator(values, type_id):
    if type_id == 0: return sum(values)
    if type_id == 1:
        prod = 1
        for val in values:
            prod *= val
        return prod
    if type_id == 2: return min(values)
    if type_id == 3: return max(values)
    if type_id == 5:
        if values[0] > values[1]:
            return 1
        else:
            return 0
    if type_id == 6:
        if values[0] < values[1]:
            return 1
        else:
            return 0
    if type_id == 7:
        if values[0] == values[1]:
            return 1
        else:
            return 0


def parse_packet(binary, literals=None):
    if literals is None:
        literals = [[]]

    if not binary or (int(binary) == 0):
        return binary, literals

    type_id = int(binary[3:6], 2)
    packet_data = binary[6:]

    # Literals
    if type_id == 4:
        literal, packet_data = get_literal_packet_value(packet_data)
        literals[-1].append(literal)
        return packet_data, literals

    # Operator packet
    length_type_id = packet_data[0]
    if length_type_id == '0':
        len_sub_packets = int(packet_data[1:16], 2)
        packet_data = packet_data[16:16 + len_sub_packets]
        # literals.append([])
        while packet_data and int(packet_data) != 0:
            packet_data, literals = parse_packet(packet_data, literals)
        # literals = [val for lit in literals for val in lit if val]
        literals = [apply_operator(literals[-1], type_id)]

    elif length_type_id == '1':
        num_sub_packets = int(packet_data[1:12], 2)
        packet_data = packet_data[12:]
        # literals.append([])
        for _ in range(num_sub_packets):
            packet_data, literals = parse_packet(packet_data, literals)
        literals = [apply_operator(literals, type_id)]

    return packet_data, literals


def part_two(packets):
    binary = bin(int(packets, 16))[2:].zfill(len(packets) * 4)
    parsed = parse_packet(binary)
    return parsed


if __name__ == "__main__":
    data = read_file("day16.txt")

    print(part_two(data)[1])
