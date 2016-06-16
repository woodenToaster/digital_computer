

# Basic gates

def not_gate(ip):
    assert type(ip) == int, "not_gate requires integer input"
    return not ip


def or_gate(*inputs):
    assert len(inputs) > 1, "or_gate requires at least 2 inputs."
    return 1 if any(list(inputs)) else 0


def and_gate(*inputs):
    assert len(inputs) > 1, "and_gate requires at least 2 inputs."
    return 1 if all(list(inputs)) else 0


def nor_gate(*inputs):
    assert len(inputs) > 1, "nor_gate requires at least 2 inputs."
    return not_gate(or_gate(*inputs))


def nand_gate(*inputs):
    assert len(inputs) > 1, "nand_gate requires at least 2 inputs."
    return not_gate(and_gate(*inputs))


def xor_gate(*inputs):
    assert len(inputs) > 1, "xor_gate requires at least 2 inputs."
    return 0 if sum(inputs) % 2 == 0 else 1


def xnor_gate(*inputs):
    assert len(inputs) > 1, "xnor_gate requires at least 2 inputs."
    return not_gate(xor_gate(*inputs))


def one_of_eight_decoder(input_str):
    assert len(input_str) == 3, "one_of_eight_decoder takes a 3 digit string."
    a, b, c = bin_str_to_lst(input_str)

    y0 = and_gate(not_gate(a), not_gate(b), not_gate(c))
    y1 = and_gate(not_gate(a), not_gate(b), c)
    y2 = and_gate(not_gate(a), b, not_gate(c))
    y3 = and_gate(not_gate(a), b, c)
    y4 = and_gate(a, not_gate(b), not_gate(c))
    y5 = and_gate(a, not_gate(b), c)
    y6 = and_gate(a, b, not_gate(c))
    y7 = and_gate(a, b, c)

    outputs = [y0, y1, y2, y3, y4, y5, y6, y7]

    return outputs.index(1)


# ALU components

def half_adder(a, b):
    sum_bit = xor_gate(a, b)
    carry = and_gate(a, b)
    return (sum_bit, carry)


def full_adder(a, b, c):
    if a == 0:
        return half_adder(b, c)
    else:
        sum_bit = xor_gate(a, b, c)
        carry = or_gate(and_gate(a, b), and_gate(a, c), and_gate(b, c))
        return (sum_bit, carry)


def adder_8(a, b):
    assert len(a) == len(b) == 8, "adder_8 takes two lists of length 8."
    a7, a6, a5, a4, a3, a2, a1, a0 = a
    b7, b6, b5, b4, b3, b2, b1, b0 = b

    s0, c1 = half_adder(a0, b0)
    s1, c2 = full_adder(a1, b1, c1)
    s2, c3 = full_adder(a2, b2, c2)
    s3, c4 = full_adder(a3, b3, c3)
    s4, c5 = full_adder(a4, b4, c4)
    s5, c6 = full_adder(a5, b5, c5)
    s6, c7 = full_adder(a6, b6, c6)
    s7, c8 = full_adder(a7, b7, c7)

    return [c8, s7, s6, s5, s4, s3, s2, s1, s0]


# Helpers

def bin_str_to_lst(bin_str):
    return [int(b) for b in bin_str]
