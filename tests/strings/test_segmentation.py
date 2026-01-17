import math

import pytest

from blaise.strings.segmentation import Segmenter

# Helper to compare DataFrames approximately


def assert_df_equal(df, expected_rows):
    # expected_rows: list of tuples (text, score)
    assert df.shape[0] == len(expected_rows)
    for row, (exp_text, exp_score) in zip(df.iter_rows(named=True), expected_rows):
        assert row["text"] == exp_text
        # allow small tolerance for floating point
        assert math.isclose(row["score"], exp_score, rel_tol=1e-9)


def test_segment_with_dict_word_dist():
    word_dist = {"hello": 8, "world": 2}
    seg = Segmenter(word_dist=word_dist)
    assert seg.word_dist == {"hello": 0.8, "world": 0.2}
    df = seg.segment("helloworld")
    expected_score = -(5 * math.log(0.8) + 5 * math.log(0.2))
    assert_df_equal(df, [("hello world", expected_score)])


def test_segment_with_list_word_dist():
    word_dist = ["hello", "world"]
    seg = Segmenter(word_dist=word_dist)
    assert seg.word_dist == {"hello": 0.5, "world": 0.5}
    df = seg.segment("helloworld")
    expected_score = -(5 * math.log(0.5) + 5 * math.log(0.5))
    assert_df_equal(df, [("hello world", expected_score)])


def test_segment_with_no_solution():
    word_dist = ["hello", "wor"]
    seg = Segmenter(word_dist=word_dist)
    df = seg.segment("helloworld")
    assert len(df) == 0


def test_segment_empty_string():
    seg = Segmenter(word_dist={"a": 1.0})
    df = seg.segment("")
    assert df.shape[0] == 1
    assert df["text"].item() == ""
    assert df["score"].item() == 0


def test_n_branch_limit():
    # Word dict with multiple segmentation possibilities
    words = {"a": 1.0, "aa": 1.0, "aaa": 1.0}
    seg = Segmenter(word_dist=words, n_branch_limit=1)
    df = seg.segment("aaa")
    # Only one segmentation should be returned
    assert df.shape[0] == 1
    # The best segmentation is any of the equal-scoring ones; check that text is one of them
    assert df["text"].item() in {"a a a", "a aa", "aa a", "aaa"}


if __name__ == "__main__":
    pytest.main([__file__])
