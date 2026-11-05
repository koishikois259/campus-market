"""Export ten selected report UIs and their offline gallery without rescaling."""
from pathlib import Path
import copy
import json
import re
import shutil
import struct

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / 'UI设计源文件'
TARGET = ROOT / 'UI界面'
selection = json.loads((SOURCE / '主要界面清单.json').read_text(encoding='utf-8'))
assert 0 < len(selection['pages']) <= 10
assert {m for p in selection['pages'] for m in p['modules']} == {'用户','商品','预约','订单','支付','代交','售后','平台管理'}
pages = []
for index, entry in enumerate(selection['pages'], 1):
    assert entry['number'] == index
    manifest = json.loads((SOURCE / entry['version'] / '画板清单.json').read_text(encoding='utf-8'))
    page = copy.deepcopy(next(p for p in manifest['pages'] if p['id'] == entry['id']))
    source = ROOT / page['png']
    header = source.read_bytes()[:24]
    assert header[:8] == b'\x89PNG\r\n\x1a\n'
    assert struct.unpack('>II',header[16:24]) == (page['width']*2,page['height']*2)
    page.update(number=index,filename=f"界面{index:02d}——{entry['name']}.png",
                title=entry['name'],modules=entry['modules'],source_png=page['png'])
    page['png']='UI界面/'+page['filename']
    page['note']='、'.join(entry['modules'])+'模块 · 报告精选界面；业务按钮仅作静态展示。'
    pages.append(page)
ids={p['id'] for p in pages}
for page in pages:page['hotspots']=[h for h in page.get('hotspots',[]) if h['target'] in ids]
TARGET.mkdir(parents=True,exist_ok=True)
assert not {p.name for p in TARGET.glob('*.png')} - {p['filename'] for p in pages}, 'Archive old PNGs before exporting'
for page in pages:
    shutil.copyfile(ROOT/page['source_png'],TARGET/page['filename'])
    assert (ROOT/page['source_png']).read_bytes()==(TARGET/page['filename']).read_bytes()
rows=[f"| {p['number']:02d} | [{p['filename']}]({p['filename']}) | {'、'.join(p['modules'])} | `{p['id']}` |" for p in pages]
directory='\n'.join([
    '# UI主要界面目录','',
    '本目录保留报告使用的10张主要界面，覆盖八个业务模块。文件名为“界面xx——名称.png”。',
    '图片与过程稿原图逐字节一致，均为完整画板2x PNG。','',
    '[主要界面预览](预览.html) · [全部补充稿](../UI过程稿/补充_v0.3/预览.html) · [主流程过程稿](../UI过程稿/修订_v0.2/预览.html)','',
    '| 编号 | 图片 | 对应模块 | 源画板 |','|---|---|---|---|',*rows,'',
    '其余图片、各版预览和原编号1—38存入 `../UI过程稿/`；可编辑SVG仍在 `../UI设计源文件/`。',
    '这些图片由本地SVG导出，尚未在Pixso中核对，不记为Pixso截图。',
    '重建主要图片和预览：`python UI设计源文件/整理主要界面.py`。',''])
(TARGET/'界面目录.md').write_text(directory,encoding='utf-8',newline='\n')
html=(ROOT/'UI过程稿/补充_v0.3/预览.html').read_text(encoding='utf-8')
html=html.replace('UI 补充稿预览','UI 主要界面预览').replace('v0.3 · 补充初稿待审查','报告精选 · 10张')
html=html.replace('补充画板 · 24 张','主要画板 · 10 张').replace('查看已确认主流程','查看全部补充稿')
html=html.replace('补充模块初稿，待你审查。','八模块主要界面，共10张。')
html=re.sub(r'const pages = [\s\S]*?;\nconst \$=',lambda _: 'const pages = '+json.dumps(pages,ensure_ascii=False).replace('<','\\u003c')+';\nconst $=',html,count=1)
html=html.replace("const filename=page.id+'.png'","const filename=page.filename")
html=html.replace("'../../'+page.svg","'../'+page.svg")
html=html.replace("location.href='../修订_v0.2/预览.html'","location.href='../UI过程稿/补充_v0.3/预览.html'")
(TARGET/'预览.html').write_text(html,encoding='utf-8',newline='\n')
print(f'Exported {len(pages)} selected PNGs, directory and preview.')
