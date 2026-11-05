"""Additional module mockups; retain confirmed v0.2 assets and report unchanged."""
from pathlib import Path
import importlib.util
import json
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent.parent
VERSION = '补充_v0.3'
OUT = ROOT / 'UI设计源文件' / VERSION
OUT.mkdir(parents=True, exist_ok=True)
spec = importlib.util.spec_from_file_location('ui_v02', Path(__file__).with_name('生成修订稿.py'))
ui = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ui)
ui.OUT, ui.VERSION = OUT, VERSION
C, PAGES = ui.C, ui.PAGES

LOGIN='UI-01_学校邮箱登录'
GOODS='UI-05_我的商品'
SCHEME='UI-08g_编辑交易方案'
PAY='UI-09_模拟线上付款'
RECEIPT='UI-08e_交付与收货'
METHODS='UI-08f_线下与赠送变体'
PAY_STATES='UI-09v_付款与结算变体'
TASKS='UI-10_我的代交任务'
TASK='UI-10a_代交任务详情'
DELIVERY_STATES='UI-10v_代交异常与改约'
AFTER_APPLY='UI-11_申请部分退货'
AFTER_REPLY='UI-11a_卖方处理售后'
AFTER_FUNDS='UI-11b_退款进度与返款'
AFTER_ADMIN='UI-11c_管理员售后核查'
AFTER_STATES='UI-11v_售后关键变体'
AUDIT='UI-12_商品审核'
REPORT='UI-13b_提交举报'
ADMIN_REPORT='UI-13_举报处理'
ADMIN_FUNDS='UI-13a_异常资金处理'
AUTHORITY='UI-14_授权与代交分配'
SETTINGS='UI-14a_账号限制与邮箱设置'
STATS='UI-15_成交与赠送统计'
LOGS='UI-15a_操作日志查询'
COMMON_STATES='UI-01v_校验与权限变体'


class Page(ui.Page):
    def __init__(self,key,title,height=1000,note='',actor='周同学',role='user'):
        super().__init__(key,title,height,note or '补充模块 AI 初稿，待用户审查；虚构样例为不同阶段或可选分支。')
        self.parts[2]='<desc>校园二手交易系统补充模块初稿，白底黑字和彩色商品图。待审查，非真实业务。</desc>'
        self.actor,self.role=actor,role

    def header(self,active='我的交易'):
        self.line(80,79,1360,79);self.text(80,48,'校园集市',23,C['ink'],700)
        if self.role=='admin':
            items=[(310,'商品审核',AUDIT),(456,'举报与异常',ADMIN_REPORT),(634,'权限与分配',AUTHORITY),(812,'统计与日志',STATS)]
        elif self.role=='courier':
            items=[(324,'我的代交任务',TASKS)]
        elif self.role=='anonymous':items=[]
        else:items=[(324,'我的商品',GOODS),(454,'交易方案',SCHEME),(584,'付款与交付',PAY),(754,'售后服务',AFTER_APPLY)]
        for x,label,target in items:
            self.text(x,48,label,16,C['ink'] if label==active else C['muted'],600 if label==active else 400)
            if self.role in ('admin','courier') or (self.actor=='周同学' and target!=GOODS) or (self.actor=='林同学' and target==GOODS):
                self.link(x,23,130,38,target,label)
            elif self.actor=='林同学' and target==AFTER_APPLY:self.link(x,23,130,38,AFTER_REPLY,label)
            if label==active:self.line(x,78,x+len(label)*16,78,C['ink'],2)
        if self.actor:
            self.text(1220,48,{'admin':'管理员','courier':'官方代交人'}.get(self.role,'邮箱已验证'),13,C['muted'],anchor='end')
            self.text(1360,48,self.actor,15,anchor='end')

    def heading(self,title,subtitle='',active='我的交易'):
        self.header(active);self.text(80,151,title,30,C['ink'],700)
        if subtitle:self.text(80,190,subtitle,16,C['muted'])

    def label_input(self,x,y,w,label,value='',h=44):
        self.text(x,y,label,15);self.input(x,y+16,w,value,h=h)

    def notice(self,x,y,w,lines):
        self.rect(x,y,w,len(lines)*27+24,C['light'],7)
        self.lines(x+16,y+30,lines,15,gap=27)

    def textarea(self,x,y,w,lines,h=100):
        self.rect(x,y,w,h,C['white'],7,C['line']);self.lines(x+14,y+29,lines,15,gap=28)

    def jump(self,x,y,w,label,target,kind='secondary',h=44):
        self.button(x,y,w,label,kind,h);self.link(x,y,w,h,target,'查看'+label+'画板')

    def state_card(self,x,y,w,h,label,title,lines):
        self.card(x,y,w,h);self.pill(x+24,y+22,label,'gray')
        self.text(x+24,y+94,title,22,C['ink'],700)
        self.lines(x+24,y+137,lines,15,C['muted'],30)


def login():
    p=Page(LOGIN,'学校邮箱注册与登录',actor='',role='anonymous')
    p.header();p.text(180,244,'学校邮箱登录',32,C['ink'],700)
    p.text(180,287,'验证邮箱后即可发布、预约和管理本人交易。',16,C['muted'])
    p.card(180,332,610,470)
    p.label_input(212,382,546,'学校邮箱','请输入学校邮箱')
    p.label_input(212,495,334,'邮箱验证码','输入验证码')
    p.button(562,511,196,'获取验证码','secondary',44)
    p.text(212,597,'验证码5分钟有效；再次发送须间隔60秒。',14,C['muted'])
    p.button(212,639,546,'验证并登录',h=50)
    p.text(212,738,'首次验证通过后建立账号，已有账号直接登录。',15,C['muted'])
    p.text(894,382,'使用说明',21,C['ink'],600)
    p.lines(894,429,['仅接受平台配置的学校邮箱域名。','同一邮箱只对应一个账号。','连续输错5次后，该验证码失效。'],16,C['muted'],40)
    p.line(894,566,1304,566)
    p.lines(894,614,['买卖身份使用同一账号。','代交及管理权限由平台授权。'],16,C['muted'],38)
    p.save()


def goods():
    p=Page(GOODS,'我的商品与审核状态',actor='林同学')
    p.heading('我的商品','查看本人商品，按状态继续处理。','我的商品')
    p.card(80,228,1280,666)
    for x,label in [(108,'全部 3'),(268,'草稿 1'),(438,'待审核 1'),(626,'已发布 1'),(814,'已下架 0')]:
        p.text(x,274,label,16,C['ink'] if x==108 else C['muted'],600 if x==108 else 400)
    p.line(108,302,1332,302)
    rows=[('book','高等数学教材（上册）','已发布','库存 3 件 · 有效预约占用 3 件','¥10.00',True),
          ('lamp','宿舍阅读灯','草稿','库存 1 件 · 尚未公开','¥25.00',False),
          ('plant','桌面绿植','待审核','库存 1 件 · 免费赠送','¥0.00',False)]
    for i,(kind,name,state,desc,price,locked) in enumerate(rows):
        y=326+i*180;p.art(108,y,112,108,kind)
        p.text(246,y+31,name,21,C['ink'],600);p.text(246,y+69,desc,15,C['muted'])
        p.text(246,y+102,state,15);p.text(1332,y+31,price,23,C['ink'],600,'end')
        if locked:
            p.button(1060,y+68,126,'编辑','disabled',38);p.button(1202,y+68,130,'下架','disabled',38)
            p.text(1332,y+139,'已有有效预约，暂不能修改或下架',13,C['muted'],anchor='end')
        else:p.button(1152,y+68,180,'继续编辑' if state=='草稿' else '查看审核进度','secondary',40)
        if i<2:p.line(108,y+159,1332,y+159)
    p.save()


def scheme():
    p=Page(SCHEME,'编辑付款与交付方案',1100)
    p.heading('修改交易方案','高等数学教材（上册） · O20261104001 · 售卖 ¥30.00','交易方案')
    p.card(80,228,780,566);p.text(108,272,'当前新方案',22,C['ink'],600)
    p.text(108,331,'付款方式',16)
    for x,label,checked in [(120,'线上付款',True),(362,'线下付款',False)]:p.check(x,372,checked);p.text(x+20,378,label,17)
    p.text(108,451,'交付方式',16)
    for x,label,checked in [(120,'见面交付',False),(362,'平台代交',True)]:p.check(x,492,checked);p.text(x+20,498,label,17)
    p.label_input(108,570,724,'交付说明','图书馆东门取件，教学楼南门交件')
    p.button(108,703,724,'保存新方案',h=48)
    p.card(892,228,468,566);p.text(920,272,'变更确认',22,C['ink'],600)
    p.lines(920,330,['原方案：线上付款、见面交付','新方案：线上付款、平台代交'],17,gap=42)
    p.notice(920,442,412,['保存后，双方原确认均失效。','须重新确认同一方案才能继续。'])
    p.lines(920,598,['售卖／赠送来自原订单，','此处不能重新选择。'],15,C['muted'])
    p.card(80,822,620,176);p.text(108,864,'线下售卖',19,C['ink'],600)
    p.lines(108,905,['仅可见面交付；平台代交不可选。','双方确认后进入待交付，由卖方确认实际收款。'],15,C['muted'])
    p.card(732,822,628,176);p.text(760,864,'免费赠送',19,C['ink'],600)
    p.lines(760,905,['无需付款，仅选择见面交付或平台代交。','双方确认后进入待交付，不进入待付款。'],15,C['muted'])
    p.save()


def pay():
    p=Page(PAY,'模拟线上付款')
    p.heading('待付款','双方已确认线上付款与平台代交方案。','付款与交付')
    p.card(80,228,780,558);p.text(108,271,'订单信息',21,C['ink'],600)
    p.art(108,306,152,142);p.text(286,344,'高等数学教材（上册）',23,C['ink'],600)
    p.text(286,386,'¥10.00 × 3 件 · 卖家：林同学',17);p.text(286,426,'O20261104001',14,C['muted'])
    p.line(108,480,832,480)
    p.lines(108,526,['进入待付款：11月4日 14:20','付款截止：11月4日 14:50','交付：平台代交 · 付款后才可取件'],16,gap=42)
    p.text(108,721,'普通取消申请不暂停付款期限。',14,C['muted'])
    p.card(892,228,468,558);p.pill(920,254,'模拟支付',width=106)
    p.text(920,347,'应付金额',16,C['muted']);p.text(920,411,'¥30.00',44,C['ink'],700)
    p.text(920,462,'剩余 20:00',22,C['ink'],600)
    p.text(920,504,'满30分钟仍未付款，自动取消。',15,C['muted'])
    p.button(920,557,412,'模拟付款 ¥30.00',h=50)
    p.text(920,650,'模拟结果不代表真实扣款。',14,C['muted'])
    p.nav(920,719,'查看付款与结算反馈 →',PAY_STATES,258)
    p.text(80,852,'付款成功后，可在原订单中查看交付进度。',15,C['muted'])
    p.save()


def receipt():
    p=Page(RECEIPT,'交付进度与买方收货',1100)
    p.heading('订单交付中','O20261104001 · ¥30.00 · 买家周同学／卖家林同学','付款与交付')
    p.card(80,228,800,594);p.text(108,272,'交付进度',22,C['ink'],600)
    for x,label,value in [(108,'付款','已付款'),(352,'代交','已交件'),(596,'买方收货','待确认')]:
        p.text(x,329,label,15,C['muted']);p.text(x,371,value,24,C['ink'],600)
    p.line(108,405,852,405)
    events=[('14:35','线上付款成功，货款待结算'),('15:00','赵同学记录取件，订单进入交付中'),('15:40','代交已交件，等待买方确认收到')]
    for n,(time,event) in enumerate(events):
        y=451+n*54;p.text(108,y,time,15,C['muted']);p.text(184,y,event,16)
    p.art(108,648,126,112);p.text(260,687,'高等数学教材（上册）',20,C['ink'],600)
    p.text(260,728,'二手 · ¥10.00 × 3 件',16,C['muted'])
    p.card(912,228,448,594);p.text(940,272,'确认收货',23,C['ink'],600)
    p.lines(940,324,['请核对已实际收到的商品与数量。','代交人交件不能代替你的确认。'],16,gap=34)
    p.notice(940,435,392,['确认收到3件后，订单完成，','随后执行线上货款结算。'])
    p.button(940,562,392,'确认收到 3 件',h=50)
    p.text(940,659,'当前货款：待买方收货后结算',15,C['muted'])
    p.text(940,707,'收货后按订单原声明申请售后。',14,C['muted'])
    p.button(80,866,340,'收货完成后可申请售后','disabled',44)
    p.save()


def methods():
    p=Page(METHODS,'线下付款与赠送的局部界面')
    p.text(80,89,'线下售卖与免费赠送',30,C['ink'],700)
    p.text(80,130,'沿用订单详情模板，只显示当前身份可执行的操作。',16,C['muted'])
    p.state_card(80,178,620,658,'林同学 · 卖方视角','线下收款待确认',
        ['教材 · 3件 · ¥30.00 · O20261104001','交付方式：双方见面','买方已在16:00确认收货','卖方尚未确认收款，订单仍待交付'])
    p.notice(108,485,564,['仅由该订单卖方确认实际收到货款。','买方收货与卖方收款缺一不可。'])
    p.button(108,625,564,'确认已实际收到 ¥30.00',h=50)
    p.text(108,761,'系统只记录线下确认，不执行线上扣款。',15,C['muted'])
    p.state_card(740,178,620,658,'周同学 · 接收方视角','赠送商品待确认收到',
        ['桌面绿植 · 1件 · ¥0.00','O20261104004 · 发布者：张同学','代交已交件，等待接收方确认','无需付款、无需结算或退款'])
    p.notice(768,485,564,['确认收到后，订单完成。','赠送数量单独统计，不计入售卖金额。'])
    p.button(768,625,564,'确认收到赠送商品 1 件',h=50)
    p.text(768,761,'取件后异常须交管理员处理。',15,C['muted'])
    p.nav(80,914,'返回交付与收货 →',RECEIPT,240);p.save()


def pay_states():
    p=Page(PAY_STATES,'付款超时与结算的局部界面',1120)
    p.text(80,80,'付款与结算反馈',30,C['ink'],700)
    p.text(80,120,'同一订单在不同结果下的分支示例；支付、退款和结算分别记录。',16,C['muted'])
    cards=[(80,158,'未超时','本次模拟付款失败',['金额 ¥30.00 · 截止14:50','未扣款，订单仍为待付款。','保留原截止时间，刷新不重新计时。'],'重新模拟付款',PAY),
           (740,158,'已取消','付款超时自动取消',['14:20进入待付款，14:50仍未付。','订单已取消，占用已释放。','不能继续支付或交付。'],'已超时，不能继续付款',None),
           (80,588,'买方视角 · 迟到付款','订单已取消，退款处理中',['取消后收到¥30.00成功付款结果。','按原支付退款，不恢复订单。','退款失败仍为处理中，转管理员处理。'],'查看退款进度',None),
           (740,588,'卖方视角 · 订单已完成','结算失败，等待处理',['买方已收货，订单保持已完成。','线上结算¥30.00失败，尚未到账。','管理员可重试，不能重复转款。'],'已通知管理员处理',None)]
    for x,y,label,title,lines,button,target in cards:
        p.state_card(x,y,620,396,label,title,lines)
        if target:p.jump(x+24,y+309,572,button,target)
        else:p.button(x+24,y+309,572,button,'secondary' if x==80 else 'disabled',44)
    p.save()


def tasks():
    p=Page(TASKS,'官方代交人的本人任务',actor='赵同学',role='courier')
    p.heading('我的代交任务','只显示分配给本人的任务。','我的代交任务')
    p.card(80,230,1280,620)
    for x,label in [(108,'待取件 1'),(302,'已取件 1'),(496,'已交件 0'),(690,'失败 0')]:p.text(x,279,label,16)
    p.line(108,307,1332,307)
    for n,(kind,name,oid,status,detail) in enumerate([
        ('book','高等数学教材（上册） · 3件','O20261104001','待取件','线上售卖已付款 · 林同学 → 周同学'),
        ('plant','桌面绿植 · 1件','O20261104004','已取件','免费赠送 · 张同学 → 周同学')]):
        y=337+n*218;p.art(108,y,138,126,kind)
        p.text(276,y+28,name,22,C['ink'],600);p.text(276,y+68,detail,16,C['muted'])
        p.text(276,y+106,oid,14,C['muted']);p.pill(1198,y,status,'gray',134)
        if n==0:p.jump(1152,y+76,180,'查看任务',TASK)
        else:p.button(1152,y+76,180,'查看任务','secondary',44)
        p.line(108,y+182,1332,y+182)
    p.text(108,812,'任务交件后，仍须由买方或赠送接收方确认收到。',15,C['muted'])
    p.save()


def task():
    p=Page(TASK,'代交任务详情与取件',1100,actor='赵同学',role='courier')
    p.heading('代交任务 D20261104001','O20261104001 · 已分配给赵同学','我的代交任务')
    p.card(80,230,800,660);p.text(108,276,'待取件',25,C['ink'],700)
    p.art(108,313,136,128);p.text(272,350,'高等数学教材（上册）',23,C['ink'],600)
    p.text(272,392,'数量 3 件 · 线上售卖已付款',17)
    p.line(108,478,852,478)
    for y,label,value in [(526,'发布者','林同学 · 图书馆东门'),(594,'接收方','周同学 · 教学楼南门'),(662,'代交人','赵同学（我）')]:
        p.text(108,y,label,15,C['muted']);p.text(270,y,value,18)
    p.notice(108,734,744,['取件：核对商品、数量和交付方后记录。','交件：先完成取件，不能跳过该步骤。'])
    p.card(912,230,448,660);p.text(940,276,'当前操作',22,C['ink'],600)
    p.lines(940,328,['交付资格：线上付款成功','任务归属：分配给本人','取件记录：尚未记录'],16,gap=42)
    p.button(940,503,392,'确认已取件 3 件',h=50)
    p.button(940,576,392,'确认已交件','disabled',48)
    p.text(940,666,'取件后才能记录交件。',15,C['muted'])
    p.jump(940,730,392,'记录异常与查看改约',DELIVERY_STATES)
    p.nav(80,969,'← 返回本人任务列表',TASKS,230);p.save()


def delivery_states():
    p=Page(DELIVERY_STATES,'无人代交 改约及取件后异常',1180)
    p.text(80,80,'代交异常与共同改约',30,C['ink'],700)
    p.text(80,120,'不同分支的局部界面；双方改约与管理员异常处理分别执行。',16,C['muted'])
    p.state_card(80,158,620,438,'交易双方视角','暂未分配到代交人',
        ['原订单保留，线上售卖已付款。','新方案：见面交付','买方已确认 · 卖方待确认'])
    p.button(108,476,564,'确认新的见面方案',h=46)
    p.text(108,561,'双方确认前，不按单方选择改变交付。',14,C['muted'])
    p.state_card(740,158,620,438,'双方已共同确认','代交失败后改为见面',
        ['原订单与价格保持，订单回到待交付。','旧代交任务已停止，不得继续交件。','按双方确认的新方案交付。'])
    p.jump(768,476,564,'查看交付与收货',RECEIPT)
    p.text(768,561,'页面仅展示改约生效后的结果。',14,C['muted'])
    p.state_card(80,626,620,438,'管理员视角 · 退回已核实','核实后异常取消',
        ['已取件且无法交付，商品已核实退回。','记录核查原因与退回证据。','线上已付款¥30.00，取消后进入退款。'])
    p.button(108,944,564,'确认异常取消并发起原路退款',h=46)
    p.text(108,1029,'退回商品需重新审核，不直接恢复可售。',14,C['muted'])
    p.state_card(740,626,620,438,'代交人视角','损坏或丢失，提交核查',
        ['异常原因：交付途中发现物品损坏。','保留当前状态和证据，通知管理员。','未核实退回时，禁止直接取消或恢复库存。'])
    p.button(768,944,564,'提交异常原因与证据','secondary',46)
    p.text(768,1029,'不自动计算赔偿；赠送取件后同样须核查。',14,C['muted'])
    p.save()


def after_apply():
    p=Page(AFTER_APPLY,'买方申请部分退货',1180)
    p.heading('申请售后','O20261104001 · 原订单已完成 · 支持售后','售后服务')
    p.card(80,230,800,822);p.text(108,274,'退货商品',22,C['ink'],600)
    p.art(108,306,128,120);p.text(264,341,'高等数学教材（上册）',22,C['ink'],600)
    p.text(264,383,'原单价 ¥10.00 · 购买 3 件 · 原金额 ¥30.00',16)
    p.line(108,461,852,461)
    p.text(108,504,'可申请退货 3 件',18,C['ink'],600)
    p.text(108,542,'已成功退货 0 件，其他有效申请占用 0 件。',15,C['muted'])
    p.label_input(108,600,230,'本次退货数量 *','1')
    p.text(404,600,'预计退款',15,C['muted']);p.text(404,654,'¥10.00',30,C['ink'],700)
    p.text(108,719,'申请原因 *',15)
    p.textarea(108,738,744,['收到后发现部分内页破损，希望退回其中1件。'],86)
    p.text(108,870,'图片证据',15);p.art(108,887,126,100,'book_wear')
    p.button(254,887,138,'添加图片','secondary',100)
    p.text(414,939,'请上传与本次问题对应的清晰图片。',14,C['muted'])
    p.card(912,230,448,512);p.text(940,274,'申请条件',21,C['ink'],600)
    p.lines(940,326,['收货：11月4日 16:00','申请截止：11月11日 16:00','连续168小时，恰好到期仍可申请。'],15,gap=38)
    p.line(940,450,1332,450)
    p.lines(940,495,['同意或批准后仍须退货验收。','原订单保持已完成。','退回不自动恢复可售库存。'],15,C['muted'],35)
    p.button(940,651,392,'提交退货申请',h=48)
    p.save()


def after_reply():
    p=Page(AFTER_REPLY,'卖方答复售后与沟通',1180,actor='林同学')
    p.heading('处理售后申请','A20261105001 · 待卖方处理 · 原订单已完成','售后服务')
    p.card(80,230,800,826);p.text(108,275,'买方申请',22,C['ink'],600)
    p.text(108,327,'周同学 · 高等数学教材（上册）',23,C['ink'],600)
    p.text(108,370,'申请退 1 件 · 原单价 ¥10.00 · 预计退款 ¥10.00',17)
    p.text(108,408,'原订单 O20261104001 · 购买3件，共¥30.00',15,C['muted'])
    p.line(108,448,852,448);p.text(108,492,'原因与证据',19,C['ink'],600)
    p.text(108,533,'收到后发现部分内页破损，希望退回其中1件。',16)
    p.art(108,560,144,108,'book_wear')
    p.line(108,708,852,708);p.text(108,753,'双方沟通',19,C['ink'],600)
    p.text(108,794,'周同学  11月5日09:00：已补充问题图片。',15,C['muted'])
    p.textarea(108,824,744,['请填写需要向买方说明的内容'],74)
    p.button(704,918,148,'发送留言','secondary',40)
    p.card(912,230,448,826);p.text(940,275,'答复申请',23,C['ink'],600)
    p.lines(940,330,['提交：11月5日 09:00','答复截止：11月7日 09:00','卖方应在48小时内答复。'],15,gap=38)
    p.notice(940,478,392,['同意后进入待退货，','不直接向买方退款。'])
    p.button(940,607,392,'同意退货',h=48)
    p.text(940,708,'拒绝原因',15)
    p.textarea(940,726,392,['拒绝时必须填写具体原因'],100)
    p.button(940,850,392,'提交拒绝答复','secondary',44)
    p.text(940,967,'拒绝或超时后，由买方申请介入。',14,C['muted'])
    p.save()


def after_funds():
    p=Page(AFTER_FUNDS,'售后退款进度与卖方返款',1100,actor='林同学')
    p.heading('退款处理中','A20261105001 · 原订单仍为已完成 · 本次退货1件','售后服务')
    p.card(80,230,800,644);p.text(108,275,'退货与退款进度',22,C['ink'],600)
    stages=[(108,'待退货'),(296,'待验收'),(484,'退款处理中'),(696,'已退款')]
    for x,label in stages:p.text(x,335,label,17,C['ink'] if label=='退款处理中' else C['muted'],600 if label=='退款处理中' else 400)
    p.line(108,367,852,367)
    for n,(time,event) in enumerate([('11-05 09:00','买方申请退1件，预计退款¥10.00'),('11-05 10:00','卖方同意退货'),('11-05 12:00','买方记录已退回'),('11-05 13:00','卖方验收通过，进入退款处理')]):
        y=419+n*55;p.text(108,y,time,14,C['muted']);p.text(272,y,event,16)
    p.notice(108,690,744,['退货验收已通过，不代表退款已经成功。','退回商品待卖方重新提交审核，不自动恢复可售。'])
    p.card(912,230,448,644);p.text(940,275,'等待卖方返款平台',22,C['ink'],600)
    p.text(940,336,'本次应退金额',15,C['muted']);p.text(940,392,'¥10.00',38,C['ink'],700)
    p.lines(940,448,['原货款已结算给卖方。','返款平台已确认到账：¥0.00','尚待返还：¥10.00'],16,gap=38)
    p.button(940,607,392,'模拟返款平台 ¥10.00',h=48)
    p.lines(940,704,['确认资金到账后再原路退款。','资金未到位，保持退款处理中。','平台不垫付本次退款。'],15,C['muted'],34)
    p.nav(80,954,'查看验收、争议及线下退款 →',AFTER_STATES,350)
    p.save()


def after_states():
    p=Page(AFTER_STATES,'售后资格 介入 验收及线下退款',1220)
    p.text(80,80,'售后处理的关键分支',30,C['ink'],700)
    p.text(80,120,'每个卡片为独立情形，操作始终受当前身份、原声明与处理阶段限制。',16,C['muted'])
    p.state_card(80,160,620,456,'买方视角','当前不能申请普通售后',
        ['订单原声明不支持，或已超过收货后168小时。','赠送商品没有退款申请。','显示具体原因；违规问题仍可举报。'])
    p.jump(108,505,564,'举报商品或订单',REPORT)
    p.state_card(740,160,620,456,'买方视角','卖方拒绝或48小时未答复',
        ['卖方已拒绝，或到11月7日09:00仍未答复。','申请仍保留，超时不自动批准或退款。','由买方主动提交原因和证据申请介入。'])
    p.button(768,505,564,'申请管理员介入','secondary',44)
    p.state_card(80,646,620,456,'卖方视角','商品已退回，等待验收',
        ['本次退回教材1件，预计退款¥10.00。','核对数量和商品状况后记录验收结论。','验收异常可补充证据，交管理员核查。'])
    p.button(108,991,564,'确认验收通过，进入退款处理',h=44)
    p.state_card(740,646,620,456,'线下付款 · 买方视角','等待确认实际收到退款',
        ['验收通过，卖方记录已线下退回¥10.00。','只有原订单买方确认收到后才记为已退款。','线下退款不生成平台原路退款记录。'])
    p.button(768,991,564,'确认实际收到退款 ¥10.00',h=44)
    p.save()


def after_admin():
    p=Page(AFTER_ADMIN,'管理员售后证据核查与结论',1220,actor='许老师',role='admin')
    p.heading('售后介入核查','A20261105001 · 待管理员核查 · 原订单保持已完成','举报与异常')
    p.card(80,230,800,840);p.text(108,275,'申请与原订单',22,C['ink'],600)
    p.text(108,327,'高等数学教材（上册） · O20261104001',22,C['ink'],600)
    p.lines(108,373,['买方周同学／卖方林同学 · 原声明支持售后','原订单3件，共¥30.00 · 本次申请退1件、退款¥10.00','原收货11月4日16:00 · 申请11月5日09:00，在168小时内'],16,gap=36)
    p.line(108,481,852,481)
    p.text(108,527,'买方证据',19,C['ink'],600)
    p.text(108,568,'内页存在破损，申请退回其中1件。',16)
    p.art(108,592,132,100,'book_wear')
    p.text(264,629,'问题图片 · 买方于11月5日09:00提交',15,C['muted'])
    p.text(108,750,'卖方答复与证据',19,C['ink'],600)
    p.lines(108,792,['11月5日10:00拒绝：认为属于正常使用痕迹。','附商品原描述和发布时细节图，待核对破损情况。'],16,gap=32)
    p.line(108,879,852,879)
    p.lines(108,928,['买方11月5日10:30申请介入：不同意拒绝结论，补充问题说明。','核查数量、原声明、双方材料与沟通记录，保留处理依据。'],15,C['muted'],34)
    p.card(912,230,448,840);p.text(940,275,'处理结论',22,C['ink'],600)
    p.text(940,332,'当前为卖方拒绝后的介入分支。',15,C['muted'])
    p.check(952,395,True);p.text(978,401,'同意退货',18)
    p.check(952,451,False);p.text(978,457,'驳回申请',18)
    p.text(940,538,'核查依据与原因 *',15)
    p.textarea(940,556,392,['填写证据核查结果和处理原因'],140)
    p.notice(940,735,392,['同意后进入待退货。','仍须退回并验收通过才处理退款。','驳回保留原因，不改变原订单。'])
    p.button(940,907,392,'保存核查结论并通知双方',h=48)
    p.nav(80,1148,'查看售后其他分支 →',AFTER_STATES,290)
    p.save()


def audit():
    p=Page(AUDIT,'管理员商品审核',1120,actor='许老师',role='admin')
    p.heading('商品审核','审核通过后才向校内用户公开。','商品审核')
    p.card(80,230,388,744);p.text(108,273,'待审核 2',21,C['ink'],600)
    p.rect(96,302,356,160,C['light'],7)
    p.text(116,345,'高等数学教材（上册）',19,C['ink'],600)
    p.text(116,383,'林同学 · 售卖 ¥10.00',15);p.text(116,425,'提交：11月4日 13:00',14,C['muted'])
    p.text(108,516,'桌面绿植',19,C['ink'],600);p.text(108,554,'林同学 · 免费赠送 ¥0.00',15,C['muted'])
    p.text(108,925,'审核结论与原因保留在记录中。',14,C['muted'])
    p.card(500,230,860,744);p.text(528,273,'商品 P20261104001',20,C['ink'],600)
    p.art(528,306,196,150);p.art(742,306,196,150,'book_wear')
    p.text(528,505,'高等数学教材（上册）',25,C['ink'],600)
    p.text(528,546,'二手 · 售卖 ¥10.00 · 数量6件 · 支持售后',17)
    p.lines(528,589,['使用一学期，封面右下角轻微磨损。','内页少量铅笔笔记，无缺页，装订完好。'],16,C['muted'],32)
    p.text(528,690,'审核说明／驳回原因',15)
    p.textarea(528,709,804,['驳回时须填写需要补充或修改的具体问题'],96)
    p.button(528,852,390,'审核通过',h=48);p.button(934,852,398,'驳回并记录原因','secondary',48)
    p.text(528,943,'驳回后回到可编辑草稿，原原因可查。',14,C['muted'])
    p.save()


def report():
    p=Page(REPORT,'用户举报商品或订单',1100)
    p.heading('提交举报','请说明具体问题，平台核查后记录处理结果。')
    p.card(80,230,800,724);p.text(108,275,'举报对象',20,C['ink'],600)
    p.art(108,306,126,116);p.text(260,344,'商品：高等数学教材（上册）',22,C['ink'],600)
    p.text(260,386,'P20261104001 · 发布者：林同学',16,C['muted'])
    p.text(108,478,'问题类型',15);p.input(108,494,744,'商品描述不符                         ▾')
    p.text(108,583,'问题说明 *',15)
    p.textarea(108,601,744,['部分内页破损，与详情说明不符，已附问题照片。'],100)
    p.text(108,748,'证据图片',15);p.art(108,765,126,98,'book_wear')
    p.button(254,765,134,'添加证据','secondary',98)
    p.button(108,890,744,'提交举报',h=44)
    p.card(912,230,448,398);p.text(940,275,'我的举报',21,C['ink'],600)
    p.text(940,331,'商品 P20261104001',17);p.text(940,374,'状态：待平台核查',16)
    p.lines(940,433,['每条举报只针对一个商品或订单。','订单举报从对应订单详情进入。','举报不代替售后申请或直接退款。'],15,C['muted'],34)
    p.nav(940,591,'查看售后申请 →',AFTER_APPLY,230)
    p.save()


def admin_report():
    p=Page(ADMIN_REPORT,'管理员举报核查与违规处置',1180,actor='许老师',role='admin')
    p.heading('举报处理','核对目标与证据，保留处置原因和原交易历史。','举报与异常')
    p.card(80,230,388,782);p.text(108,274,'待核查 1',21,C['ink'],600)
    p.rect(96,307,356,180,C['light'],7)
    p.text(116,351,'Z20261105001',18,C['ink'],600)
    p.lines(116,392,['目标：商品 P20261104001','举报人：周同学','问题：商品描述不符'],15,gap=34)
    p.nav(108,575,'异常资金处理 →',ADMIN_FUNDS,230)
    p.nav(108,634,'账号限制与解除 →',SETTINGS,240)
    p.nav(108,693,'售后介入核查 →',AFTER_ADMIN,230)
    p.card(500,230,860,782);p.text(528,274,'商品描述不符',23,C['ink'],600)
    p.text(528,320,'唯一举报目标：P20261104001',16,C['muted'])
    p.text(528,366,'举报说明',18,C['ink'],600)
    p.text(528,405,'部分内页破损，与详情说明不符。',16);p.art(528,435,144,108,'book_wear')
    p.line(528,579,1332,579);p.label_input(528,619,804,'处理结论','限制该商品接受新预约                     ▾')
    p.text(528,726,'处理原因 *',15)
    p.textarea(528,744,804,['经核查，商品描述与提交证据存在差异，要求整改。'],90)
    p.button(528,869,804,'保存处置结论与原因',h=48)
    p.text(528,972,'已有订单和付款记录保留，异常按实际阶段另行处理。',14,C['muted'])
    p.save()


def admin_funds():
    p=Page(ADMIN_FUNDS,'管理员退款与结算重试',1180,actor='许老师',role='admin')
    p.heading('异常资金处理','先核对业务条件，再重试原记录，防止重复退款或转款。','举报与异常')
    p.card(80,230,620,800);p.pill(108,254,'退款处理中',width=132)
    p.text(108,328,'售后退款 ¥10.00',26,C['ink'],700)
    p.lines(108,378,['A20261105001 · O20261104001','买方周同学／卖方林同学','退货1件 · 原单价¥10.00'],16,gap=36)
    p.line(108,494,672,494)
    for n,text in enumerate(['退货验收：通过','卖方返款平台：已确认到账¥10.00','原路退款：失败，仍在处理中','失败原因：模拟渠道返回处理失败']):p.text(108,539+n*44,text,16)
    p.notice(108,746,564,['沿用原申请与原支付重试。','渠道确认成功后，才显示已退款。'])
    p.button(108,893,564,'重试原路退款 ¥10.00',h=48)
    p.card(740,230,620,800);p.pill(768,254,'结算待处理',width=132)
    p.text(768,328,'货款结算 ¥25.00',26,C['ink'],700)
    p.lines(768,378,['O20261104003 · 暖光阅读台灯1件','买方林同学／卖方许同学','原订单：已完成'],16,gap=36)
    p.line(768,494,1332,494)
    for n,text in enumerate(['线上付款：成功','买方收货：已确认','货款结算：失败，未转交卖方','失败原因：模拟渠道暂不可用']):p.text(768,539+n*44,text,16)
    p.notice(768,746,564,['只重试未成功的结算。','订单不回退，成功后不再重复转款。'])
    p.button(768,893,564,'重试结算 ¥25.00',h=48)
    p.save()


def authority():
    p=Page(AUTHORITY,'代交授权与订单任务分配',1160,actor='许老师',role='admin')
    p.heading('权限与代交分配','普通账号不能自行获得代交或管理权限。','权限与分配')
    p.card(80,230,620,774);p.text(108,274,'人员授权',22,C['ink'],600)
    p.label_input(108,324,564,'账号','赵同学')
    p.text(108,430,'基础身份：买方／卖方',17)
    p.check(120,484,True,False);p.text(148,490,'官方代交权限',18)
    p.text(108,546,'当前已授权，可处理分配给本人的任务。',15,C['muted'])
    p.text(108,609,'变更原因 *',15)
    p.textarea(108,627,564,['按平台安排授权官方代交任务处理'],96)
    p.button(108,771,564,'保存授权变更',h=48)
    p.lines(108,900,['管理员账号通过授权方式配置，','不在普通注册中自选。'],15,C['muted'])
    p.card(740,230,620,774);p.text(768,274,'分配代交任务',22,C['ink'],600)
    p.text(768,335,'O20261104001',18,C['ink'],600)
    p.lines(768,382,['高等数学教材（上册） · 3件','线上售卖已付款 · 平台代交','当前尚未分配代交人'],17,gap=40)
    p.label_input(768,547,564,'代交人','赵同学（已授权，可分配）                ▾')
    p.notice(768,672,564,['仅向已付款售卖或赠送订单分配。','无可用代交人时，不能强行创建取件任务。'])
    p.button(768,816,564,'确认分配任务',h=48)
    p.nav(768,943,'查看无人代交与共同改约 →',DELIVERY_STATES,320)
    p.nav(80,1080,'账号限制、解除及学校邮箱设置 →',SETTINGS,390)
    p.save()


def settings():
    p=Page(SETTINGS,'账号限制与学校邮箱域名配置',1120,actor='许老师',role='admin')
    p.heading('账号与学校邮箱设置','只有管理员可调整限制、解除或配置学校域名。','权限与分配')
    p.card(80,230,760,740);p.text(108,274,'账号限制',22,C['ink'],600)
    p.text(108,329,'张同学 · 当前受限',20,C['ink'],600)
    p.label_input(108,385,704,'限制截止时间','2026-11-08 18:00')
    p.text(108,507,'处置／解除原因 *',15)
    p.textarea(108,525,704,['已核查相关举报，按平台结论调整限制。'],112)
    p.button(108,685,340,'保存限制调整',h=48);p.button(464,685,348,'解除限制','secondary',48)
    p.lines(108,804,['保留操作人、原因和处理时间。','原订单持续保留，不因限制账号被删除。'],16,C['muted'],36)
    p.card(872,230,488,740);p.text(900,274,'学校邮箱域名',22,C['ink'],600)
    p.lines(900,329,['有效学校域名由平台统一配置。','注册时按当前配置核对。'],16,C['muted'],36)
    p.label_input(900,457,432,'学校邮箱域名','输入已确认的学校邮箱域名')
    p.text(900,579,'配置说明',15)
    p.textarea(900,597,432,['填写本次新增或调整的原因'],104)
    p.button(900,749,432,'保存域名配置',h=48)
    p.text(900,873,'不在普通登录页面开放此设置。',14,C['muted'])
    p.save()


def stats():
    p=Page(STATS,'成交 退款 净额与赠送统计',1100,actor='许老师',role='admin')
    p.heading('成交与赠送统计','原成交保留，成功退货退款另列。','统计与日志')
    p.label_input(80,242,344,'完成时间','2026-11-04 至 2026-11-05')
    p.label_input(456,242,280,'卖家','林同学                         ▾')
    p.text(780,286,'范围：管理员可查询全平台',15,C['muted']);p.button(1216,258,144,'查询',h=44)
    values=[('原售卖成交','3 件','¥30.00'),('成功退货退款','1 件','¥10.00'),('净成交','2 件','¥20.00'),('免费赠送','0 件','不计入售卖金额')]
    for n,(label,qty,amount) in enumerate(values):
        x=80+n*326;p.card(x,354,302,200);p.text(x+22,395,label,17,C['ink'],600)
        p.text(x+22,448,qty,32,C['ink'],700);p.text(x+22,509,amount,21 if n<3 else 16,C['muted'])
    p.card(80,590,1280,332);p.text(108,634,'统计口径',21,C['ink'],600)
    p.lines(108,687,['原成交：已完成售卖订单，按原订单数量和单价统计。','成功退货退款：退款确认成功后计入；处理中或失败不扣减。','净成交：原成交减去成功退货退款。赠送数量单列，金额不并入售卖。','普通卖家复用本页，查询范围锁定本人，不能选择其他卖家。'],16,C['muted'],43)
    p.nav(1084,1008,'查看操作日志 →',LOGS,244);p.save()


def logs():
    p=Page(LOGS,'管理员关键操作日志查询',1100,actor='许老师',role='admin')
    p.heading('操作日志','按人员、时间和操作类型组合查询。','统计与日志')
    for x,w,label,value in [(80,224,'操作人','全部人员       ▾'),(336,370,'时间','2026-11-04 至 2026-11-05'),(738,318,'操作类型','审核／预约／资金等     ▾')]:p.label_input(x,242,w,label,value)
    p.button(1196,258,164,'查询',h=44)
    p.card(80,350,1280,608)
    cols=[(108,'时间'),(280,'操作人'),(428,'业务对象'),(666,'操作'),(902,'结果'),(1044,'原因／说明')]
    for x,label in cols:p.text(x,395,label,16,C['ink'],600)
    p.line(108,421,1332,421)
    records=[('11-04 13:10','许老师','商品 P...001','审核','通过','资料核对通过'),
        ('11-04 14:00','周同学','订单 O...001','预约3件','成功','占用3件'),
        ('11-04 14:20','林同学','订单 O...001','确认方案','成功','线上／平台代交'),
        ('11-05 13:00','林同学','售后 A...001','退货验收','通过','退回1件'),
        ('11-05 13:10','系统自动任务','售后 A...001','原路退款','失败','模拟渠道处理失败'),
        ('11-05 13:30','许老师','售后 A...001','重试退款','成功','原记录重试')]
    for n,row in enumerate(records):
        y=470+n*70
        for (x,_),value in zip(cols,row):p.text(x,y,value,14)
        if n<5:p.line(108,y+27,1332,y+27)
    p.lines(108,919,['日志至少保留180天，本期仅查询。普通账号只查看本人的业务记录。'],14,C['muted'])
    p.save()


def common_states():
    p=Page(COMMON_STATES,'验证码 查询 旧页面与权限反馈',1180)
    p.text(80,80,'校验与访问反馈',30,C['ink'],700)
    p.text(80,120,'失败保留已填写内容，提示下一步，不把旧状态操作当作成功。',16,C['muted'])
    cards=[(80,160,'学校邮箱验证','验证码不可用',['错误时提示剩余尝试次数。','过期或累计错误5次后，该码失效。','发送未满60秒时，显示剩余等待时间。'],'返回邮箱验证',LOGIN),
        (740,160,'商品查询','没有找到匹配商品',['可调整关键词、分类或价格条件。','下限60、上限10时提示价格区间无效。','不将无效条件当作有效空结果。'],'重置筛选条件',None),
        (80,640,'预约提交前重新核对','商品价格或状态已变化',['旧单价¥10.00，当前价格¥12.00。','请刷新并重新确认，不能按旧价格成交。','已下架、库存不足时禁止创建预约。'],'刷新商品信息',None),
        (740,640,'账号与资源归属','当前操作无权限',['未验证账号：先完成学校邮箱验证。','代交人只能访问分配给本人的任务。','他人订单、管理入口等拒绝越权访问。'],'返回邮箱验证',LOGIN)]
    for x,y,label,title,lines,button,target in cards:
        p.state_card(x,y,620,426,label,title,lines)
        if target:p.jump(x+24,y+332,572,button,target)
        else:p.button(x+24,y+332,572,button,'secondary',44)
    p.save()


def main():
    login();goods();scheme();pay();receipt();methods();pay_states()
    tasks();task();delivery_states()
    after_apply();after_reply();after_funds();after_states();after_admin()
    audit();report();admin_report();admin_funds();authority();settings();stats();logs();common_states()
    for number,page in enumerate(PAGES,15):page['number']=number
    (OUT/'画板清单.json').write_text(json.dumps(dict(version='0.3',status='补充模块 AI 初稿，待用户审查；报告暂停',pages=PAGES),ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    # Reuse the offline viewer; its routes are demonstrations, not live transactions.
    ui.preview()
    path=ROOT/'UI过程稿'/VERSION/'预览.html'
    html=path.read_text(encoding='utf-8')
    html=html.replace('UI 修订稿预览','UI 补充稿预览').replace('v0.2 · 本轮已确认','v0.3 · 补充初稿待审查')
    html=html.replace(f'修订画板 · {len(PAGES)} 张',f'补充画板 · {len(PAGES)} 张')
    html=html.replace("String(i+1).padStart(2,'0')","String(page.number).padStart(2,'0')")
    html=html.replace('${i+1}. ${page.title}','${page.number}. ${page.title}')
    html=html.replace('${index+1} / ${pages.length}','界面${page.number} · ${index+1} / ${pages.length}')
    html=html.replace('点击画板入口可跳转列表和详情。','部分入口可演示跳转；可用目录查看所有分支。')
    html=html.replace('可点击入口演示工作台、列表与详情的页面关系；接受、付款、同意取消等业务操作仅作展示。无需登录或联网。',
                      '补充模块初稿，待你审查。业务按钮仅作展示；通过目录查看全部页面，无需登录或联网。')
    html=html.replace('回到工作台','查看已确认主流程')
    html=html.replace("$('workspace').addEventListener('click',()=>show(pages.findIndex(p=>p.id==='UI-04_个人工作台')));",
                      "$('workspace').addEventListener('click',()=>{location.href='../修订_v0.2/预览.html';});")
    path.write_text(html,encoding='utf-8',newline='\n')
    print(f'Generated {len(PAGES)} additional artboards and offline preview.')


if __name__=='__main__':main()
