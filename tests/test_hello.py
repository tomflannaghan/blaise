from blaise import hello


def test_hello():
    """Test that hello() returns the expected greeting."""
    result = hello()
    assert result == "Hello from blaise!"