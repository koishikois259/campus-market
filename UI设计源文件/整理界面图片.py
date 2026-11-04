"""Copy full artboard PNGs to the course's numbered filenames, without rescaling."""
from pathlib import Path
import json
import shutil
import struct
import sys

ROOT = Path(__file__).resolve().parent.parent
VERSION = sys.argv[1] if len(sys.argv) > 1 else '修订_v0.2'
manifest = json.loads((ROOT / 'UI设计源文件' / VERSION / '画板清单.json').read_text(encoding='utf-8'))
target_dir = ROOT / 'UI界面'
rows = []

# Validate every source before writing numbered files.
for page in manifest['pages']:
    source = ROOT / page['png']
    header = source.read_bytes()[:24]
    assert header[:8] == b'\x89PNG\r\n\x1a\n', f'Invalid PNG: {source}'
    size = struct.unpack('>II', header[16:24])
    assert size == (page['width'] * 2, page['height'] * 2), f'Unexpected PNG size: {source}'

for number, page in enumerate(manifest['pages'], 1):
    source = ROOT / page['png']
    name = f'界面{number}.png'
    target = target_dir / name
    shutil.copyfile(source, target)
    assert target.read_bytes() == source.read_bytes(), f'Copy mismatch: {name}'
    rows.append(f"| {number} | [{name}]({name}) | {page['title']} | {page['width']*2} × {page['height']*2} | `{page['id']}` |")

directory = '\n'.join([
    '# UI 界面图片目录', '',
    f'当前来源：{VERSION}。按本轮预览画板顺序编号，共 {len(rows)} 张。', '',
    '图片为完整画板的 2x PNG，保持原比例，无浏览器目录、工具栏或跳转区域叠层。',
    '直接复用已核对的本地画板导出，未截图 Pixso，也不是 Pixso 导出成果。', '',
    '| 序号 | 文件 | 页面 | 像素尺寸 | 源画板 |',
    '|---|---|---|---|---|', *rows, '',
    '这是当前主流程及状态变体的阶段产物，其余业务模块后续补充后继续维护目录。',
    '版本目录保留原稿与讨论稿；打包最终 UI 图片时使用本目录的编号 PNG，并按最终确认范围核对。', '',
    '源画板和本地预览见对应版本目录；重新整理可运行 `python UI设计源文件/整理界面图片.py 修订_v0.2`。', ''
])
(target_dir / '界面目录.md').write_text(directory, encoding='utf-8', newline='\n')
print(f'Exported {len(rows)} numbered PNG files and the page directory.')
