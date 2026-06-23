"""
テーブル・文字列ユーティリティ
func1.py から抽出した純粋なテーブル操作・文字列処理関数群
"""
import re
import operator


def sort_table(table, cols):
    """複数列によるテーブルのソート

    table: リストのリスト（各内リストが1行）
    cols:  ソートする列番号のリスト（例: (1, 0) は列1でソート後、列0でソート）
    """
    for col in reversed(cols):
        try:
            table = sorted(table, key=operator.itemgetter(col))
        except Exception as e:
            print(f"sort_table エラー (col={col}): {e}")
    return table


def remove_parentheses(string):
    """文字列から括弧とその中身を除去する"""
    pattern = r'\([^()]*\)'
    return re.sub(pattern, '', string)
