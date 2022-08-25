import pyperclip
from PyQt6.QtCore import Qt
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6 import uic
import json
import sys
import re
import io

default_reg_path = './data/RegularLibrary.json'
custom_reg_path = './data/CustomRegularLibrary.json'
data = []

# 导入数据
from data.gamedata import GameData


class MainWindow(QWidget):
    """主窗口类"""

    def __init__(self):
        super().__init__()
        self.text = io.StringIO()  # 文档内容
        self.text_section = []
        self.text_now = None
        '''当前文本编辑框显示的区块\n
        None为显示全部文本'''
        self.ui = uic.loadUi("resources/main.ui")
        # 自定义变量

        self.reg = ""  # 当前匹配的正则表达式

        # 绑定控件对象
        self.b_open = self.ui.action1  # 菜单_打开按钮
        self.b_open2 = self.ui.pushButton_3
        self.t_plainTextEdit = self.ui.plainTextEdit  # log文本编辑框
        self.tree = self.ui.treeWidget  # 树形框
        self.b_font = self.ui.action2  # 菜单_字体设置按钮
        self.b_regbox = self.ui.action3  # 正则管理器按钮
        self.b_gameData = self.ui.pushButton_5  # 游戏数据按钮
        self.t_reg_group = self.ui.textEdit  # 正则匹配组编辑框
        self.reginfo_type = self.ui.label_7
        self.reginfo_description = self.ui.label_6
        self.reginfo_translation = self.ui.label_5
        self.l_type = self.ui.label  # 日志类型显示label
        self.b_regCopy = self.ui.pushButton_2  # 复制正则表达式按钮

        # 初始化
        self.ui.plainTextEdit.setFont(QFont("宋体", 12, ))  # 字体初始化
        self.t_reg_group.setFont(QFont("宋体", 12, ))
        self.ui.label_8.setFont(QFont("宋体", 11, ))
        self.ui.label_9.setFont(QFont("宋体", 11, ))
        self.ui.label_10.setFont(QFont("宋体", 11, ))
        self.reginfo_type.setFont(QFont("宋体", 11, ))
        self.reginfo_type.setText("")
        self.reginfo_description.setFont(QFont("宋体", 11, ))
        self.reginfo_description.setText("")
        self.reginfo_translation.setFont(QFont("宋体", 11, ))
        self.reginfo_translation.setText("")
        self.ui.label_2.hide()
        self.tree.setColumnHidden(1, True)  # 树形编辑框隐藏列和头
        self.tree.setColumnHidden(2, True)
        self.tree.setColumnHidden(3, True)
        self.tree.setHeaderHidden(True)

        # 信号槽
        self.tree.itemClicked.connect(self.get_tree_clicked)  # 树形编辑器被点击
        self.b_open.triggered.connect(self.openfile)  # 菜单_打开按钮
        self.b_open2.clicked.connect(self.openfile)
        self.b_font.triggered.connect(self.changefont)  # 菜单_字体设置按钮
        self.t_plainTextEdit.cursorPositionChanged.connect(self.reg_def)  # 光标改变时正则匹配行
        self.t_plainTextEdit.cursorPositionChanged.connect(self.line_deep)  # 光标行字体背景颜色加深
        self.b_regCopy.clicked.connect(self.copy_reg)  # 复制正则表达式按钮

    def text_type(self):
        """
            检测导入文本的日志类型\n
            返回 "网络日志" 或 "ACT日志" 或 ""
        """
        line = self.t_plainTextEdit.textCursor().block().text()
        if line.strip() != "":
            if re.search(r"^\d+?\|[^|]*\|", line) is not None:
                log_type = "网络日志"
                self.l_type.setText("当前文本类型为" + log_type)
                return log_type
            if re.search(r"^.{14} .*? (?P<type>\d+):", line) is not None:
                log_type = "ACT日志"
                self.l_type.setText("当前文本类型为" + log_type)
                return log_type
            self.l_type.setText("")
            return ""
        else:
            self.l_type.setText("")
            return ""

    def openfile(self):
        """打开文件"""
        file_names, ok = QFileDialog.getOpenFileName(self, "选择文件", "./", "Log Files (*.log);;Text Files (*.txt)")
        if ok:
            self.t_plainTextEdit.clear()  # 清除所有
            file = open(file_names, encoding="utf-8")
            self.t_plainTextEdit.setPlainText(file.read())
            self.text = io.StringIO(self.t_plainTextEdit.toPlainText())  # 将文本内容赋值到text
            self.text_section = []  # 分段文本初始化
            file.close()
            self.get_tree()

    def changefont(self):
        """字体设置"""
        font = self.t_plainTextEdit.currentCharFormat().font()  # 获取编辑框当前字体
        font, ok = QFontDialog.getFont(font, self, "字体设置")  # 打开字体对话框
        if ok:
            self.t_plainTextEdit.setFont(font)

    def line_deep(self):
        """光标行字体背景颜色加深"""
        selection = QTextEdit.ExtraSelection()
        selection.cursor = self.t_plainTextEdit.textCursor()  # 获取当前光标位置
        selection.format.setBackground(QColor(232, 232, 255))
        selection.format.setProperty(0x06000, True)
        extraSelections = [selection]
        self.t_plainTextEdit.setExtraSelections(extraSelections)

    def copy_reg(self):
        """复制正则表达式到剪切板"""
        if self.reg != "":
            pyperclip.copy(self.reg)

    def reg_def(self):
        """
            光标改变时正则匹配行
        """
        # 获取行以及key
        log_type = self.text_type()  # 该行的日志类型
        cursor = self.t_plainTextEdit.textCursor()  # 获取当前光标位置
        line = cursor.block().text()
        # 获取日志行的前缀
        key = ""
        if log_type == "网络日志":
            key = line[:line.find("|")]
        if log_type == "ACT日志":
            key = re.search(r"^.{14} .*? (?P<type>\d+):", line).groupdict()["type"]
        if log_type == "":
            return  # 如果为空行则不执行
        if key in regular_library.keys():  # 为非空行切能够匹配到key的情况（else为非空行匹配不到key的情况）
            regular = regular_library[key]
            text = line
            # 选择合适的正则表达式
            if log_type == "网络日志":
                self.reg = regular["regular"].replace("(?<", "(?P<")  # 将cactbot正则表达式转化为python re库正则规范
            if log_type == "ACT日志":
                self.reg = regular["0xregular"].replace("(?<", "(?P<")
            """
                self.reg:{
                    "regular" : 正则表达式
                    "0xregular" : act日志正则表达式
                    "text" : 匹配文本
                    "type" : 日志行类型（00、37、36这种前缀）
                    "0xtype" : 十六进制日志行类型
                    "name" : 日志行记录内容的名字，如AddCombatant
                    "description" : 描述
                    "translation" : 把文本行翻译成人话
                }
            """
            match_obj = re.search(self.reg, text)
            if match_obj is not None:  # 匹配不成功不执行
                # 匹配结果储存进字典，key值为组名
                match = match_obj.groupdict()
                # key列表
                match_keys = match.keys()
                # translation模块转化为str
                translation = regular['translation']
                # 如果translation为字符串则转化为列表
                if type(translation) == str:
                    translation = eval(translation)
                a = ['']
                for i in translation:
                    if i != translation[0]:
                        a.append(match[i])
                translation = translation[0].format(a)

                # 更新GUI输出
                self.reginfo_type.setText(regular['type'] + " " + regular['name'] + "  (0x" + regular['0xtype'] + ")")
                self.reginfo_description.setText(regular['description'])
                self.reginfo_translation.setText(translation)
                # 更新正则匹配组显示
                self.t_reg_group.clear()
                for i in match_keys:
                    if type(match[i]) == str:
                        t_head = i
                        t_mid = " " * (11 - len(t_head)) + ": "
                        t_end = match[i]
                        t = t_head + t_mid + t_end
                        self.t_reg_group.append(t)

    # 左侧树形分类框
    def get_tree(self):
        """打开文件时扫描一次，形成树形分类"""
        self.tree.clear()
        log_type = self.text_type()  # 日志类型
        # 扫描
        map = []  # 地图
        circulation = []  # 团灭或胜利
        ability = []  # 技能
        pos = 0  # 定位位置
        text_section_pos = 0
        for line in self.text:
            if log_type == "网络日志":
                # 找到改变地图的日志
                if line[0:2] == "01":
                    reg = regular_library['01']['regular']
                    reg = reg.replace("(?<", "(?P<")
                    map_name = re.search(reg, line).groupdict()["name"]  # 地图名字
                    time = '  -  ' + re.search(reg, line).groupdict()["timestamp"][11:19]
                    map.append(QTreeWidgetItem(self.tree))
                    map[-1].setText(0, map_name + time)
                    map[-1].setText(1, str(self.text.tell()))  # 记录当前文本光标位置
                    map[-1].setText(2, str(pos))  # 记录当前行位置
                    text_section_pos = self.text.tell() - len(line)  # 记录当前分段文本光标位置
                # 找到团灭或胜利的日志
                if line[0:2] == "33":
                    reg = regular_library['33']['regular']
                    reg = reg.replace("(?<", "(?P<")
                    code = re.search(reg, line).groupdict()["command"]
                    time = '  -  ' + re.search(reg, line).groupdict()["timestamp"][11:19]
                    if code == '40000010':
                        circulation.append(QTreeWidgetItem(map[-1]))
                        circulation[-1].setText(0, '团灭' + time)
                        circulation[-1].setText(1, str(self.text.tell()))
                        circulation[-1].setText(2, str(pos))
                        circulation[-1].setText(3, str(len(circulation) - 1))
                        # 读取分段文本
                        local_pos = self.text.tell()
                        if local_pos > text_section_pos:
                            self.text.seek(text_section_pos)
                            iotext = self.text.read(local_pos - text_section_pos)
                            self.text_section.append(iotext)
                            self.text.seek(local_pos)
                            text_section_pos = local_pos

                    if code == '40000003':
                        circulation.append(QTreeWidgetItem(map[-1]))
                        circulation[-1].setText(0, '胜利' + time)
                        circulation[-1].setText(1, str(self.text.tell()))
                        circulation[-1].setText(2, str(pos))
                        circulation[-1].setText(3, str(len(circulation) - 1))
                        # 读取分段文本
                        local_pos = self.text.tell()
                        if local_pos > text_section_pos:
                            self.text.seek(text_section_pos)
                            iotext = self.text.read(local_pos - text_section_pos)
                            self.text_section.append(iotext)
                            self.text.seek(local_pos)
                            text_section_pos = local_pos
            pos += 1

        global data
        data = []  # 初始化

        playerId = ''  # 记录玩家自己
        party = []  # 记录小队列表id
        boss = []  # 记录被攻击过的boss id列表（不可选中的不算）

        # 循环遍历每一个团灭、胜利日志块的每一行
        m = 0
        for text in self.text_section:
            data.append(GameData())

            # 记录所有实体(通过03行)
            t = io.StringIO(text)
            temp = []  # 用于记录已记录的id，防止重复记录
            for line in t:
                if line[0:2] == '03':
                    reg = regular_library['03']['regular']
                    reg = reg.replace("(?<", "(?P<")
                    dic = re.search(reg, line).groupdict()
                    data[-1].combatant = {
                        'id': dic['id'],
                        'name': dic['name'],
                        'worldId': dic['worldId'],
                        'worldName': dic['world'],
                        'jobId': str(int(dic['job'], 16)),
                        'jobName': data[-1].getJob(str(int(dic['job'], 16))),
                        'role': data[-1].getJob(str(int(dic['job'], 16)), 'role'),
                        'MaxHp': dic['hp'],
                        'ownerId': dic['ownerId']
                    }
                    if dic['id'] not in temp:
                        data[-1].entity.append(data[-1].combatant)  # 记录到data数据中
                    temp.append(dic['id'])

            # 玩家自己
            t = io.StringIO(text)
            for line in t:
                if line[0:2] == '02':
                    reg = regular_library['02']['regular']
                    reg = reg.replace("(?<", "(?P<")
                    dic = re.search(reg, line).groupdict()
                    playerId = dic['id']
                    break

            # 记录小队列表
            t = io.StringIO(text)
            for line in t:
                if line[0:2] == '11':
                    party = []
                    reg = regular_library['11']['regular']
                    reg = reg.replace("(?<", "(?P<")
                    party_dict = re.search(reg, line).groupdict()
                    party_num = len(party_dict) - 3
                    for i in range(0, party_num - 1):
                        l = party_dict['id' + str(i)]
                        if l is not None:
                            party.append(l)
                    break  # 退出当前循环
            # 小队、boss记录到data数据中
            for i in data[-1].entity:
                if i['id'] == playerId:
                    data[-1].player = i  # 记录玩家自己
                if i['id'] in party:
                    data[-1].party.append(i)  # 记录小队
                else:
                    if int(i['ownerId'], 16) == 0:
                        data[-1].boss.append(i)  # 记录敌对

            # 记录当前日志块的BOSS
            boss = []  # 清空boss列表
            t = io.StringIO(text)
            for line in t:
                if line[0:2] == '21':
                    reg = regular_library['21']['regular']
                    reg = reg.replace("(?<", "(?P<")
                    _id = re.search(reg, line).groupdict()["id"]
                    if _id == '07':  # 如果21行为攻击
                        dic = re.search(reg, line).groupdict()
                        sourceId = dic["sourceId"]
                        targetId = dic["targetId"]

                        if sourceId in party and targetId not in boss:
                            boss.append(targetId)

            t = io.StringIO(text)
            for line in t:
                # 找到boss放技能的日志
                if line[0:2] == '20':
                    reg = regular_library['20']['regular']
                    reg = reg.replace("(?<", "(?P<")
                    dic = re.search(reg, line).groupdict()
                    _ability = dic["ability"]
                    sourceId = dic["sourceId"]
                    time = '  -  ' + dic["timestamp"][11:19]
                    if sourceId in boss:
                        ability.append(QTreeWidgetItem(circulation[m]))
                        ability[-1].setText(0, _ability + time)
                        ability[-1].setText(1, '技能')
                        ability[-1].setText(2, str(t.tell()))
            m += 1

    # 属性编辑器被点击,快速定位到指定位置
    def get_tree_clicked(self):

        def fold(start, end):
            """折叠显示"""
            start = int(start)
            end = int(end)
            doc = self.t_plainTextEdit.document()
            QTextBlock(doc).setVisible(False)
            '''num = doc.blockCount()  # 文本总行数
            for i in range(0, start):
                doc.findBlockByNumber(i).setVisible(False)
            for i in range(end + 1, num):
                doc.findBlockByNumber(i).setVisible(False)'''
            self.t_plainTextEdit.viewport().update()
            self.t_plainTextEdit.document().adjustSize()

        def move_cursor(new_pos):
            """移动光标到"""
            a = self.t_plainTextEdit.textCursor()
            a.setPosition(int(new_pos))  # 快速定位到指定位置，但是会在下一行
            a.movePosition(QTextCursor.MoveOperation.Up, QTextCursor.MoveMode.MoveAnchor, 1)  # 设置光标到指定行
            a.movePosition(QTextCursor.MoveOperation.StartOfLine, QTextCursor.MoveMode.MoveAnchor)
            self.t_plainTextEdit.setTextCursor(a)

        # 如果点击的是“团灭”“胜利”，显示分段文本
        text = self.tree.currentItem().text(0)[0:2]  # 当前选中的文本
        if text == '团灭' or text == '胜利':
            text_section_pos = int(self.tree.currentItem().text(3))
            self.t_plainTextEdit.clear()
            self.t_plainTextEdit.setPlainText(self.text_section[text_section_pos])
            self.text_now = text_section_pos  # 记录下当前文本显示的区块

        # 如果点的是具体技能，则快速移动到指定位置
        if self.tree.currentItem().text(1) == '技能':
            father = int(self.tree.currentItem().parent().text(3))  # 获取父节点
            # 如果当前选中技能不在文本编辑框的区块中，则切换显示文本
            if father != self.text_now:
                self.t_plainTextEdit.clear()
                self.t_plainTextEdit.setPlainText(self.text_section[father])
                self.text_now = father  # 记录下当前文本显示的区块
            text_section_pos = int(self.tree.currentItem().text(2))
            move_cursor(text_section_pos)  # 移动光标


class RegWindow(QWidget):
    """正则管理器窗口"""

    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("resources/openReg.ui")
        global regular_library
        self.regularLibrary = regular_library
        self.isupdata = False  # 文本框内容是否保存
        # 绑定控件对象
        self.default_list = self.ui.listWidget
        self.default_table = self.ui.tableWidget
        self.default_text = self.ui.textEdit
        self.default_add = self.ui.pushButton
        self.default_minus = self.ui.pushButton_2
        self.default_save = self.ui.pushButton_5

        # 信号槽
        self.default_list.itemClicked.connect(self.click_default_list)  # 默认正则列表被点击后更新属性表格
        self.default_table.itemClicked.connect(self.click_default_table)  # 默认属性表格被点击后显示文本框
        self.default_text.textChanged.connect(self.change_default_text)  # 默认文本框与属性表格同步
        self.default_add.clicked.connect(self.click_default_list_add)
        self.default_minus.clicked.connect(self.click_default_list_minus)
        self.default_save.clicked.connect(self.save_default)

        # 初始化运行
        self.default_table.setEnabled(False)
        self.default_text.setEnabled(False)
        self.update_default_list()

    def update_default_list(self):
        """刷新默认正则列表"""
        for i in self.regularLibrary.keys():
            self.default_list.addItem(i + "  (0x{})".format(self.regularLibrary[i]['0xtype']))
        # 建立表格但是不填充数据
        row = len(self.regularLibrary["00"])  # 行数=字典键数
        self.default_table.setRowCount(row)
        self.default_table.verticalHeader().setVisible(False)
        self.default_table.setColumnWidth(0, 150)
        self.default_table.setColumnWidth(1, 539)

    def click_default_list(self):
        """正则列表被点击"""
        self.default_table.setEnabled(True)
        target = self.default_list.currentItem().text()
        target = target[:target.find(' ')]  # target为选中的key
        self.update_default_table(target)  # 被点击后刷新表格数据
        # 清空文本框
        self.default_text.setEnabled(False)
        self.isupdata = False
        self.default_text.setText("")

    def click_default_list_add(self):
        """增加正则条目"""
        value, ok = QInputDialog.getText(self, "新增正则条目", "请输入正则行类型:", QLineEdit.EchoMode.Normal, "这是默认值")
        if ok:
            key = value
            key_HEX = hex(int(value)).upper()[2:]  # 转换为十六进制
            self.regularLibrary[key] = {}
            self.regularLibrary[key]['regular'] = ''
            self.regularLibrary[key]['0xregular'] = ''
            self.regularLibrary[key]['type'] = key
            self.regularLibrary[key]['0xtype'] = key_HEX
            self.regularLibrary[key]['name'] = ''
            self.regularLibrary[key]['description'] = ''
            self.regularLibrary[key]['translation'] = []
            self.default_list.clear()  # 清空列表
            for i in self.regularLibrary.keys():  # 刷新列表
                self.default_list.addItem(i + "  (0x{})".format(self.regularLibrary[i]['0xtype']))
            self.default_list.setCurrentRow(len(self.regularLibrary.keys()) - 1)  # 选中列表末尾
            self.click_default_list()  # 刷新表格

    def click_default_list_minus(self):
        """减少正则条目"""
        t = self.default_list.currentItem().text()
        key = str(t)[:str(t).find(" ")]
        del self.regularLibrary[key]
        self.default_list.clear()
        for i in self.regularLibrary.keys():
            self.default_list.addItem(i + "  (0x{})".format(self.regularLibrary[i]['0xtype']))
        self.default_list.setCurrentRow(len(self.regularLibrary.keys()) - 1)
        self.click_default_list()

    def update_default_table(self, key):
        """填充属性表格数据,key为日志行前缀"""
        row = 0
        for i in self.regularLibrary[key].keys():
            item = QTableWidgetItem()
            item2 = QTableWidgetItem()
            item.setText(i)
            item.setFlags(Qt.ItemFlag.ItemIsEnabled)  # 设置不可选中
            item2.setText(str(self.regularLibrary[key][i]))
            self.default_table.setItem(row, 0, item)
            self.default_table.setItem(row, 1, item2)
            row += 1

    def click_default_table(self):
        """默认属性表格被点击"""
        col = self.default_table.currentColumn()
        if col == 1:
            self.default_text.setEnabled(True)
            self.isupdata = True
            text = self.default_table.currentItem().text()
            self.default_text.setText(text)  # 输出到文本编辑框
            self.default_text.setFocus()  # 选中表格某一栏后直接聚焦到文本编辑框
            self.default_text.moveCursor(QTextCursor.MoveOperation.End)  # 光标移动到编辑框尾部
        else:
            self.default_text.setEnabled(False)
            self.isupdata = False
            self.default_text.setText("")  # 清空文本框

    def change_default_text(self):
        """默认文本框与表格同步"""
        if self.isupdata:
            text = self.default_text.document().toPlainText()  # 获取文本框文本内容
            select_table_row = self.default_table.currentRow()
            select_table_col = self.default_table.currentColumn()
            item = QTableWidgetItem()
            item.setText(text)
            self.default_table.setItem(select_table_row, select_table_col, item)
            # 随时更新self.regularLibrary
            target = self.default_list.currentItem().text()
            target = target[:target.find(' ')]
            key = self.default_table.item(select_table_row, 0).text()
            value = self.default_table.item(select_table_row, 1).text()
            self.regularLibrary[target][key] = value

    def save_default(self):
        """保存默认正则"""
        text = regToText(self.regularLibrary)
        value, ok = QInputDialog.getMultiLineText(self, "保存默认正则", "请检查正则集", text)
        if ok:
            write_reg(default_reg_path, self.regularLibrary)
            self.default_list.clear()  # 清空列表
            self.default_text.setEnabled(False)
            self.isupdata = False
            self.default_text.clear()
            # 重新更新regularLibrary
            self.regularLibrary = read_reg(default_reg_path)
            self.update_default_list()
            global regular_library
            regular_library = read_reg(default_reg_path)


class GameDataWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("resources/gameData.ui")


def read_reg(path):
    """读取reg的txt文件,返回一个字典"""
    f = open(path, 'r')
    data = json.load(f)
    f.close()
    return data


def write_reg(path, reg_dict):
    """往reg的txt文件里写入一个字典"""
    dict_json = regToText(reg_dict)
    f = open(path, 'w')
    f.write(dict_json)
    f.close()


def regToText(library):
    """把正则字典转换成方便自己看的文本"""
    return json.dumps(library, sort_keys=False, indent=4, ensure_ascii=False, separators=(',', ': '))


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # 第一次读取默认正则和自定义正则
    regular_library = read_reg(default_reg_path)
    # custom_regular_library = read_reg(custom_reg_path)

    mainWindow = MainWindow()  # 主窗口
    regWindow = RegWindow()  # 正则管理器窗口
    gameDataWindow = GameDataWindow()  # 游戏数据窗口
    mainWindow.b_regbox.triggered.connect(regWindow.ui.show)  # 点击正则管理器按钮弹出窗口
    mainWindow.b_gameData.clicked.connect(gameDataWindow.ui.show)  # 点击游戏数据按钮弹出窗口

    mainWindow.ui.show()
    app.exec()
