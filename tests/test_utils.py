import pandas as pd
import pytest

from utils import normalize_binary_target


def test_numeric_zero_one_labels_keep_their_meaning_when_one_appears_first():
    source = pd.Series([1, 0, 1, 0])
    encoded, mapping = normalize_binary_target(source)

    assert encoded.tolist() == [1, 0, 1, 0]
    assert mapping == {0: 0, 1: 1}


def test_numeric_classes_outside_zero_one_use_deterministic_order():
    source = pd.Series([9, 3, 9, 3])
    encoded, mapping = normalize_binary_target(source)

    assert encoded.tolist() == [1, 0, 1, 0]
    assert mapping == {3: 0, 9: 1}


def test_approved_and_rejected_labels_have_correct_positive_class():
    source = pd.Series(["Rejected", "Approved", "APPROVED", "rejected"])
    encoded, mapping = normalize_binary_target(source)

    assert encoded.tolist() == [0, 1, 1, 0]
    assert mapping == {"approved": 1, "rejected": 0}


def test_yes_no_labels_have_correct_positive_class():
    source = pd.Series(["No", "Yes", "No"])
    encoded, mapping = normalize_binary_target(source)

    assert encoded.tolist() == [0, 1, 0]
    assert mapping == {"yes": 1, "no": 0}


def test_unknown_text_labels_use_deterministic_sorted_order():
    source = pd.Series(["zebra", "ant", "zebra"])
    encoded, mapping = normalize_binary_target(source)

    assert encoded.tolist() == [1, 0, 1]
    assert mapping == {"ant": 0, "zebra": 1}


def test_missing_target_values_remain_missing():
    source = pd.Series(["Approved", None, "Rejected"])
    encoded, _ = normalize_binary_target(source)

    assert encoded.iloc[0] == 1
    assert pd.isna(encoded.iloc[1])
    assert encoded.iloc[2] == 0


def test_single_class_target_is_rejected():
    with pytest.raises(ValueError, match="exactly 2"):
        normalize_binary_target(pd.Series(["Approved", "Approved"]))
