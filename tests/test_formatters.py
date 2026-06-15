from formatters import FORMATTERS

# Update _EXAMPLE_ROW to match your dataset's schema.
_EXAMPLE_ROW = {
    "question": "What is the boiling point of water?",
    "choices": {"text": ["50°C", "100°C", "150°C", "200°C"], "label": ["A", "B", "C", "D"]},
    "answerKey": "B",
}


def test_all_formatters_return_required_keys():
    for name, fn in FORMATTERS.items():
        result = fn(_EXAMPLE_ROW)
        assert "instruction" in result, f"{name}: missing 'instruction'"
        assert "response" in result, f"{name}: missing 'response'"
        assert "source" in result, f"{name}: missing 'source'"
        assert isinstance(result["instruction"], str), f"{name}: 'instruction' must be str"
        assert isinstance(result["response"], str), f"{name}: 'response' must be str"
        assert isinstance(result["source"], str), f"{name}: 'source' must be str"


def test_formatters_keys_are_strings():
    for key in FORMATTERS:
        assert isinstance(key, str)
