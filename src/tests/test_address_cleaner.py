"""
住所クレンジングユーティリティのテスト
address-cleansing/test_address_cleaner.py から移植・パス修正。
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pytest
from unittest.mock import MagicMock, patch
from utils.address_cleaner import clean_address_logic, clean_addresses_in_book, process_excel


def test_clean_address_logic():
    result = clean_address_logic("東京都千代田区丸の内1-1-1")
    assert result != ""
    assert "東京都" in result

    assert clean_address_logic("") == ""
    assert clean_address_logic(None) == ""

    result_invalid = clean_address_logic("存在しない架空の住所12345")
    assert result_invalid == "存在しない架空の住所12345"


def test_clean_addresses_in_book():
    mock_wb = MagicMock()
    mock_app = MagicMock()
    mock_wb.app = mock_app

    mock_sheet = MagicMock()
    mock_last_cell = MagicMock()
    mock_last_cell.row = 100
    mock_sheet.cells.last_cell = mock_last_cell

    mock_end_up = MagicMock()
    mock_end_up.row = 3

    def range_side_effect(addr):
        m = MagicMock()
        if addr == 'D100':
            m.end.return_value = mock_end_up
        elif addr == 'D2:D3':
            m.value = ["住所1", "住所2"]
        return m

    mock_sheet.range.side_effect = range_side_effect
    mock_wb.sheets.__getitem__ = lambda self, key: mock_sheet

    clean_addresses_in_book(mock_wb)

    assert mock_app.screen_updating is True
    assert mock_app.calculation == 'automatic'
    assert mock_app.display_alerts is True


@patch('utils.address_cleaner.xw', create=True)
@patch('utils.address_cleaner.os.path.exists')
def test_process_excel(mock_exists, mock_xw):
    mock_exists.return_value = True

    mock_app_instance = MagicMock()
    mock_xw.App.return_value.__enter__.return_value = mock_app_instance

    mock_wb = MagicMock()
    mock_app_instance.books.open.return_value = mock_wb

    mock_sheet = MagicMock()
    mock_wb.sheets.__getitem__ = lambda self, key: mock_sheet

    mock_last_cell = MagicMock()
    mock_last_cell.row = 100
    mock_sheet.cells.last_cell = mock_last_cell

    mock_end_up = MagicMock()
    mock_end_up.row = 2

    def range_side_effect(addr):
        m = MagicMock()
        if addr == 'D100':
            m.end.return_value = mock_end_up
        elif addr == 'D2:D2':
            m.value = "住所1"
        return m

    mock_sheet.range.side_effect = range_side_effect

    process_excel("dummy.xlsx")

    mock_wb.save.assert_called_once()
    mock_wb.close.assert_called_once()
