"""Generate editable SVG UI mockups; PNG previews are rendered separately.

These are preparatory design assets for import into Pixso, not a working app.
Only standard SVG shapes/text are used, without remote resources or raster UI.
"""
from pathlib import Path
from html import escape
import json

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'UI设计源文件' / '初稿_v0.1'
OUT.mkdir(parents=True, exist_ok=True)
C = dict(bg='#F5F7F4', white='#FFFFFF', ink='#18372D', text='#344D42', muted='#67766C',
         green='#187559', light='#EAF4EE', line='#E1E8E1', orange='#9B621B', amber='#FFF5E5',
         red='#B34942', pink='#FFF0ED', gray='#EFF2EF')
PAGES = []


class Page:
    def __init__(self, key, title, height=1000):
        self.key, self.title, self.height = key, title, height
        self.parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="1440" height="{height}" viewBox="0 0 1440 {height}">',
                      f'<title>{escape(title)}</title>',
                      '<desc>校园二手交易系统 UI 初稿，可导入 Pixso 的矢量画板。样例数据均为虚构。</desc>']
        self.rect(0, 0, 1440, height, C['bg'])

    def rect(self, x, y, w, h, fill=None, r=0, stroke=None):
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill or C["white"]}"' + (f' stroke="{stroke}"' if stroke else '') + '/>')

    def text(self, x, y, value, size=16, color=None, weight=400, anchor='start'):
        self.parts.append(f'<text x="{x}" y="{y}" font-family="Microsoft YaHei, Noto Sans CJK SC, sans-serif" font-size="{size}" font-weight="{weight}" fill="{color or C["text"]}" text-anchor="{anchor}">{escape(str(value))}</text>')

    def lines(self, x, y, values, size=16, color=None, gap=28, weight=400):
        for n, line in enumerate(values): self.text(x, y+n*gap, line, size, color, weight)

    def line(self, x1, y1, x2, y2, color=None, width=1):
        self.parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color or C["line"]}" stroke-width="{width}"/>')

    def circle(self, x, y, r, fill):
        self.parts.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}"/>')

    def path(self, d, fill='none', stroke=None, width=2):
        self.parts.append(f'<path d="{d}" fill="{fill}"' + (f' stroke="{stroke}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"' if stroke else '') + '/>')

    def card(self, x, y, w, h): self.rect(x, y, w, h, r=16, stroke=C['line'])

    def pill(self, x, y, label, tone='green', width=None):
        fg, bg = {'green':(C['green'], C['light']), 'orange':(C['orange'], C['amber']),
                  'gray':(C['muted'], C['gray']), 'red':(C['red'], C['pink'])}[tone]
        w = width or (len(label)*14+24)
        self.rect(x, y, w, 28, bg, 7)
        self.text(x+w/2, y+19, label, 13, fg, 500, 'middle')

    def button(self, x, y, w, label, kind='primary', h=46):
        fill, color, stroke = {'primary':(C['green'], C['white'], None),
            'secondary':(C['white'], C['text'], C['line']), 'soft':(C['light'], C['green'], None),
            'disabled':(C['gray'], '#A0ABA4', None), 'danger':(C['pink'], C['red'], None)}[kind]
        self.rect(x, y, w, h, fill, 9, stroke)
        self.text(x+w/2, y+h/2+6, label, 16, color, 600, 'middle')

    def input(self, x, y, w, value='', placeholder=False, h=44):
        self.rect(x, y, w, h, C['white'], 8, C['line'])
        self.text(x+14, y+28, value, 15, C['muted'] if placeholder else C['text'])

    def check(self, x, y, selected=True, radio=True):
        if radio:
            self.circle(x, y, 8, C['green'] if selected else '#CBD6CF')
            self.circle(x, y, 6, C['white'])
            if selected: self.circle(x, y, 4, C['green'])
        else:
            self.rect(x-8, y-8, 16, 16, C['green'] if selected else C['white'], 4, C['line'])
            if selected: self.path(f'M{x-4} {y} l3 3 l5 -6', stroke=C['white'])

    def header(self, active='商品广场', seller=False):
        self.rect(0, 0, 1440, 80, C['white'])
        self.line(0, 79, 1440, 79)
        self.rect(72, 22, 36, 36, C['green'], 11)
        self.path('M82 46 C80 30 98 29 99 30 C100 44 92 50 82 46 Z', '#CFE6CD')
        self.path('M83 48 L95 35', stroke=C['white'], width=1.5)
        self.text(120, 49, '校园集市', 23, C['ink'], 700)
        for x, label in [(324,'商品广场'), (454,'发布商品'), (584,'我的交易')]:
            self.text(x, 48, label, 16, C['green'] if label == active else C['muted'], 600 if label == active else 400)
            if label == active: self.rect(x, 76, 64, 3, C['green'], 1)
        self.pill(1100, 27, '邮箱已验证', width=100)
        self.circle(1234, 40, 18, C['light'])
        self.text(1234, 46, '林' if seller else '周', 15, C['green'], 600, 'middle')
        self.text(1264, 46, '林同学' if seller else '周同学', 15)

    def footer(self):
        self.line(80, self.height-58, 1360, self.height-58)
        self.text(80, self.height-28, '校园集市 · 校内闲置交易', 13, C['muted'])
        self.text(1360, self.height-28, '让闲置继续被需要', 13, C['muted'], anchor='end')

    def art(self, x, y, w, h, kind='book'):
        # Native vector product illustrations, intentionally retained as editable shapes.
        self.rect(x, y, w, h, {'book':'#E7EEE3','headphone':'#ECEAE5','lamp':'#EEEADF','plant':'#E6EEE8'}[kind], 12)
        scale = min(w/280, h/220)
        self.parts.append(f'<g transform="translate({x+(w-240*scale)/2} {y+(h-180*scale)/2}) scale({scale})">')
        if kind == 'book':
            self.rect(54, 19, 147, 160, '#CCD9C8', 9)
            self.rect(42, 7, 147, 160, '#527B60', 9)
            self.rect(42, 7, 12, 160, '#3D604A', 5)
            self.rect(65, 32, 100, 3, '#BCD0BB', 1)
            self.text(69, 65, '高等数学', 21, '#FFFFFF', 600)
            self.text(70, 90, '上册', 14, '#DFE9DC')
            self.path('M68 135 Q90 101 110 125 T169 111', stroke='#D7E7CC', width=2)
            self.text(69, 151, 'MATHEMATICS', 10, '#D7E7CC')
        elif kind == 'headphone':
            self.path('M65 107 V83 C65 13 177 13 177 83 V108', stroke='#575B58', width=19)
            self.rect(48, 88, 40, 69, '#343C38', 16)
            self.rect(153, 88, 40, 69, '#343C38', 16)
            self.rect(56, 98, 19, 48, '#757D76', 8)
            self.rect(166, 98, 19, 48, '#757D76', 8)
        elif kind == 'lamp':
            self.rect(57, 156, 132, 13, '#B7AD8F', 7)
            self.path('M124 155 L124 86 L172 43', stroke='#A89B79', width=9)
            self.path('M137 39 L173 27 L202 65 L148 86 Z', '#F8F5DD')
            self.path('M147 87 L203 66', stroke='#D8CFAE', width=3)
            self.circle(171, 44, 5, '#A89B79')
        else:
            self.path('M119 135 C121 90 114 63 121 26', stroke='#6D8A58', width=6)
            self.path('M119 101 C61 111 52 75 63 58 C98 55 122 70 119 101', '#6D9863')
            self.path('M121 77 C174 89 191 50 175 35 C141 33 121 48 121 77', '#8DAE7C')
            self.path('M119 50 C85 52 83 18 95 8 C115 9 129 26 119 50', '#5E8555')
            self.path('M79 125 L164 125 L154 174 L90 174 Z', '#C6AA91')
            self.rect(75, 122, 92, 13, '#D9BDA0', 5)
        self.parts.append('</g>')

    def save(self):
        self.footer()
        self.parts.append('</svg>')
        path = OUT / (self.key+'.svg')
        path.write_text('\n'.join(self.parts)+'\n', encoding='utf-8', newline='\n')
        PAGES.append(dict(id=self.key, title=self.title, width=1440, height=self.height,
                          svg=f'UI设计源文件/初稿_v0.1/{self.key}.svg',
                          png=f'UI过程稿/初稿_v0.1/{self.key}.png'))


def browse():
    p = Page('UI-02_商品浏览', '商品浏览与组合查询')
    p.header()
    p.text(80, 150, '发现校内好物', 32, C['ink'], 700)
    p.text(80, 183, '书本、数码与日常闲置，在校园里找到新主人。', 16, C['muted'])
    p.input(850, 132, 398, '搜索商品名称或描述', True, 48)
    p.button(1260, 132, 100, '搜索', h=48)
    p.card(80, 218, 1280, 164)
    p.text(106, 258, '分类', 15, C['muted'])
    for x, label in [(170,'全部'),(264,'书籍教材'),(394,'数码电子'),(524,'生活用品'),(654,'文体用品')]:
        if label=='全部': p.button(x, 234, 72, label, 'soft', 36)
        else: p.text(x, 258, label, 15)
    p.line(106, 290, 1334, 290)
    p.text(106, 332, '价格', 15, C['muted'])
    p.input(170, 305, 100, '最低价', True)
    p.text(285, 333, '—', 14, C['muted'])
    p.input(310, 305, 100, '最高价', True)
    p.text(460, 332, '交易类型', 15, C['muted'])
    for x,label,selected in [(552,'全部',True),(642,'售卖',False),(732,'赠送',False)]:
        p.check(x, 327, selected)
        p.text(x+17, 333, label, 15)
    p.text(862, 332, '状态', 15, C['muted'])
    p.input(920, 305, 164, '已发布       ▾')
    p.text(1306, 333, '重置', 15, C['green'], anchor='end')
    p.text(80, 427, '全部商品', 21, C['ink'], 600)
    p.text(180, 427, '4 件', 14, C['muted'])
    p.text(1360, 427, '按当前筛选条件展示', 14, C['muted'], anchor='end')
    products=[('高等数学教材（上册）','book','10.00','6','林同学','售卖'),
              ('无线头戴式耳机','headphone','45.00','1','陈同学','售卖'),
              ('暖光阅读台灯','lamp','25.00','2','许同学','售卖'),
              ('桌面绿植 · 免费赠送','plant','0.00','1','张同学','赠送')]
    for n,(name,kind,price,qty,seller,trade) in enumerate(products):
        x=80+n*326
        p.card(x, 452, 302, 414)
        p.art(x+12, 464, 278, 210, kind)
        p.pill(x+24, 478, trade, 'green' if trade=='赠送' else 'gray', 56)
        p.text(x+20, 713, name, 18, C['ink'], 600)
        p.text(x+20, 751, '¥ '+price, 27, C['green'], 700)
        p.text(x+20, 789, '已发布', 14, C['green'])
        p.text(x+282, 789, '可用 '+qty+' 件', 14, C['muted'], anchor='end')
        p.line(x+20, 807, x+282, 807)
        p.text(x+20, 840, seller, 14, C['muted'])
        p.text(x+282, 840, '查看详情 →', 14, C['green'], anchor='end')
    p.save()


def detail():
    p=Page('UI-03_商品详情与预约','商品详情与数量预约',1050)
    p.header()
    p.text(80, 120, '商品广场  /  书籍教材  /  商品详情', 14, C['muted'])
    p.card(80, 152, 1280, 678)
    p.art(108, 180, 568, 448)
    p.art(108, 646, 100, 84)
    p.rect(108,646,100,84,'none',12,C['green'])
    p.text(108, 769, '商品图片  1 / 1', 14, C['muted'])
    p.pill(724, 182, '已发布')
    p.pill(820, 182, '售卖','gray',64)
    p.text(724, 251, '高等数学教材（上册）', 29, C['ink'], 700)
    p.text(724, 288, '书籍教材 · 内页有少量笔记，封面与装订完好', 15, C['muted'])
    p.text(724, 351, '¥ 10.00', 40, C['green'], 700)
    p.text(916, 349, '/ 件', 15, C['muted'])
    p.text(724, 390, '可用数量', 15, C['muted'])
    p.text(820, 390, '6 件', 18, C['ink'], 600)
    p.rect(724, 416, 600, 76, C['light'], 10)
    p.text(744, 445, '支持售后退款', 16, C['green'], 600)
    p.text(744, 472, '收货后 168 小时内可申请，需退货验收后退款。', 15, C['text'])
    p.line(724, 516, 1324, 516)
    p.text(724, 552, '预约数量', 16)
    p.button(844, 526, 44, '−', 'secondary', 42)
    p.input(900, 526, 68, '3', h=42)
    p.button(980, 526, 44, '+', 'secondary', 42)
    p.text(1044, 552, '最多 6 件', 14, C['muted'])
    p.text(724, 602, '预约金额', 16)
    p.text(1324, 603, '¥ 30.00', 27, C['ink'], 700, 'end')
    p.text(724, 638, '提交后等待卖家接受，再共同确认付款与交付方案。', 15, C['muted'])
    p.button(724, 668, 600, '提交预约', h=52)
    p.text(724, 749, '发布者', 14, C['muted'])
    p.text(799, 749, '林同学 · 学校邮箱已验证', 15)
    p.text(1324, 790, '举报商品', 14, C['muted'], anchor='end')
    p.card(80, 854, 1280, 106)
    p.text(108, 891, '商品描述', 18, C['ink'], 600)
    p.text(108, 927, '自用教材，内页有少量铅笔笔记，适合日常学习。具体交付安排在预约接受后由双方确认。', 16)
    p.save()


def publish():
    p=Page('UI-06_发布商品','发布与编辑商品',1120)
    p.header('发布商品', True)
    p.text(80, 144, '发布闲置', 30, C['ink'], 700)
    p.text(80, 177, '先填写商品信息，审核通过后向校内用户展示。', 16, C['muted'])
    p.card(80, 208, 880, 812)
    p.text(108, 247, '基本信息', 20, C['ink'], 600)
    p.text(108, 286, '商品名称 *', 15)
    p.input(108, 302, 824, '高等数学教材（上册）')
    p.text(108, 381, '商品图片', 15)
    p.art(108, 398, 164, 124)
    p.rect(288, 398, 164, 124, '#FAFCF9', 12, C['line'])
    p.text(370, 449, '+', 32, C['green'], anchor='middle')
    p.text(370, 483, '添加图片', 15, C['muted'], anchor='middle')
    p.lines(478, 437, ['已添加 1 / 9 张', 'JPG / PNG，单张不超过 5MB'], 14, C['muted'])
    p.text(108, 559, '分类 *', 15)
    p.input(108, 574, 394, '书籍教材                           ▾')
    p.text(538, 559, '交易类型 *', 15)
    p.check(548, 596, True); p.text(566, 602, '售卖', 16)
    p.check(678, 596, False); p.text(696, 602, '免费赠送', 16)
    p.text(108, 656, '单价 *', 15)
    p.input(108, 672, 394, '¥  10.00')
    p.text(538, 656, '数量 *', 15)
    p.input(538, 672, 394, '6')
    p.text(108, 752, '售后声明 *', 15)
    p.check(120, 784, True); p.text(139, 790, '支持售后退款', 16)
    p.check(360, 784, False); p.text(379, 790, '不支持售后退款', 16)
    p.text(108, 824, '售卖须明确选择；声明随订单保留。', 14, C['muted'])
    p.text(108, 866, '商品描述 *', 15)
    p.rect(108, 882, 824, 106, C['white'], 8, C['line'])
    p.lines(122, 911, ['自用教材，内页有少量铅笔笔记，封面与装订完好。', '具体交付安排在预约接受后由双方确认。'], 15)
    p.card(992, 208, 368, 266)
    p.text(1020, 247, '发布前请检查', 20, C['ink'], 600)
    for y,head,sub in [(291,'信息真实完整','描述成色与已知问题。'),(359,'售后约定清楚','买家预约前可以查看。'),(427,'审核通过后公开','驳回后可修改并重新提交。')]:
        p.circle(1026,y-5,5,C['green'])
        p.text(1044,y,head,16,C['ink'],600)
        p.text(1044,y+25,sub,14,C['muted'])
    p.button(992, 504, 368, '提交审核', h=50)
    p.button(992, 568, 368, '保存草稿', 'secondary', h=48)
    p.text(992, 650, '* 为必填项', 14, C['muted'])
    p.lines(992, 680, ['免费赠送时金额为 0，', '不进入付款与退款流程。'], 15, C['muted'])
    p.save()


def sidebar(p, selected='交易概览'):
    p.card(80, 126, 232, 752)
    p.circle(122, 174, 22, C['light']); p.text(122,181,'林',18,C['green'],600,'middle')
    p.text(156, 174, '林同学', 18, C['ink'], 600)
    p.text(156, 198, '学校邮箱已验证', 12, C['muted'])
    p.line(104, 225, 288, 225)
    for y,label in [(270,'交易概览'),(334,'我的商品'),(398,'售后服务'),(462,'我的举报'),(526,'本人业务记录'),(590,'账号信息')]:
        if label==selected: p.rect(96,y-29,200,48,C['light'],9)
        p.text(120,y,label,16,C['green'] if label==selected else C['text'],600 if label==selected else 400)
    p.lines(104, 808, ['同一账号可同时买入和卖出', '仅展示本人业务记录'], 12, C['muted'], 24)


def workspace():
    p=Page('UI-04_个人工作台','个人工作台与预约订单列表')
    p.header('我的交易', True); sidebar(p)
    p.text(348, 159, '下午好，林同学', 28, C['ink'], 700)
    p.text(348, 193, '有 1 笔预约等待你处理。', 16, C['muted'])
    for x,number,label,sub in [(348,'1','待接受预约','及时答复买家的预约'),(696,'1','商品草稿','完善后可提交审核'),(1044,'0','待处理售后','当前没有待答复申请')]:
        p.card(x, 222, 316, 138)
        p.text(x+22, 259, label, 15, C['muted'])
        p.text(x+22, 309, number, 34, C['green'], 700)
        p.text(x+76, 306, sub, 13, C['muted'])
    p.card(348, 390, 1012, 488)
    p.text(374, 433, '我卖出的', 20, C['green'], 600)
    p.text(520, 433, '我买到的', 18, C['muted'])
    p.line(374, 453, 464, 453, C['green'], 3)
    p.input(1014, 408, 320, '搜索订单编号或商品', True, 36)
    for x, label in [(374,'全部 1'),(475,'待确认 1'),(600,'待付款'),(707,'待交付'),(814,'交付中'),(921,'已完成'),(1028,'已取消')]:
        if x==374:p.button(x,478,88,label,'soft',34)
        else:p.text(x,500,label,14,C['muted'])
    p.line(374, 536, 1334, 536)
    p.text(374, 568, '订单 O20261104001 · 11-04 14:00', 14, C['muted'])
    p.pill(1168, 546, '待确认 · 待接受','orange',166)
    p.art(374, 596, 120, 112)
    p.text(514, 627, '高等数学教材（上册）', 19, C['ink'], 600)
    p.text(514, 660, '买家：周同学   ·   ¥10.00 × 3 件', 15, C['muted'])
    p.text(514, 695, '接受截止：11 月 5 日 14:00', 15, C['orange'])
    p.text(1334, 632, '¥ 30.00', 24, C['ink'], 700, 'end')
    p.button(1182, 662, 152, '处理预约', h=44)
    p.line(374, 736, 1334, 736)
    p.text(854, 801, '已展示全部订单', 14, C['muted'], anchor='middle')
    p.save()


def order(mode='seller'):
    seller=mode=='seller'
    changed=mode=='changed'
    key={'seller':'UI-08a_订单详情_待卖家接受','buyer':'UI-08b_订单详情_确认方案','changed':'UI-08c_订单详情_方案修改'}[mode]
    p=Page(key, {'seller':'订单详情：卖家接受预约','buyer':'订单详情：买家确认方案','changed':'订单详情：方案修改后重新确认'}[mode],1100)
    p.header('我的交易', seller)
    p.text(80, 120, '我的交易  /  订单详情', 14, C['muted'])
    p.text(80, 168, '订单详情', 30, C['ink'], 700)
    p.pill(234, 141, '待确认','orange',84)
    p.text(1360, 167, 'O20261104001', 15, C['muted'], anchor='end')
    p.card(80, 200, 1280, 92)
    for x,num,label,active in [(124,'1','预约与方案确认',True),(568,'2','付款与交付',False),(1010,'3','收货与结算',False)]:
        p.circle(x, 246, 18, C['green'] if active else C['gray'])
        p.text(x,252,num,15,C['white'] if active else C['muted'],600,'middle')
        p.text(x+34,252,label,17,C['green'] if active else C['muted'],600)
    p.line(350,246,502,246);p.line(754,246,944,246)
    p.card(80, 316, 828, 276)
    p.text(108, 356, '预约商品', 20, C['ink'], 600)
    p.text(880, 355, '下单时信息', 13, C['muted'], anchor='end')
    p.art(108, 380, 146, 140)
    p.text(278, 411, '高等数学教材（上册）', 21, C['ink'], 600)
    p.text(278, 447, '售卖   ·   ¥10.00 × 3 件', 16)
    p.pill(278, 470, '支持售后退款',width=122)
    p.text(880, 412, '¥ 30.00', 28, C['green'], 700, 'end')
    p.line(108,540,880,540)
    p.text(108, 571, '预约编号 R20261104001', 14, C['muted'])
    p.text(880, 571, '预约时间 11-04 14:00', 14, C['muted'], anchor='end')
    p.card(80, 616, 828, 132)
    p.text(108, 655, '交易双方', 19, C['ink'], 600)
    p.text(108, 702, '买家  周同学'+('' if seller else '（我）'), 16)
    p.text(488, 702, '卖家  林同学'+('（我）' if seller else ''), 16)
    p.card(80, 772, 828, 214)
    p.text(108, 812, '交易记录', 19, C['ink'], 600)
    events=[('14:00','预约成功，占用 3 件，等待卖家接受')]
    if not seller: events.append(('14:10','卖家接受预约，进入方案确认'))
    if not seller: events.append(('14:12', '卖家确认线上付款、见面交付'))
    if changed: events.append(('14:15', '买家修改方案，双方确认已重置'))
    for n,(time,event) in enumerate(reversed(events)):
        y=846+n*34
        p.circle(114,y-5,4,C['green'] if n==0 else '#BCC9BF')
        p.text(137,y,time,14,C['muted']);p.text(209,y,event,15)
    p.text(880, 967, '举报订单', 13, C['muted'], anchor='end')
    if seller:
        p.card(932, 316, 428, 428)
        p.pill(960, 342, '需要你处理','orange',112)
        p.text(960, 408, '周同学想预约 3 件', 23, C['ink'], 700)
        p.lines(960, 447, ['请在 11 月 5 日 14:00 前答复。', '超过期限仍未接受，订单将自动取消。'],15,C['muted'])
        p.rect(960, 504, 372, 88, C['light'], 10)
        p.lines(978, 538, ['接受后仍为待确认，', '双方确认同一方案后才能继续。'],15,C['green'])
        p.button(960, 620, 372, '接受预约', h=48)
        p.button(960, 684, 372, '拒绝预约', 'secondary', h=40)
    else:
        p.card(932, 316, 428, 670)
        p.text(960, 358, '确认交易方案', 23, C['ink'], 700)
        p.text(960, 391, '卖家已接受，等待双方确认同一方案。', 14, C['muted'])
        if changed:
            p.rect(960, 411, 372, 67, C['amber'], 8)
            p.lines(976, 437, ['方案已修改', '原确认不再有效，双方须重新确认。'],14,C['orange'],24)
        else:
            p.rect(960, 411, 372, 67, C['light'], 8)
            p.lines(976, 437, ['当前方案：线上付款 · 见面交付', '卖家已确认，等待你确认。'],14,C['green'],24)
        p.text(960, 512, '付款方式', 15)
        p.text(960, 548, '线下付款' if changed else '线上付款', 18, C['ink'], 600)
        p.text(960, 595, '交付方式', 15)
        p.text(960, 631, '见面交付', 18, C['ink'], 600)
        p.text(960, 667, '线下付款仅支持见面交付。', 14, C['muted'])
        p.line(960, 689, 1332, 689)
        p.text(960, 725, '买家（我）', 15)
        p.pill(1220,704,'待确认','gray',112)
        p.text(960, 768, '卖家', 15)
        p.pill(1220,747,'待确认' if changed else '已确认','gray' if changed else 'green',112)
        p.button(960, 804, 372, '确认当前方案', h=48)
        p.button(960, 866, 372, '修改方案', 'secondary', h=44)
        p.text(960, 947, '申请取消', 14, C['muted'])
        p.text(1332, 947, '未付款取消须对方同意', 13, C['muted'], anchor='end')
    p.save()


def reservation_states():
    p=Page('UI-03v_预约反馈变体','预约反馈的局部画板',1000)
    p.text(80, 82, '预约反馈', 30, C['ink'], 700)
    p.text(80, 116, '同一预约操作在不同结果下的局部界面', 16, C['muted'])
    data=[(80,156,'提交中','正在提交预约','请稍候，正在核对商品和可用数量。','请勿重复提交。','提交中…','disabled','gray'),
          (740,156,'预约成功','已预约 3 件','高等数学教材（上册） · ¥30.00','等待卖家在 11 月 5 日 14:00 前接受。','查看订单','primary','green'),
          (80,512,'库存变化','可用数量已变化','当前仅剩 2 件，原预约数量为 3 件。','本次未创建预约，请核对后重新提交。','核对最新商品','primary','orange'),
          (740,512,'提交失败','预约未成功','本次预约已确认失败，未占用商品数量。','已保留你填写的数量，请稍后重试。','重试预约','primary','red')]
    for x,y,label,head,a,b,button,kind,tone in data:
        p.card(x,y,620,324);p.pill(x+28,y+24,label,tone)
        p.text(x+28,y+99,head,25,C['ink'],700)
        p.lines(x+28,y+143,[a,b],16,C['muted'],31)
        if label=='预约成功':p.text(x+28,y+219,'订单 O20261104001',14,C['muted'])
        p.button(x+28,y+250,564,button,kind,h=46)
    p.save()


def goods_states():
    p=Page('UI-05v_商品管理与发布变体','商品管理与表单的局部变体',1070)
    p.text(80, 78, '商品管理与发布反馈', 30, C['ink'], 700)
    p.text(80, 111, '草稿、驳回、受限操作与重新审核', 16, C['muted'])
    p.card(80, 144, 1280, 238)
    p.pill(108, 167, '草稿 · 审核驳回', 'red', 164)
    p.text(108, 226, '高等数学教材（上册）', 23, C['ink'], 600)
    p.lines(108, 262, ['驳回原因：请补充封面清晰图片，并说明内页笔记情况。', '修改后可重新提交审核，审核通过前不会公开展示。'],16,C['muted'])
    p.button(108, 315, 170, '修改并重新提交',h=42)
    p.card(80, 406, 1280, 238)
    p.pill(108,429,'已发布')
    p.text(108, 488, '高等数学教材（上册）', 23, C['ink'], 600)
    p.text(108, 527, '存在 1 笔有效预约，占用 3 件；暂不能修改或直接下架。',16,C['orange'])
    p.text(108, 558, '可用数量 3 件；预约占用 3 件。',15,C['muted'])
    p.button(108,586,110,'编辑','disabled',40);p.button(234,586,110,'下架','disabled',40)
    p.button(1132,586,200,'查看关联订单','secondary',40)
    p.card(80, 668, 620, 270)
    p.text(108, 711, '提交前请完善售后声明',21,C['ink'],600)
    p.check(120,749,False);p.text(139,755,'支持售后退款',16)
    p.check(370,749,False);p.text(389,755,'不支持售后退款',16)
    p.text(108,797,'售卖商品必须明确选择，当前不能提交审核。',15,C['red'])
    p.button(108,841,564,'提交审核','disabled',46)
    p.card(740, 668, 620, 270)
    p.text(768,711,'免费赠送',21,C['ink'],600)
    p.text(768,754,'商品金额',15,C['muted']);p.text(1332,755,'¥ 0.00',25,C['green'],700,'end')
    p.lines(768,796,['无需付款，无退款流程。','数量与审核规则保持一致。'],15,C['muted'])
    p.button(768,866,564,'提交审核',h=46)
    p.save()


def cancel_states():
    p=Page('UI-08v_取消协商变体','取消申请与对方处理的局部画板',1000)
    p.text(80, 80, '取消协商',30,C['ink'],700)
    p.text(80,114,'同一未付款售卖订单的不同视角',16,C['muted'])
    p.card(80,156,620,660)
    p.text(108,202,'申请取消订单',25,C['ink'],700)
    p.text(108,240,'高等数学教材（上册） · 3 件 · ¥30.00',17)
    p.text(108,276,'订单 O20261104001',14,C['muted'])
    p.text(108,326,'取消原因 *',16)
    p.rect(108,344,564,120,C['white'],8,C['line'])
    p.lines(122,376,['临时调整了学习计划，','希望与卖家协商取消本次交易。'],15)
    p.rect(108,490,564,112,C['amber'],10)
    p.lines(126,524,['对方同意后才会取消订单并释放占用。','申请期间订单状态和库存占用保持不变，','原有超时倒计时继续。'],15,C['orange'],29)
    p.button(108,638,564,'提交取消申请',h=48)
    p.button(108,702,564,'暂不申请','secondary',44)
    p.card(740,156,620,302)
    p.pill(768,180,'买家视角','gray',100)
    p.text(768,247,'已提交取消申请',25,C['ink'],700)
    p.lines(768,287,['等待卖家答复，原订单仍为待确认。','预约占用 3 件尚未释放。'],16,C['muted'])
    p.button(768,369,564,'返回订单','secondary',48)
    p.card(740,482,620,334)
    p.pill(768,506,'卖家视角','gray',100)
    p.text(768,574,'周同学申请取消',25,C['ink'],700)
    p.lines(768,616,['原因：学习计划调整，希望协商取消。','同意时将再次核对订单是否尚未付款。'],16,C['muted'])
    p.button(768,705,270,'同意取消',h=48)
    p.button(1054,705,278,'拒绝申请','secondary',48)
    p.save()


if __name__=='__main__':
    browse(); detail(); publish(); workspace()
    order('seller');order('buyer');order('changed')
    reservation_states();goods_states();cancel_states()
    (ROOT/'UI设计源文件'/'初稿_v0.1'/'画板清单.json').write_text(
        json.dumps(dict(version='0.1',status='AI 初稿，待审查；待导入 Pixso 核对',pages=PAGES),ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(f'Generated {len(PAGES)} SVG artboards in {OUT}')
