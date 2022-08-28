import json
from PyQt6.QtCore import Qt
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6 import uic

default_reg_path = './data/RegularLibrary.json'


class RegWindow(QWidget):
    """正则管理器窗口"""

    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("resources/ui/openReg.ui")
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
