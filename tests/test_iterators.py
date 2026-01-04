from blaise.iterators import product_index_ordered


class TestProductIndexOrdered:
    def test_empty(self):
        assert list(product_index_ordered([], [])) == []

    def test_single(self):
        assert list(product_index_ordered("A", "B", "C", "D")) == [("A", "B", "C", "D")]

    def test_ordering(self):
        assert list(product_index_ordered(range(10), range(10)))[:5] == [
            (0, 0),
            (0, 1),
            (1, 0),
            (0, 2),
            (1, 1),
        ]

    def test_ordering_three_lists(self):
        assert list(product_index_ordered("AB", [1, 2, 3], "CD")) == [
            ("A", 1, "C"),
            ("A", 1, "D"),
            ("A", 2, "C"),
            ("B", 1, "C"),
            ("A", 3, "D"),
            ("B", 1, "D"),
            ("B", 2, "C"),
            ("B", 3, "D"),
        ]
