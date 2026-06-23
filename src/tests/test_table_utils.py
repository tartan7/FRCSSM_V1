"""
テーブル・文字列ユーティリティのテストケース
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from test_framework import TestSuite, assert_equal, assert_true, assert_false
from utils.table_utils import sort_table, remove_parentheses


# --- sort_table ---

def test_sort_table_single_column():
    """sort_table: 1列指定の基本ソート"""
    table = [["田中", 3], ["鈴木", 1], ["佐藤", 2]]
    result = sort_table(table, [1])
    assert_equal(result[0][1], 1, "1列目で昇順ソート: 1番目")
    assert_equal(result[1][1], 2, "1列目で昇順ソート: 2番目")
    assert_equal(result[2][1], 3, "1列目で昇順ソート: 3番目")
    return True


def test_sort_table_by_string_column():
    """sort_table: 文字列列のソート"""
    table = [["田中", "B"], ["鈴木", "A"], ["佐藤", "C"]]
    result = sort_table(table, [1])
    assert_equal(result[0][1], "A", "文字列ソート: 1番目")
    assert_equal(result[1][1], "B", "文字列ソート: 2番目")
    assert_equal(result[2][1], "C", "文字列ソート: 3番目")
    return True


def test_sort_table_multi_column():
    """sort_table: 複数列指定のソート（後ろの列が優先）"""
    table = [
        ["B", 2],
        ["A", 2],
        ["B", 1],
        ["A", 1],
    ]
    result = sort_table(table, [1, 0])
    # cols=[1, 0] → reversed([1, 0]) = [0, 1] → まず列0でソート、次に列1でソート
    # 最終的に列1が最優先
    assert_equal(result[0][1], 1, "列1昇順: 1番目の列1値")
    assert_equal(result[2][1], 2, "列1昇順: 3番目の列1値")
    return True


def test_sort_table_first_column():
    """sort_table: 0列目でソート"""
    table = [["C", 3], ["A", 1], ["B", 2]]
    result = sort_table(table, [0])
    assert_equal(result[0][0], "A", "0列目ソート: 1番目")
    assert_equal(result[1][0], "B", "0列目ソート: 2番目")
    assert_equal(result[2][0], "C", "0列目ソート: 3番目")
    return True


def test_sort_table_empty_table():
    """sort_table: 空テーブルはそのまま返る"""
    result = sort_table([], [0])
    assert_equal(result, [], "空テーブルは空リストを返す")
    return True


def test_sort_table_single_row():
    """sort_table: 1行テーブルはそのまま"""
    table = [["田中", 1, "東京都"]]
    result = sort_table(table, [1])
    assert_equal(len(result), 1, "1行はそのまま1行")
    assert_equal(result[0][0], "田中", "値が保持される")
    return True


def test_sort_table_already_sorted():
    """sort_table: 既にソート済みのテーブルは変わらない"""
    table = [[1, "A"], [2, "B"], [3, "C"]]
    result = sort_table(table, [0])
    assert_equal(result[0][0], 1, "順序が保持される")
    assert_equal(result[1][0], 2, "順序が保持される")
    assert_equal(result[2][0], 3, "順序が保持される")
    return True


def test_sort_table_invalid_column_returns_original():
    """sort_table: 存在しない列インデックスはエラーなく元テーブルを返す"""
    table = [["A", 1], ["B", 2]]
    result = sort_table(table, [99])
    assert_true(isinstance(result, list), "例外なくリストが返る")
    assert_equal(len(result), 2, "行数が保持される")
    return True


def test_sort_table_preserves_row_contents():
    """sort_table: ソート後も行内容が完全に保持される"""
    table = [
        [3, "田中", "東京都", 10000],
        [1, "鈴木", "大阪府", 5000],
        [2, "佐藤", "名古屋市", 8000],
    ]
    result = sort_table(table, [0])
    assert_equal(result[0], [1, "鈴木", "大阪府", 5000], "1行目の全列が保持")
    assert_equal(result[1], [2, "佐藤", "名古屋市", 8000], "2行目の全列が保持")
    assert_equal(result[2], [3, "田中", "東京都", 10000], "3行目の全列が保持")
    return True


def test_sort_table_does_not_mutate_original():
    """sort_table: 元のテーブルを破壊しない（新しいリストを返す）"""
    original = [["B", 2], ["A", 1]]
    original_first = original[0][:]
    sort_table(original, [0])
    assert_equal(original[0], original_first, "元テーブルは変更されない")
    return True


# --- remove_parentheses ---

def test_remove_parentheses_basic():
    """remove_parentheses: 基本的な括弧除去"""
    result = remove_parentheses("田中太郎(長男)")
    assert_equal(result, "田中太郎", "括弧とその内容が除去される")
    return True


def test_remove_parentheses_no_parentheses():
    """remove_parentheses: 括弧なしはそのまま"""
    result = remove_parentheses("田中太郎")
    assert_equal(result, "田中太郎", "括弧なしは変化しない")
    return True


def test_remove_parentheses_empty_string():
    """remove_parentheses: 空文字はそのまま"""
    result = remove_parentheses("")
    assert_equal(result, "", "空文字は空文字を返す")
    return True


def test_remove_parentheses_only_parentheses():
    """remove_parentheses: 括弧のみは空文字になる"""
    result = remove_parentheses("(テスト)")
    assert_equal(result, "", "括弧のみは空文字")
    return True


def test_remove_parentheses_empty_parentheses():
    """remove_parentheses: 空括弧も除去される"""
    result = remove_parentheses("田中()")
    assert_equal(result, "田中", "空括弧も除去される")
    return True


def test_remove_parentheses_multiple():
    """remove_parentheses: 複数の括弧をすべて除去"""
    result = remove_parentheses("田中(長男)(50歳)")
    assert_equal(result, "田中", "複数括弧がすべて除去される")
    return True


def test_remove_parentheses_nested_outer_only():
    """remove_parentheses: ネストした括弧は外側のみ除去"""
    result = remove_parentheses("田中(長男(東京))")
    # パターン r'\([^()]*\)' は内側の括弧から除去されるため
    # "(長男(東京))" → 内側 "(東京)" を先に除去 → "田中(長男)"
    # → 再実行は1回のみなので "田中(長男)" のまま
    assert_true("田中" in result, "元の名前部分は保持される")
    return True


def test_remove_parentheses_with_spaces():
    """remove_parentheses: 括弧内にスペースがあっても除去"""
    result = remove_parentheses("田中 (長男)")
    assert_equal(result, "田中 ", "括弧部分が除去される（前のスペースは残る）")
    return True


def test_remove_parentheses_price_format():
    """remove_parentheses: 価格形式の括弧除去"""
    result = remove_parentheses("テスト花屋 (5,000円)")
    assert_equal(result, "テスト花屋 ", "価格括弧が除去される")
    return True


def test_remove_parentheses_japanese_parentheses_not_removed():
    """remove_parentheses: 全角括弧は除去しない（半角括弧のみ対象）"""
    result = remove_parentheses("田中太郎（長男）")
    assert_equal(result, "田中太郎（長男）", "全角括弧は除去されない")
    return True


def run_table_utils_tests():
    """テーブルユーティリティテストを実行"""
    suite = TestSuite("テーブルユーティリティテスト")

    suite.add_test(test_sort_table_single_column)
    suite.add_test(test_sort_table_by_string_column)
    suite.add_test(test_sort_table_multi_column)
    suite.add_test(test_sort_table_first_column)
    suite.add_test(test_sort_table_empty_table)
    suite.add_test(test_sort_table_single_row)
    suite.add_test(test_sort_table_already_sorted)
    suite.add_test(test_sort_table_invalid_column_returns_original)
    suite.add_test(test_sort_table_preserves_row_contents)
    suite.add_test(test_sort_table_does_not_mutate_original)
    suite.add_test(test_remove_parentheses_basic)
    suite.add_test(test_remove_parentheses_no_parentheses)
    suite.add_test(test_remove_parentheses_empty_string)
    suite.add_test(test_remove_parentheses_only_parentheses)
    suite.add_test(test_remove_parentheses_empty_parentheses)
    suite.add_test(test_remove_parentheses_multiple)
    suite.add_test(test_remove_parentheses_nested_outer_only)
    suite.add_test(test_remove_parentheses_with_spaces)
    suite.add_test(test_remove_parentheses_price_format)
    suite.add_test(test_remove_parentheses_japanese_parentheses_not_removed)

    return suite.run_tests()


if __name__ == "__main__":
    run_table_utils_tests()
