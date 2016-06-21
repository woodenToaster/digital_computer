import unittest

import gates


class TestGates(unittest.TestCase):

    def test_not_gate_inverts(self):
        self.assertEqual(gates.not_gate(1), 0)
        self.assertEqual(gates.not_gate(0), 1)

    def test_not_gate_with_str_input_raises(self):
        with self.assertRaises(AssertionError):
            gates.not_gate('1')

    def test_or_gate(self):
        self.assertEqual(gates.or_gate(0, 0), 0)
        self.assertEqual(gates.or_gate(0, 1), 1)
        self.assertEqual(gates.or_gate(1, 0), 1)
        self.assertEqual(gates.or_gate(1, 1), 1)

    def test_or_gate_one_input_raises(self):
        with self.assertRaises(AssertionError):
            gates.or_gate(1)

    def test_nor_gate(self):
        self.assertEqual(gates.nor_gate(0, 0), 1)
        self.assertEqual(gates.nor_gate(0, 1), 0)
        self.assertEqual(gates.nor_gate(1, 0), 0)
        self.assertEqual(gates.nor_gate(1, 1), 0)

    def test_and_gate(self):
        self.assertEqual(gates.and_gate(0, 0), 0)
        self.assertEqual(gates.and_gate(0, 1), 0)
        self.assertEqual(gates.and_gate(1, 0), 0)
        self.assertEqual(gates.and_gate(1, 1), 1)

    def test_and_gate_one_input_raises(self):
        with self.assertRaises(AssertionError):
            gates.and_gate(1)

    def test_nand_gate(self):
        self.assertEqual(gates.nand_gate(0, 0), 1)
        self.assertEqual(gates.nand_gate(0, 1), 1)
        self.assertEqual(gates.nand_gate(1, 0), 1)
        self.assertEqual(gates.nand_gate(1, 1), 0)

    def test_xor_gate(self):
        self.assertEqual(gates.xor_gate(0, 0), 0)
        self.assertEqual(gates.xor_gate(0, 1), 1)
        self.assertEqual(gates.xor_gate(1, 0), 1)
        self.assertEqual(gates.xor_gate(1, 1), 0)
        self.assertEqual(gates.xor_gate(0, 0, 0), 0)
        self.assertEqual(gates.xor_gate(1, 1, 1), 1)
        self.assertEqual(gates.xor_gate(1, 0, 0), 1)

    def test_xnor_gate(self):
        self.assertEqual(gates.xnor_gate(0, 0), 1)
        self.assertEqual(gates.xnor_gate(0, 1), 0)
        self.assertEqual(gates.xnor_gate(1, 0), 0)
        self.assertEqual(gates.xnor_gate(1, 1), 1)
        self.assertEqual(gates.xnor_gate(0, 0, 0), 1)
        self.assertEqual(gates.xnor_gate(1, 1, 1), 0)
        self.assertEqual(gates.xnor_gate(1, 0, 0), 0)

    def test_one_of_eight_decoder(self):
        self.assertEqual(gates.one_of_eight_decoder('000'), 0)
        self.assertEqual(gates.one_of_eight_decoder('001'), 1)
        self.assertEqual(gates.one_of_eight_decoder('010'), 2)
        self.assertEqual(gates.one_of_eight_decoder('011'), 3)
        self.assertEqual(gates.one_of_eight_decoder('100'), 4)
        self.assertEqual(gates.one_of_eight_decoder('101'), 5)
        self.assertEqual(gates.one_of_eight_decoder('110'), 6)
        self.assertEqual(gates.one_of_eight_decoder('111'), 7)

    def test_rs_flipflop(self):
        rs = gates.RSFlipFlop()
        rs.send(s=1)
        self.assertEqual(rs.q, 1)
        self.assertEqual(rs.not_q, 0)

        rs.send(r=1)
        self.assertEqual(rs.q, 0)
        self.assertEqual(rs.not_q, 1)

    def test_clocked_d_flipflop(self):
        dff = gates.ClockedDFlipFlop()
        dff.send(d=1, clock=0)
        self.assertEqual(dff.q(), 0)
        self.assertEqual(dff.not_q(), 1)

        dff.send(d=1, clock=1)
        self.assertEqual(dff.q(), 1)
        self.assertEqual(dff.not_q(), 0)

        dff.send(d=0, clock=1)
        self.assertEqual(dff.q(), 0)
        self.assertEqual(dff.not_q(), 1)

    def test_register_8(self):
        zero = [0] * 8
        r8 = gates.Register8()
        r8.send(zero, enable=1, clock=1)
        self.assertListEqual(r8.word, zero)

        one = [0] * 7 + [1]
        r8.send(one, load=1)
        self.assertListEqual(r8.word, zero)

        r8.send(one, load=1, clock=1)
        self.assertListEqual(r8.word, one)

        two_fifty_five = [1] * 8
        r8.send(two_fifty_five, load=1, clock=1)
        self.assertListEqual(r8.word, two_fifty_five)


class TestALUComponents(unittest.TestCase):

    def test_half_adder(self):
        self.assertEqual(gates.half_adder(0, 0), (0, 0))
        self.assertEqual(gates.half_adder(0, 1), (1, 0))
        self.assertEqual(gates.half_adder(1, 0), (1, 0))
        self.assertEqual(gates.half_adder(1, 1), (0, 1))

    def test_full_adder(self):
        self.assertEqual(gates.full_adder(0, 0, 0), (0, 0))
        self.assertEqual(gates.full_adder(0, 0, 1), (1, 0))
        self.assertEqual(gates.full_adder(0, 1, 0), (1, 0))
        self.assertEqual(gates.full_adder(0, 1, 1), (0, 1))
        self.assertEqual(gates.full_adder(1, 0, 0), (1, 0))
        self.assertEqual(gates.full_adder(1, 0, 1), (0, 1))
        self.assertEqual(gates.full_adder(1, 1, 0), (0, 1))
        self.assertEqual(gates.full_adder(1, 1, 1), (1, 1))

    def test_adder_8(self):
        fifteen = [0, 0, 0, 0, 1, 1, 1, 1]
        eighteen = [0, 0, 0, 1, 0, 0, 1, 0]
        thirty_three = [0, 0, 0, 1, 0, 0, 0, 0, 1]
        two_fifty_five = [1] * 8
        five_ten = [1, 1, 1, 1, 1, 1, 1, 1, 0]

        self.assertListEqual(gates.adder_8(fifteen, eighteen), thirty_three)
        self.assertListEqual(
            gates.adder_8(two_fifty_five, two_fifty_five), five_ten
        )


class TestHelpers(unittest.TestCase):

    def test_bin_str_to_lst(self):
        self.assertEqual(gates.bin_str_to_lst('101'), [1, 0, 1])
        self.assertEqual(gates.bin_str_to_lst('1'), [1])
        self.assertEqual(gates.bin_str_to_lst('0'), [0])
        self.assertEqual(gates.bin_str_to_lst('11110'), [1, 1, 1, 1, 0])

if __name__ == '__main__':
    unittest.main()
