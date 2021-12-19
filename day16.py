"""Day 16."""
import binascii


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


def parse_packet(binary, literal_values=None, versions=None):
    if literal_values is None:
        literal_values = []
    if versions is None:
        versions = []

    version = int(binary[:3], 2)
    versions.append(version)

    type_id = int(binary[3:6], 2)
    packet_data = binary[6:]

    if type_id == 4:  # Literal packet
        literal_value, packet_data = get_literal_packet_value(packet_data)
        literal_values.append(literal_value)
        if packet_data and (int(packet_data) != 0):
            return parse_packet(packet_data, literal_values, versions)
        return literal_values, versions, packet_data

    # Operator packet
    length_type_id = packet_data[0]
    if length_type_id == '0':
        len_sub_packets = int(packet_data[1:16], 2)
        sub_packets = packet_data[16:16+len_sub_packets]
        remaining_packets = packet_data[16+len_sub_packets:]
        literal_values, versions, sub_packets = parse_packet(sub_packets, literal_values, versions)
        if not remaining_packets and sub_packets and (int(sub_packets) != 0):
            return parse_packet(sub_packets, literal_values, versions)
        try:
            return parse_packet(remaining_packets, literal_values, versions)
        except Exception as e:
            return literal_values, versions, remaining_packets
    elif length_type_id == '1':
        num_sub_packets = int(packet_data[1:12], 2)
        sub_packets = packet_data[12:]
        literal_values, versions, sub_packets = parse_packet(sub_packets, literal_values, versions)
        if sub_packets and (int(sub_packets) != 0):
            return parse_packet(sub_packets, literal_values, versions)
        else:
            return literal_values, versions, sub_packets


def part_one(packets):
    binary = bin(int(packets, 16))[2:].zfill(len(packets) * 4)
    literals, versions, _ = parse_packet(binary)
    print(literals, versions)
    return sum(versions)


def part_two(packets):
    ...


if __name__ == "__main__":
    data = read_file("day16.txt")

    print(part_one(data))
    print(part_two(data))
