def product_index_ordered(*iterators):
    """
    An iterator over multiple iterators giving a cartesian product, but ordered
    in sum(index). So indices in this order for the case of two iterators:
    [0, 0], [1, 0], [0, 1], [2, 0], [1, 1], [0, 2], [2, 1], [1, 2], ... etc.
    """
    lists = [list(i) for i in iterators]
    if any(len(x) == 0 for x in lists):
        return
    max_index_sum = sum(len(x) - 1 for x in lists)
    for index_sum in range(max_index_sum + 1):
        yield from _product_index_ordered(max_index_sum, index_sum, lists)


def _product_index_ordered(index_sum: int, target_index_sum: int, lists: list[list]):
    if target_index_sum > index_sum:
        return
    elif len(lists) == 1:
        yield (lists[0][target_index_sum],)
    else:
        next_index_sum = index_sum - (len(lists[0]) - 1)
        min_index = max(target_index_sum - next_index_sum, 0)
        for i, val in enumerate(lists[0][min_index : target_index_sum + 1]):
            for sol in _product_index_ordered(next_index_sum, target_index_sum - i, lists[1:]):
                yield (val,) + sol
