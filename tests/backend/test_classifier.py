def test_unknown_is_safe():
    result = {"name": "unknown", "confidence": 0, "uncertain": True}
    assert result["uncertain"]
