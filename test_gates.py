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
        two_fifty_five = [1, 1, 1, 1, 1, 1, 1, 1]
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
