"""UI v0.2: apply the user's review without overwriting v0.1 artifacts."""
from pathlib import Path
import importlib.util
import json
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
VERSION = '修订_v0.2'
OUT = ROOT / 'UI设计源文件' / VERSION
OUT.mkdir(parents=True, exist_ok=True)
spec = importlib.util.spec_from_file_location('ui_v01', Path(__file__).with_name('生成初稿.py'))
base = importlib.util.module_from_spec(spec)
sys.dont_write_bytecode = True
spec.loader.exec_module(base)
C = base.C
C.update(bg='#FFFFFF', ink='#171717', text='#303030', muted='#737373',
         green='#171717', light='#F5F5F5', line='#E7E7E7', orange='#515151',
         amber='#F7F7F7', red='#333333', pink='#F6F6F6', gray='#F3F3F3')
PAGES = []


class Page(base.Page):
    def __init__(self, key, title, height=1000, note=''):
        super().__init__(key, title, height)
        self.parts[2] = '<desc>校园二手交易系统 UI v0.2 修订稿，白底黑字。可导入的矢量素材，样例数据均为虚构。</desc>'
        self.links = []
        self.note = note

    def header(self, active='商品广场', seller=False):
        self.line(80,79,1360,79)
        self.text(80,48,'校园集市',23,C['ink'],700)
        for x,label in [(324,'商品广场'),(454,'发布商品'),(584,'我的交易')]:
            self.text(x,48,label,16,C['ink'] if label==active else C['muted'],600 if label==active else 400)
            if label==active:self.line(x,78,x+64,78,C['ink'],2)
        self.text(1220,48,'邮箱已验证',13,C['muted'],anchor='end')
        self.text(1360,48,'林同学' if seller else '周同学',15,anchor='end')

    def footer(self):
        self.line(80,self.height-42,1360,self.height-42)
        self.text(80,self.height-18,'校园集市',12,C['muted'])

    def card(self,x,y,w,h):
        self.rect(x,y,w,h,r=8,stroke=C['line'])

    def link(self, x, y, w, h, target, label):
        self.links.append(dict(x=x, y=y, width=w, height=h, target=target, label=label))

    def nav(self, x, y, label, target, w=150):
        self.text(x, y, label, 14, C['green'])
        self.link(x, y-22, w, 32, target, label)

    def art(self, x, y, w, h, kind='book'):
        super().art(x, y, w, h, 'book' if kind == 'book_wear' else kind)
        if kind == 'book_wear':
            scale = min(w/280, h/220)
            self.parts.append(f'<g transform="translate({x+(w-240*scale)/2} {y+(h-180*scale)/2}) scale({scale})">')
            self.path('M177 145 l10 4 M176 151 l9 3 M180 157 l6 2', stroke='#E2D6B5', width=3)
            self.parts.append('<circle cx="181" cy="152" r="20" fill="none" stroke="#A76825" stroke-width="2"/>')
            self.parts.append('</g>')

    def save(self):
        self.footer()
        self.parts.append('</svg>')
        svg='\n'.join(self.parts)+'\n'
        for before,after in {'#CBD6CF':'#D3D3D3','#A0ABA4':'#A3A3A3','#BCC9BF':'#C2C2C2'}.items():
            svg=svg.replace(before,after)
        (OUT/(self.key+'.svg')).write_text(svg, encoding='utf-8', newline='\n')
        PAGES.append(dict(id=self.key, title=self.title, width=1440, height=self.height, note=self.note,
                          svg=f'UI设计源文件/{VERSION}/{self.key}.svg',
                          png=f'UI过程稿/{VERSION}/{self.key}.png', hotspots=self.links))


WORK = 'UI-04_个人工作台'
SELL_LIST = 'UI-07a_卖方待答复预约'
BUY_LIST = 'UI-07b_买方预约与待确认'
CANCEL_LIST = 'UI-07c_取消待答复订单'
SELL_DETAIL = 'UI-08a_订单详情_待卖家接受'
BUY_DETAIL = 'UI-08b_订单详情_确认方案'
CHANGE_DETAIL = 'UI-08c_订单详情_方案修改'
WAIT_DETAIL = 'UI-08d_订单详情_等待卖家接受'
CANCEL = 'UI-08v_取消协商变体'


def browse():
    p=Page('UI-02_商品浏览','商品浏览与组合查询',760,
           '依最新意见改为白底黑字；缩小商品图，预览仅保留名称、价格、发布人和库存。新旧及磨损移到详情。')
    p.header()
    p.text(80,146,'商品广场',28,C['ink'],700)
    p.input(850,110,398,'搜索商品名称或描述',True,44);p.button(1260,110,100,'搜索',h=44)
    p.text(80,214,'分类',15,C['muted'])
    for x,label in [(170,'全部'),(264,'书籍教材'),(394,'数码电子'),(524,'生活用品'),(654,'文体用品')]:
        if label=='全部':p.button(x,190,72,label,'soft',36)
        else:p.text(x,214,label,15)
    p.text(80,274,'价格',15,C['muted'])
    p.input(170,246,100,'最低价',True);p.text(285,274,'—',14,C['muted']);p.input(310,246,100,'最高价',True)
    p.text(460,274,'交易类型',15,C['muted'])
    for x,label,selected in [(552,'全部',True),(642,'售卖',False),(732,'赠送',False)]:
        p.check(x,268,selected);p.text(x+17,274,label,15)
    p.text(862,274,'状态',15,C['muted']);p.input(920,246,164,'已发布       ▾')
    p.text(1360,274,'重置',15,C['ink'],anchor='end');p.line(80,316,1360,316)
    p.text(80,361,'全部商品',18,C['ink'],600);p.text(176,361,'4 件',14,C['muted'])
    products=[('高等数学教材（上册）','book','10.00','6','林同学'),
              ('无线头戴式耳机','headphone','45.00','1','陈同学'),
              ('暖光阅读台灯','lamp','25.00','2','许同学'),
              ('桌面绿植','plant','0.00','1','张同学')]
    for n,(name,kind,price,qty,seller) in enumerate(products):
        x=80+n*326
        p.art(x,388,302,146,kind)
        p.text(x,569,name,18,C['ink'],500)
        p.text(x,608,'¥ '+price,23,C['ink'],600)
        p.text(x,646,seller,14,C['muted']);p.text(x+302,646,'库存 '+qty+' 件',14,C['muted'],anchor='end')
        if n==0:p.link(x,388,302,276,'UI-03_商品详情与预约','查看教材详情')
    p.save()


def detail():
    p=Page('UI-03_商品详情与预约','商品详情与数量预约',1120,
           '按第2条意见增加二手标签、磨损细节图与文字说明；本页为周同学预约林同学教材。')
    p.header();p.text(80,120,'商品广场  /  书籍教材  /  商品详情',14,C['muted'])
    p.link(80,98,90,30,'UI-02_商品浏览','返回商品广场')
    p.card(80,152,1280,678);p.art(108,180,568,448)
    p.art(108,646,100,84);p.rect(108,646,100,84,'none',12,C['green'])
    p.art(224,646,100,84,'book_wear')
    p.text(108,762,'商品全貌',14,C['muted']);p.text(224,762,'磨损细节',14,C['muted'])
    p.pill(724,182,'已发布');p.pill(820,182,'售卖','gray',64);p.pill(900,182,'二手','gray',64)
    p.text(724,251,'高等数学教材（上册）',29,C['ink'],700)
    p.text(724,288,'书籍教材 · 使用一学期，内页有少量铅笔笔记',15,C['muted'])
    p.text(724,351,'¥ 10.00',40,C['green'],700);p.text(916,349,'/ 件',15,C['muted'])
    p.text(724,390,'可用数量',15,C['muted']);p.text(820,390,'6 件',18,C['ink'],600)
    p.rect(724,416,600,76,C['light'],10);p.text(744,445,'支持售后退款',16,C['green'],600)
    p.text(744,472,'收货后 168 小时内可申请，需退货验收后退款。',15)
    p.line(724,516,1324,516);p.text(724,552,'预约数量',16)
    p.button(844,526,44,'−','secondary',42);p.input(900,526,68,'3',h=42);p.button(980,526,44,'+','secondary',42)
    p.text(1044,552,'最多 6 件',14,C['muted']);p.text(724,602,'预约金额',16)
    p.text(1324,603,'¥ 30.00',27,C['ink'],700,'end')
    p.text(724,638,'提交后等待卖家接受，再共同确认付款与交付方案。',15,C['muted'])
    p.button(724,668,600,'提交预约',h=52)
    p.link(724,668,600,52,'UI-03v_预约反馈变体','查看预约反馈示例')
    p.text(724,749,'发布者',14,C['muted']);p.text(799,749,'林同学 · 学校邮箱已验证',15)
    p.text(1324,790,'举报商品',14,C['muted'],anchor='end')
    p.card(80,854,1280,178);p.text(108,892,'商品描述与磨损情况',19,C['ink'],600)
    p.lines(108,929,['新旧情况：二手，使用一学期。',
        '磨损说明：封面右下角轻微磨损（见细节图），内页有少量铅笔笔记，无缺页，装订完好。',
        '具体交付安排在预约接受后由双方确认。'],16,gap=31)
    p.save()


def publish():
    p=Page('UI-06_发布商品','发布与编辑商品',1260,
           '按第3条意见增加全新闲置/二手单选，图片与描述共同说明使用和磨损情况；新旧情况独立于售卖/赠送。')
    p.header('发布商品',True);p.text(80,144,'发布闲置',30,C['ink'],700)
    p.text(80,177,'先填写商品信息，审核通过后向校内用户展示。',16,C['muted'])
    p.card(80,208,880,954);p.text(108,247,'基本信息',20,C['ink'],600)
    p.text(108,286,'商品名称 *',15);p.input(108,302,824,'高等数学教材（上册）')
    p.text(108,381,'商品图片',15);p.art(108,398,144,108);p.art(268,398,144,108,'book_wear')
    p.rect(428,398,144,108,'#FAFCF9',12,C['line'])
    p.text(500,443,'+',30,C['green'],anchor='middle');p.text(500,478,'添加图片',15,C['muted'],anchor='middle')
    p.lines(598,432,['已添加 2 / 9 张','JPG / PNG，单张不超过 5MB'],14,C['muted'])
    p.text(108,535,'上传全貌和磨损细节，便于买家了解实物情况。',14,C['muted'])
    p.text(108,575,'新旧情况 *',15)
    p.check(120,606,False);p.text(139,612,'全新闲置（未使用）',16)
    p.check(400,606,True);p.text(419,612,'二手（已使用）',16)
    p.text(108,664,'分类 *',15);p.input(108,680,394,'书籍教材                           ▾')
    p.text(538,664,'交易类型 *',15)
    p.check(548,702,True);p.text(566,708,'售卖',16);p.check(678,702,False);p.text(696,708,'免费赠送',16)
    p.text(108,765,'单价 *',15);p.input(108,781,394,'¥  10.00')
    p.text(538,765,'数量 *',15);p.input(538,781,394,'6')
    p.text(108,865,'售后声明 *',15)
    p.check(120,897,True);p.text(139,903,'支持售后退款',16)
    p.check(360,897,False);p.text(379,903,'不支持售后退款',16)
    p.text(108,937,'售卖须明确选择；声明随订单保留。',14,C['muted'])
    p.text(108,983,'商品描述与磨损情况 *',15)
    p.rect(108,1000,824,118,C['white'],8,C['line'])
    p.lines(122,1030,['二手，使用一学期。封面右下角轻微磨损（见细节图）。',
                    '内页有少量铅笔笔记，无缺页，装订完好。'],15,gap=31)
    p.text(108,1144,'说明使用情况、磨损位置和已知问题；全新闲置可说明未使用情况。',13,C['muted'])
    p.card(992,208,368,266);p.text(1020,247,'发布前请检查',20,C['ink'],600)
    for y,head,sub in [(291,'新旧情况明确','选择全新闲置或二手。'),(359,'图片与文字一致','说明使用情况与磨损位置。'),(427,'审核通过后公开','驳回后可修改并重新提交。')]:
        p.circle(1026,y-5,5,C['green']);p.text(1044,y,head,16,C['ink'],600);p.text(1044,y+25,sub,14,C['muted'])
    p.button(992,504,368,'提交审核',h=50);p.button(992,568,368,'保存草稿','secondary',48)
    p.text(992,650,'* 为必填项',14,C['muted'])
    p.lines(992,680,['免费赠送时金额为 0，','不进入付款与退款流程。'],15,C['muted'])
    p.save()


def workspace():
    p=Page(WORK,'个人工作台：买方与卖方入口',1000,
           '按第4、5、6、7、10条意见分设入口；点击买方/卖方待办卡片进入列表，再选订单查看详情。')
    p.header('我的交易',True);base.sidebar(p)
    p.text(348,159,'个人工作台',28,C['ink'],700)
    p.text(348,193,'分别查看买入与卖出的待处理交易。',16,C['muted'])
    cards=[(348,'2','买方预约与待确认','等待卖家接受或确认方案',BUY_LIST),
           (606,'1','卖方待答复','尚未接受的预约',SELL_LIST),
           (864,'1','商品草稿','完善后可提交审核','UI-06_发布商品'),
           (1122,'0','待处理售后','当前没有待答复申请',None)]
    for x,num,label,sub,target in cards:
        p.card(x,222,238,148);p.text(x+20,258,label,16,C['ink'],600)
        p.text(x+20,308,num,34,C['green'],700);p.text(x+20,341,sub,13,C['muted'])
        if target:
            p.text(x+218,306,'→',20,C['green'],anchor='end');p.link(x,222,238,148,target,label)
    p.card(348,400,1012,492)
    p.text(374,443,'我卖出的',20,C['green'],600);p.text(520,443,'我买到的',18,C['muted'])
    p.link(506,417,118,40,BUY_LIST,'查看我买到的待确认交易')
    p.line(374,463,464,463,C['green'],3)
    p.nav(1180,441,'取消待答复 →',CANCEL_LIST,154)
    p.text(374,508,'待确认 · 尚未接受',16,C['orange'],600)
    p.text(1334,508,'1 笔',14,C['muted'],anchor='end');p.line(374,530,1334,530)
    p.text(374,565,'订单 O20261104001 · 11-04 14:00',14,C['muted'])
    p.art(374,592,120,112);p.text(514,625,'高等数学教材（上册）',19,C['ink'],600)
    p.text(514,658,'买家：周同学   ·   二手   ·   ¥10.00 × 3 件',15,C['muted'])
    p.text(514,693,'接受截止：11 月 5 日 14:00',15,C['orange'])
    p.text(1334,628,'¥ 30.00',24,C['ink'],700,'end')
    p.button(1182,660,152,'处理预约',h=44);p.link(1182,660,152,44,SELL_DETAIL,'处理这笔卖方预约')
    p.line(374,732,1334,732)
    p.nav(374,779,'查看全部待答复预约 →',SELL_LIST,248)
    p.text(374,841,'待确认方案与取消协商，也可从对应的买方或卖方列表进入。',14,C['muted'])
    p.save()


def queue(role):
    buyer=role=='buyer';key=BUY_LIST if buyer else SELL_LIST
    p=Page(key,'买方预约与待确认列表' if buyer else '卖方待答复预约列表',1000,
           '林同学的本人交易；等待卖家接受与等待方案确认分别标明。' if buyer else '林同学的本人卖方预约；先列出所有尚未接受的预约，再选择一笔处理。')
    p.header('我的交易',True);p.nav(80,122,'← 返回个人工作台',WORK,180)
    p.text(80,174,'买方预约与待确认' if buyer else '卖方待答复预约',30,C['ink'],700)
    p.text(80,210,'我作为买家：等待卖家接受，或双方尚未确认同一方案。' if buyer else '我作为卖家：集中处理本人商品尚未接受的预约。',16,C['muted'])
    p.nav(1188,173,'切换卖方列表 →' if buyer else '切换买方列表 →',SELL_LIST if buyer else BUY_LIST,172)
    p.card(80,242,1280,634)
    if buyer:
        p.button(108,266,180,'全部待确认 2','soft',38)
        p.text(324,292,'等待卖家接受 1',15,C['muted']);p.text(520,292,'方案待确认 1',15,C['muted'])
    else:
        p.button(108,266,188,'预约待答复 1','soft',38)
        p.text(332,292,'方案待确认 0',15,C['muted'])
    p.nav(1174,292,'取消待答复 →',CANCEL_LIST,158);p.line(108,328,1332,328)
    rows=[dict(oid='O20261104002',kind='headphone',name='无线头戴式耳机',party='卖家：陈同学',
               amount='45.00',quantity='1',unit='45.00',status='待确认 · 待卖家接受',
               desc='接受截止：11 月 5 日 13:30',target=WAIT_DETAIL,button='查看预约'),
          dict(oid='O20261104003',kind='lamp',name='暖光阅读台灯',party='卖家：许同学',
               amount='25.00',quantity='1',unit='25.00',status='待确认 · 方案待确认',
               desc='卖家已接受并确认方案，等待你确认',target=BUY_DETAIL,button='确认方案')]
    if not buyer:
        rows=[dict(oid='O20261104001',kind='book',name='高等数学教材（上册）',party='买家：周同学',
                   amount='30.00',quantity='3',unit='10.00',status='待确认 · 待我接受',
                   desc='接受截止：11 月 5 日 14:00',target=SELL_DETAIL,button='处理预约')]
    for n,row in enumerate(rows):
        y=350+n*216
        p.text(108,y+8,row['oid'],14,C['muted']);p.pill(1106,y-14,row['status'],'orange',226)
        p.art(108,y+34,130,126,row['kind'])
        p.text(266,y+65,row['name'],21,C['ink'],600)
        p.text(266,y+100,f"{row['party']}   ·   二手   ·   ¥{row['unit']} × {row['quantity']} 件",15,C['muted'])
        p.text(266,y+138,row['desc'],15,C['orange'] if '截止' in row['desc'] else C['muted'])
        p.text(1332,y+65,'¥ '+row['amount'],25,C['ink'],700,'end')
        p.button(1174,y+100,158,row['button'],h=44);p.link(1174,y+100,158,44,row['target'],row['button'])
        p.line(108,y+190,1332,y+190)
    p.text(720,831,'已展示全部待确认交易' if buyer else '已展示全部未接受预约',14,C['muted'],anchor='middle')
    p.save()


def cancel_queue():
    p=Page(CANCEL_LIST,'取消待答复：买方与卖方',1000,
           '取消申请的分支示例；林同学作为买方和卖方，都能从工作台及对应列表找到待答复订单。')
    p.header('我的交易',True);p.nav(80,122,'← 返回个人工作台',WORK,180)
    p.text(80,176,'取消待答复',30,C['ink'],700)
    p.text(80,210,'按我在订单中的身份查看；对方同意前，订单状态和库存占用保持不变。',16,C['muted'])
    for y,title,oid,name,party,reason,amount,target in [
        (246,'我作为买方','O20261104003','暖光阅读台灯','卖家 许同学申请取消','临时无法按约交付，希望协商取消。','25.00',BUY_LIST),
        (536,'我作为卖方','O20261104001','高等数学教材（上册）','买家 周同学申请取消','学习计划调整，希望协商取消。','30.00',SELL_LIST)]:
        p.card(80,y,1280,264);p.pill(108,y+22,title,width=122)
        p.text(108,y+88,name,22,C['ink'],600);p.text(1332,y+86,'¥ '+amount,24,C['green'],700,'end')
        p.text(108,y+124,oid+'   ·   原订单：待确认',14,C['muted'])
        p.text(108,y+164,party,17,C['ink'],600);p.text(108,y+198,'原因：'+reason,15,C['muted'])
        p.button(1174,y+168,158,'答复取消申请',h=44);p.link(1174,y+168,158,44,CANCEL,'查看双方取消答复画板')
        p.nav(900,y+198,'返回对应交易列表',target,214)
    p.save()


def order(mode='seller'):
    seller=mode=='seller';changed=mode=='changed';waiting=mode=='waiting'
    key={'seller':SELL_DETAIL,'buyer':BUY_DETAIL,'changed':CHANGE_DETAIL,'waiting':WAIT_DETAIL}[mode]
    title={'seller':'订单详情：卖家接受预约','buyer':'订单详情：买家确认方案',
           'changed':'订单详情：方案修改后重新确认','waiting':'订单详情：买方等待卖家接受'}[mode]
    p=Page(key,title,1100,'本页由个人工作台的对应身份列表进入；当前登录者为林同学。')
    if seller:
        name,kind,unit,qty,amount,oid,buyer,seller_name,time,condition=('高等数学教材（上册）','book','10.00',3,'30.00','001','周同学','林同学','14:00','二手 · 封面右下角轻微磨损，内页少量笔记')
    elif waiting:
        name,kind,unit,qty,amount,oid,buyer,seller_name,time,condition=('无线头戴式耳机','headphone','45.00',1,'45.00','002','林同学','陈同学','13:30','二手 · 耳罩边缘轻微磨损，功能正常')
    else:
        name,kind,unit,qty,amount,oid,buyer,seller_name,time,condition=('暖光阅读台灯','lamp','25.00',1,'25.00','003','林同学','许同学','14:00','二手 · 灯座轻微划痕，照明功能正常')
    p.header('我的交易',True)
    back=SELL_LIST if seller else BUY_LIST
    p.nav(80,120,'我的交易  /  '+('卖方待答复预约' if seller else '买方预约与待确认'),back,340)
    p.text(80,168,'订单详情',30,C['ink'],700);p.pill(234,141,'待确认','orange',84)
    p.text(1360,167,'O20261104'+oid,15,C['muted'],anchor='end')
    p.card(80,200,1280,92)
    for x,num,label,active in [(124,'1','预约与方案确认',True),(568,'2','付款与交付',False),(1010,'3','收货与结算',False)]:
        p.circle(x,246,18,C['green'] if active else C['gray']);p.text(x,252,num,15,C['white'] if active else C['muted'],600,'middle')
        p.text(x+34,252,label,17,C['green'] if active else C['muted'],600)
    p.line(350,246,502,246);p.line(754,246,944,246)
    p.card(80,316,828,276);p.text(108,356,'预约商品',20,C['ink'],600)
    p.text(880,355,'下单时信息',13,C['muted'],anchor='end');p.art(108,380,146,140,kind)
    p.text(278,411,name,21,C['ink'],600);p.text(278,447,f'售卖   ·   ¥{unit} × {qty} 件',16)
    p.pill(278,470,'支持售后退款',width=122);p.text(278,526,condition,14,C['muted'])
    p.text(880,412,'¥ '+amount,28,C['green'],700,'end');p.line(108,540,880,540)
    p.text(108,571,'预约编号 R20261104'+oid,14,C['muted']);p.text(880,571,'预约时间 11-04 '+time,14,C['muted'],anchor='end')
    p.card(80,616,828,132);p.text(108,655,'交易双方',19,C['ink'],600)
    p.text(108,702,'买家  '+buyer+('（我）' if buyer=='林同学' else ''),16)
    p.text(488,702,'卖家  '+seller_name+('（我）' if seller_name=='林同学' else ''),16)
    p.card(80,772,828,214);p.text(108,812,'交易记录',19,C['ink'],600)
    events=[(time,f'预约成功，占用 {qty} 件，等待卖家接受')]
    if not seller and not waiting:events.extend([('14:10','卖家接受预约，进入方案确认'),('14:12','卖家确认线上付款、见面交付')])
    if changed:events.append(('14:15','买家修改方案，双方确认已重置'))
    for n,(event_time,event) in enumerate(reversed(events)):
        y=846+n*34;p.circle(114,y-5,4,C['green'] if n==0 else '#BCC9BF')
        p.text(137,y,event_time,14,C['muted']);p.text(209,y,event,15)
    p.text(880,967,'举报订单',13,C['muted'],anchor='end')
    if seller or waiting:
        p.card(932,316,428,428);p.pill(960,342,'需要你处理' if seller else '等待卖家答复','orange',140)
        p.text(960,408,'周同学想预约 3 件' if seller else '已提交预约，等待接受',23,C['ink'],700)
        deadline='14:00' if seller else '13:30'
        p.lines(960,447,[f'接受截止：11 月 5 日 {deadline}','超过期限仍未接受，订单将自动取消。'],15,C['muted'])
        p.rect(960,504,372,88,C['light'],10)
        p.lines(978,538,['接受后仍为待确认，','双方确认同一方案后才能继续。'],15,C['green'])
        if seller:
            p.button(960,620,372,'接受预约',h=48);p.button(960,684,372,'拒绝预约','secondary',40)
        else:
            p.button(960,620,372,'返回买方列表','secondary',48);p.link(960,620,372,48,BUY_LIST,'返回买方列表')
            p.text(960,707,'申请取消',14,C['green'])
    else:
        p.card(932,316,428,670);p.text(960,358,'确认交易方案',23,C['ink'],700)
        p.text(960,391,'卖家已接受，等待双方确认同一方案。',14,C['muted'])
        p.rect(960,411,372,67,C['amber'] if changed else C['light'],8)
        p.lines(976,437,['方案已修改','原确认不再有效，双方须重新确认。'] if changed else ['当前方案：线上付款 · 见面交付','卖家已确认，等待你确认。'],14,C['orange'] if changed else C['green'],24)
        p.text(960,512,'付款方式',15);p.text(960,548,'线下付款' if changed else '线上付款',18,C['ink'],600)
        p.text(960,595,'交付方式',15);p.text(960,631,'见面交付',18,C['ink'],600)
        p.text(960,667,'线下付款仅支持见面交付。',14,C['muted']);p.line(960,689,1332,689)
        p.text(960,725,'买家（我）',15);p.pill(1220,704,'待确认','gray',112)
        p.text(960,768,'卖家',15);p.pill(1220,747,'待确认' if changed else '已确认','gray' if changed else 'green',112)
        p.button(960,804,372,'确认当前方案',h=48);p.button(960,866,372,'修改方案','secondary',44)
        if not changed:p.link(960,866,372,44,CHANGE_DETAIL,'查看修改方案后重新确认的示例')
        p.text(960,947,'申请取消',14,C['green']);p.link(960,925,112,36,CANCEL,'查看取消协商示例')
        p.text(1332,947,'未付款取消须对方同意',13,C['muted'],anchor='end')
    p.save()


def cancel_states():
    p=Page(CANCEL,'取消协商：申请与双方答复',1120,
           '第10条意见：工作台或买卖列表均可进入取消答复。下面是分支示例，图内同意/拒绝按钮不执行真实交易。')
    p.text(80,78,'取消协商',30,C['ink'],700);p.nav(1170,77,'← 返回待答复列表',CANCEL_LIST,190)
    p.text(80,113,'申请取消不改变原订单状态与库存占用，也不暂停原有倒计时。',16,C['muted'])
    p.card(80,148,620,408);p.text(108,192,'申请取消订单',23,C['ink'],700)
    p.text(108,231,'暖光阅读台灯 · 1 件 · ¥25.00',17)
    p.text(108,264,'O20261104003 · 申请人：林同学（买家）',14,C['muted'])
    p.text(108,307,'取消原因 *',15);p.rect(108,323,564,98,C['white'],8,C['line'])
    p.lines(122,355,['计划有变，希望与卖家协商取消。','对方同意前，订单仍为待确认。'],15)
    p.button(108,465,564,'提交取消申请',h=46)
    p.card(740,148,620,408);p.pill(768,172,'我发出的申请','gray',140)
    p.text(768,237,'等待卖家许同学答复',23,C['ink'],700)
    p.lines(768,280,['暖光阅读台灯 · O20261104003','原订单仍为待确认，占用 1 件未释放。','同意时还须核对订单尚未付款。'],16,C['muted'],34)
    p.button(768,465,564,'返回买方列表','secondary',46);p.link(768,465,564,46,BUY_LIST,'返回买方列表')
    for x,tag,head,object_line,reason,back in [
        (80,'我作为买方 · 待我答复','卖家许同学申请取消','台灯 · O20261104003 · ¥25.00','临时无法按约交付，希望协商取消。',BUY_LIST),
        (740,'我作为卖方 · 待我答复','买家周同学申请取消','教材 · O20261104001 · ¥30.00','学习计划调整，希望协商取消。',SELL_LIST)]:
        p.card(x,580,620,418);p.pill(x+28,604,tag,'orange',220)
        p.text(x+28,674,head,23,C['ink'],700);p.text(x+28,715,object_line,15,C['muted'])
        p.text(x+28,755,'原因：'+reason,15)
        p.text(x+28,796,'双方同意且尚未付款时，才会取消并释放占用。',15,C['muted'])
        p.button(x+28,837,272,'同意取消',h=48);p.button(x+316,837,276,'拒绝申请','secondary',48)
        p.nav(x+28,953,'返回对应交易列表 →',back,230)
    p.save()


def preview():
    target_dir=ROOT/'UI过程稿'/VERSION
    target_dir.mkdir(parents=True,exist_ok=True)
    template=(ROOT/'UI过程稿/初稿_v0.1/预览.html').read_text(encoding='utf-8')
    template=template.replace('UI 初稿预览','UI 修订稿预览').replace('v0.1 · 待审查','v0.2 · 本轮已确认')
    template=template.replace('首轮画板 · 10 张',f'修订画板 · {len(PAGES)} 张')
    template=template.replace('双击画板切换适应宽度与 100%。','双击画板切换适应宽度与 100%。<br>点击画板入口可跳转列表和详情。')
    template=template.replace('<span class="spacer"></span>','<span class="spacer"></span><button id="workspace" type="button">回到工作台</button><label><input id="show-links" type="checkbox"> 显示跳转区域</label>')
    template=template.replace('<img id="artboard" alt="" draggable="false">','<div id="stage"><img id="artboard" alt="" draggable="false"><div id="hotspots"></div></div>')
    template=template.replace('</style>','''
  #stage { position:relative; margin:0 auto; box-shadow:0 6px 24px #253e3210; }
  #artboard { width:100%; height:100%; margin:0; border:0; box-shadow:none; }
  #hotspots { position:absolute; inset:0; pointer-events:none; }
  .hotspot { position:absolute; pointer-events:auto; border:2px solid transparent; border-radius:7px; }
  .hotspot:hover, .hotspot:focus-visible, .show-links .hotspot { border-color:#187559; background:#18755914; }
  .toolbar label { font-size:13px; }
</style>''')
    for before,after in {'#253e32':'#171717','#eef1ee':'#F6F6F6','#344d42':'#303030',
        '#d7e0d8':'#E4E4E4','#187559':'#171717','#67ac89':'#777777','#dfe6df':'#E7E7E7',
        '#718078':'#737373','#156649':'#171717','#eaf4ee':'#F1F1F1','#f9fbf8':'#FAFAFA',
        '#64756a':'#666666','#a0473e':'#333333'}.items():
        template=template.replace(before,after)
    template=template.replace('静态设计画板：图内业务按钮用于展示设计；请通过左侧目录切换页面。无需登录或联网。',
        '可点击入口演示工作台、列表与详情的页面关系；接受、付款、同意取消等业务操作仅作展示。无需登录或联网。')
    code='const pages = '+json.dumps(PAGES,ensure_ascii=False).replace('<','\\u003c')+';\n'
    code+=r'''
const $=id=>document.getElementById(id);
let index=0;
try { const found=pages.findIndex(p=>p.id===decodeURIComponent(location.hash.slice(1))); if(found>=0)index=found; } catch(_){}
for(const [i,page] of pages.entries()){
  const button=document.createElement('button');button.type='button';button.className='page';
  const number=document.createElement('span');number.className='num';number.textContent=String(i+1).padStart(2,'0');
  const label=document.createElement('span');label.textContent=page.title;button.append(number,label);
  button.addEventListener('click',()=>show(i));$('pages').append(button);
  const option=document.createElement('option');option.value=i;option.textContent=`${i+1}. ${page.title}`;$('mobile-pages').append(option);
}
function resize(){
  const padding=innerWidth<=850?24:48;
  const page=pages[index];
  const scale=$('zoom').value==='fit'?Math.max(.1,($('viewport').clientWidth-padding)/page.width):Number($('zoom').value);
  $('stage').style.width=`${page.width*scale}px`;$('stage').style.height=`${page.height*scale}px`;
}
function show(i){
  index=Math.max(0,Math.min(pages.length-1,i));const page=pages[index];
  $('title').textContent=page.title;$('note').textContent=page.note||'沿用首轮已讨论的状态规则。';$('count').textContent=`${index+1} / ${pages.length}`;
  $('previous').disabled=index===0;$('next').disabled=index===pages.length-1;$('mobile-pages').value=index;
  [...$('pages').children].forEach((button,n)=>{button.classList.toggle('active',n===index);if(n===index)button.setAttribute('aria-current','page');else button.removeAttribute('aria-current');});
  const filename=page.id+'.png';$('error').style.display='none';$('stage').style.display='block';$('artboard').alt=page.title;$('artboard').src=filename;
  $('open-png').href=filename;$('open-svg').href='../../'+page.svg;
  $('hotspots').replaceChildren();
  for(const spot of page.hotspots){
    const a=document.createElement('a');a.className='hotspot';a.href='#'+encodeURIComponent(spot.target);a.title=spot.label;a.setAttribute('aria-label',spot.label);
    a.style.left=100*spot.x/page.width+'%';a.style.top=100*spot.y/page.height+'%';a.style.width=100*spot.width/page.width+'%';a.style.height=100*spot.height/page.height+'%';
    a.addEventListener('click',event=>{event.preventDefault();const next=pages.findIndex(p=>p.id===spot.target);if(next>=0)show(next);});$('hotspots').append(a);
  }
  $('viewport').scrollTop=0;$('viewport').scrollLeft=0;resize();history.replaceState(null,'','#'+encodeURIComponent(page.id));
}
$('previous').addEventListener('click',()=>show(index-1));$('next').addEventListener('click',()=>show(index+1));
$('workspace').addEventListener('click',()=>show(pages.findIndex(p=>p.id==='UI-04_个人工作台')));
$('mobile-pages').addEventListener('change',event=>show(Number(event.target.value)));$('zoom').addEventListener('change',resize);addEventListener('resize',resize);
$('show-links').addEventListener('change',event=>$('stage').classList.toggle('show-links',event.target.checked));
$('artboard').addEventListener('dblclick',()=>{$('zoom').value=$('zoom').value==='fit'?'1':'fit';resize();});
$('artboard').addEventListener('error',()=>{$('error').style.display='block';$('stage').style.display='none';});
addEventListener('keydown',event=>{if(event.target.matches('select,input,textarea'))return;if(event.key==='ArrowLeft'||event.key==='ArrowRight'){event.preventDefault();show(index+(event.key==='ArrowRight'?1:-1));}});
show(index);
'''
    template=re.sub(r'<script>[\s\S]*?</script>',lambda _:'<script>\n'+code+'</script>',template)
    (target_dir/'预览.html').write_text(template,encoding='utf-8',newline='\n')


if __name__=='__main__':
    browse();detail();publish();workspace()
    order('seller');order('buyer');order('changed')
    # Reuse accepted v0.1 variants through the v0.2 writer; v0.1 files stay intact.
    base.Page=Page
    base.reservation_states();base.goods_states()
    cancel_states();queue('seller');queue('buyer');cancel_queue();order('waiting')
    (OUT/'画板清单.json').write_text(json.dumps(dict(version='0.2',status='用户认可本轮修订，已按课程命名整理图片；待 Pixso 核对',pages=PAGES),
        ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    preview()
    print(f'Generated {len(PAGES)} revised artboards and offline preview.')
