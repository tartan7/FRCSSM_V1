"""
レイアウト管理クラス
GUIレイアウトの統一管理と最適化
"""
import TkEasyGUI as sg
from typing import Dict, List, Any, Optional, Tuple

class LayoutManager:
    """レイアウトの統一管理クラス"""
    
    def __init__(self):
        self.theme = "clam"  # デフォルトテーマ
        self.window_size = (450, 700)  # デフォルトウィンドウサイズ（コンテンツサイズに最適化）
        self.font_family = "Arial"
        self.font_size = 10
        
    def set_theme(self, theme: str) -> None:
        """テーマを設定"""
        self.theme = theme
        sg.theme(theme)
    
    def set_window_size(self, width: int, height: int) -> None:
        """ウィンドウサイズを設定"""
        self.window_size = (width, height)
    
    def set_font(self, family: str, size: int) -> None:
        """フォントを設定"""
        self.font_family = family
        self.font_size = size
    
    def get_button_style(self, size: Tuple[int, int] = (12, 1)) -> Dict[str, Any]:
        """ボタンのスタイルを取得"""
        return {
            'size': size,
            'font': (self.font_family, self.font_size),
            'button_color': ('white', '#4CAF50'),
            'mouseover_colors': ('white', '#45a049'),
            'disabled': False
        }
    
    def get_input_style(self, size: Tuple[int, int] = (20, 1)) -> Dict[str, Any]:
        """入力フィールドのスタイルを取得"""
        return {
            'size': size,
            'font': (self.font_family, self.font_size),
            'background_color': 'white',
            'text_color': 'black'
        }
    
    def get_text_style(self, font_size: Optional[int] = None) -> Dict[str, Any]:
        """テキストのスタイルを取得"""
        size = font_size or self.font_size
        return {
            'font': (self.font_family, size),
            'text_color': 'black'
        }
    
    def get_title_style(self) -> Dict[str, Any]:
        """タイトルのスタイルを取得"""
        return {
            'font': (self.font_family, 16, 'bold'),
            'text_color': '#2E7D32',
            'justification': 'center'
        }
    
    def get_section_style(self) -> Dict[str, Any]:
        """セクションのスタイルを取得"""
        return {
            'font': (self.font_family, 12, 'bold'),
            'text_color': '#1976D2',
            'justification': 'left'
        }
    
    def create_window(self, title: str, layout: List[List], **kwargs) -> sg.Window:
        """最適化されたウィンドウを作成"""
        # デフォルト設定を適用
        window_kwargs = {
            'title': title,
            'layout': layout,
            'size': self.window_size,
            'resizable': True,
            'finalize': True,
            'element_justification': 'left',
            'font': (self.font_family, self.font_size),
            'auto_size_buttons': True,
            'auto_size_text': True,
            'grab_anywhere': False,
            'keep_on_top': False,
            'modal': False
        }
        
        # ユーザー指定の設定で上書き
        window_kwargs.update(kwargs)
        
        return sg.Window(**window_kwargs)
    
    def create_modal_window(self, title: str, layout: List[List], **kwargs) -> sg.Window:
        """モーダルウィンドウを作成"""
        modal_kwargs = {
            'modal': True,
            'grab_anywhere': True,
            'keep_on_top': True
        }
        modal_kwargs.update(kwargs)
        
        return self.create_window(title, layout, **modal_kwargs)
    
    def create_scrollable_layout(self, content: List[List], max_height: int = 400) -> List[List]:
        """スクロール可能なレイアウトを作成"""
        return [
            [sg.Column(
                content,
                scrollable=True,
                vertical_scroll_only=True,
                size=(None, max_height),
                key='scrollable_content'
            )]
        ]
    
    def create_tab_layout(self, tabs: Dict[str, List[List]]) -> List[List]:
        """タブレイアウトを作成"""
        tab_group = []
        for tab_name, tab_content in tabs.items():
            tab_group.append(sg.Tab(tab_name, tab_content))
        
        return [[sg.TabGroup([tab_group], key='tab_group')]]
    
    def create_form_layout(self, fields: List[Dict[str, Any]]) -> List[List]:
        """フォームレイアウトを作成"""
        layout = []
        
        for field in fields:
            field_type = field.get('type', 'input')
            label = field.get('label', '')
            key = field.get('key', '')
            size = field.get('size', (20, 1))
            required = field.get('required', False)
            
            if field_type == 'input':
                layout.append([
                    sg.Text(f"{label}{'*' if required else ''}:", **self.get_text_style()),
                    sg.Input(key=key, **self.get_input_style(size))
                ])
            elif field_type == 'multiline':
                layout.append([
                    sg.Text(f"{label}{'*' if required else ''}:", **self.get_text_style()),
                    sg.Multiline(key=key, size=size, **self.get_input_style())
                ])
            elif field_type == 'checkbox':
                layout.append([
                    sg.Checkbox(label, key=key, **self.get_text_style())
                ])
            elif field_type == 'combo':
                options = field.get('options', [])
                layout.append([
                    sg.Text(f"{label}{'*' if required else ''}:", **self.get_text_style()),
                    sg.Combo(options, key=key, **self.get_input_style(size))
                ])
            elif field_type == 'calendar':
                layout.append([
                    sg.Text(f"{label}{'*' if required else ''}:", **self.get_text_style()),
                    sg.Input(key=key, **self.get_input_style(size)),
                    sg.CalendarButton('カレンダー', key=f'{key}_calendar', target=key)
                ])
        
        return layout
    
    def create_button_row(self, buttons: List[Dict[str, Any]]) -> List[List]:
        """ボタン行を作成"""
        button_elements = []
        
        for button in buttons:
            text = button.get('text', '')
            key = button.get('key', '')
            size = button.get('size', (12, 1))
            color = button.get('color', None)
            
            button_style = self.get_button_style(size)
            if color:
                button_style['button_color'] = color
            
            button_elements.append(sg.Button(text, key=key, **button_style))
        
        return [button_elements]
    
    def create_table_layout(self, headers: List[str], data: List[List], key: str = 'table') -> List[List]:
        """テーブルレイアウトを作成"""
        return [
            [sg.Table(
                values=data,
                headings=headers,
                key=key,
                auto_size_columns=True,
                max_col_width=50,
                num_rows=10,
                alternating_row_color='lightblue',
                selected_row_colors=('white', '#4CAF50'),
                enable_events=True,
                font=(self.font_family, self.font_size)
            )]
        ]
    
    def create_status_bar(self, text: str = "準備完了") -> List[List]:
        """ステータスバーを作成"""
        return [
            [sg.HSeparator()],
            [sg.Text(text, key='status_text', **self.get_text_style(9), justification='left')]
        ]
    
    def create_progress_bar(self, key: str = 'progress') -> List[List]:
        """プログレスバーを作成"""
        return [
            [sg.ProgressBar(100, orientation='h', size=(40, 20), key=key, visible=False)]
        ]
    
    def optimize_layout(self, layout: List[List]) -> List[List]:
        """レイアウトを最適化"""
        optimized = []
        
        for row in layout:
            optimized_row = []
            for element in row:
                if isinstance(element, sg.Text):
                    # テキスト要素の最適化
                    if not hasattr(element, 'font') or not element.font:
                        element.font = (self.font_family, self.font_size)
                elif isinstance(element, sg.Input):
                    # 入力要素の最適化
                    if not hasattr(element, 'font') or not element.font:
                        element.font = (self.font_family, self.font_size)
                elif isinstance(element, sg.Button):
                    # ボタン要素の最適化
                    if not hasattr(element, 'font') or not element.font:
                        element.font = (self.font_family, self.font_size)
                
                optimized_row.append(element)
            optimized.append(optimized_row)
        
        return optimized