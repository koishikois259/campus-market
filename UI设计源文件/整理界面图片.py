"""Copy full artboard PNGs to the course's numbered filenames, without rescaling."""
from pathlib import Path
import json
import shutil
import struct
import sys

ROOT = Path(__file__).resolve().parent.parent
VERSIONS = sys.argv[1:] or ['修订_v0.2', '补充_v0.3']
pages = []
for version in VERSIONS:
    manifest = json.loads((ROOT / 'UI设计源文件' / version / '画板清单.json').read_text(encoding='utf-8'))
    for page in manifest['pages']:
        pages.append(dict(page, version=version,
                          review='本轮已认可' if version == '修订_v0.2' else '待用户审查'))
assert len({page['id'] for page in pages}) == len(pages), 'Duplicate artboard IDs'
target_dir = ROOT / 'UI过程稿' / '原编号_v0.3'
rows = []

# Validate every source before writing numbered files.
for page in pages:
    source = ROOT / page['png']
    header = source.read_bytes()[:24]
    assert header[:8] == b'\x89PNG\r\n\x1a\n', f'Invalid PNG: {source}'
    size = struct.unpack('>II', header[16:24])
    assert size == (page['width'] * 2, page['height'] * 2), f'Unexpected PNG size: {source}'

for number, page in enumerate(pages, 1):
    source = ROOT / page['png']
    name = f'界面{number}.png'
    target = target_dir / name
    shutil.copyfile(source, target)
    assert target.read_bytes() == source.read_bytes(), f'Copy mismatch: {name}'
    rows.append(f"| {number} | [{name}]({name}) | {page['title']} | {page['width']*2} × {page['height']*2} | `{page['id']}` | {page['review']} |")

directory = '\n'.join([
    '# UI 界面图片目录', '',
    f"当前来源：{'、'.join(VERSIONS)}，共 {len(rows)} 张。", '',
    '界面1—14为用户已认可的主流程；界面15起为新增模块初稿，待用户审查。原编号和原图保持不变。', '',
    '图片为完整画板的 2x PNG，保持原比例，无浏览器目录、工具栏或跳转区域叠层。',
    '直接复用已核对的本地画板导出，未截图 Pixso，也不是 Pixso 导出成果。', '',
    '| 序号 | 文件 | 页面 | 像素尺寸 | 源画板 | 审查状态 |',
    '|---|---|---|---|---|---|', *rows, '',
    '相近状态变体用于审查与说明；后续报告只选各模块主要且不重复的界面，不逐图堆入。',
    '版本目录保留原稿与讨论稿；打包最终 UI 图片时使用本目录的编号 PNG，并按最终确认范围核对。', '',
    '重新整理全部图片：`python UI设计源文件/整理界面图片.py 修订_v0.2 补充_v0.3`。', ''
])
(target_dir / '界面目录.md').write_text(directory, encoding='utf-8', newline='\n')
print(f'Exported {len(rows)} numbered PNG files and the page directory.')
