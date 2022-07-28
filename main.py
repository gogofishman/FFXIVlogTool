import pyperclip
from PyQt6.QtCore import Qt
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6 import uic
import sys
import re

default_reg_path = './data/RegularLibrary.txt'
custom_reg_path = './data/CustomRegularLibrary.txt'


class MainWindow(QWidget):
    """主窗口类"""

    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("resources/main.ui")
        # 自定义变量
        self.text = ""  # 文档内容
        self.reg = ""  # 当前匹配的正则表达式

        # 绑定控件对象
        self.b_open = self.ui.action1  # 菜单_打开按钮
        self.t_plainTextEdit = self.ui.plainTextEdit  # log文本编辑框
        self.b_font = self.ui.action2  # 菜单_字体设置按钮
        self.b_regbox = self.ui.action3  # 正则管理器按钮
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

        # 信号槽
        self.b_open.triggered.connect(self.openfile)  # 菜单_打开按钮
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
            self.text = file.read()  # text储存文本信息
            self.t_plainTextEdit.setPlainText(self.text)
            file.close()

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


class RegWindow(QWidget):
    """正则管理器窗口"""

    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("resources/openReg.ui")
        self.isupdata = False  # 文本框内容是否保存
        # 绑定控件对象
        self.default_list = self.ui.listWidget
        self.default_table = self.ui.tableWidget
        self.default_text = self.ui.textEdit

        # 信号槽
        self.default_list.itemClicked.connect(self.click_default_list)  # 默认正则列表被点击后更新属性表格
        self.default_table.itemClicked.connect(self.click_default_table)  # 默认属性表格被点击后显示文本框
        self.default_text.textChanged.connect(self.change_default_text)  # 默认文本框与属性表格同步

        # 初始化运行
        self.default_table.setEnabled(False)
        self.default_text.setEnabled(False)
        self.update_default_list()

    def update_default_list(self):
        """刷新默认正则列表"""
        for i in regular_library.keys():
            self.default_list.addItem(i + "  (0x{})".format(regular_library[i]['0xtype']))
        # 建立表格但是不填充数据
        row = len(regular_library["00"])  # 行数=字典键数
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

    def update_default_table(self, key):
        """填充属性表格数据,key为日志行前缀"""
        row = 0
        for i in regular_library[key].keys():
            item = QTableWidgetItem()
            item2 = QTableWidgetItem()
            item.setText(i)
            item.setFlags(Qt.ItemFlag.ItemIsEnabled)  # 设置不可选中
            item2.setText(str(regular_library[key][i]))
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
            # 随时更新regular_library
            target = self.default_list.currentItem().text()
            target = target[:target.find(' ')]
            key = self.default_table.item(select_table_row, 0).text()
            value = self.default_table.item(select_table_row, 1).text()
            regular_library[target][key] = value


def read_reg(path):
    """读取reg的txt文件,返回一个字典"""
    f = open(path, 'r')
    data = f.read()
    if data != "":
        data2 = eval(data)
    else:
        data2 = {}
    f.close()
    return data2


def write_reg(path, reg_dict):
    """往reg的txt文件里写入一个字典"""
    f = open(path, 'w')
    f.write(str(reg_dict))
    f.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # 第一次读取默认正则和自定义正则
    regular_library = read_reg(default_reg_path)
    custom_regular_library = read_reg(custom_reg_path)

    mainWindow = MainWindow()  # 主窗口
    regWindow = RegWindow()  # 正则管理器窗口
    mainWindow.b_regbox.triggered.connect(regWindow.ui.show)  # 点击正则管理器按钮弹出窗口

    mainWindow.ui.show()
    app.exec()
