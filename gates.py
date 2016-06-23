

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


class RSFlipFlop():

    def __init__(self):
        self.q = 0
        self.not_q = 1

    def send(self, r=0, s=0):
        if s == 1:
            self.q = 1
            self.not_q = 0
        if r == 1:
            self.q = 0
            self.not_q = 1


class ClockedDFlipFlop():

    def __init__(self):
        self._rs = RSFlipFlop()

    def send(self, d=0, clock=0):
        self._rs.send(s=and_gate(d, clock), r=and_gate(not_gate(d), clock))

    @property
    def q(self):
        return self._rs.q

    @property
    def not_q(self):
        return self._rs.not_q


class JKFlipFlop():

    def __init__(self):
        self._rs = RSFlipFlop()

    def send(self, j=0, k=0, clock=0):
        s = and_gate(clock, j, self._rs.not_q)
        r = and_gate(clock, k, self._rs.q)

        self._rs.send(r=r, s=s)

    @property
    def q(self):
        return self._rs.q

    @property
    def not_q(self):
        return self._rs.not_q


class Register8():

    def __init__(self):
        self.dff0 = ClockedDFlipFlop()
        self.dff1 = ClockedDFlipFlop()
        self.dff2 = ClockedDFlipFlop()
        self.dff3 = ClockedDFlipFlop()
        self.dff4 = ClockedDFlipFlop()
        self.dff5 = ClockedDFlipFlop()
        self.dff6 = ClockedDFlipFlop()
        self.dff7 = ClockedDFlipFlop()
        self.word = [0] * 8

    # TODO: enable
    def send(self, word8, load=0, clear=0, clock=0):
        if clear and clock:
            self.word = [0] * 8
            return

        x7, x6, x5, x4, x3, x2, x1, x0 = word8

        self.dff0.send(
            d=or_gate(and_gate(load, x0), and_gate(not_gate(load), self.dff0.q)),
            clock=clock
        )
        y0 = self.dff0.q

        self.dff1.send(
            d=or_gate(and_gate(load, x1), and_gate(not_gate(load), self.dff1.q)),
            clock=clock
        )
        y1 = self.dff1.q

        self.dff2.send(
            d=or_gate(and_gate(load, x2), and_gate(not_gate(load), self.dff2.q)),
            clock=clock
        )
        y2 = self.dff2.q

        self.dff3.send(
            d=or_gate(and_gate(load, x3), and_gate(not_gate(load), self.dff3.q)),
            clock=clock
        )
        y3 = self.dff3.q

        self.dff4.send(
            d=or_gate(and_gate(load, x4), and_gate(not_gate(load), self.dff4.q)),
            clock=clock
        )
        y4 = self.dff4.q

        self.dff5.send(
            d=or_gate(and_gate(load, x5), and_gate(not_gate(load), self.dff5.q)),
            clock=clock
        )
        y5 = self.dff5.q

        self.dff6.send(
            d=or_gate(and_gate(load, x6), and_gate(not_gate(load), self.dff6.q)),
            clock=clock
        )
        y6 = self.dff6.q

        self.dff7.send(
            d=or_gate(and_gate(load, x7), and_gate(not_gate(load), self.dff7.q)),
            clock=clock
        )
        y7 = self.dff7.q

        self.word = [y7, y6, y5, y4, y3, y2, y1, y0]


class ControlledSynchronousCounter():

    def __init__(self):
        pass


class ProgramCounter8(Register8):
    pass


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
