#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt
import sys
from PyQt4.QtGui import QStandardItem
from iconizer.qtconsole.list_window import ItemToActionDictInListUi, ListViewWindow


def default_action(item):
    print "click action"
    QtGui.QApplication.quit()


class ListItem(object):
    def __init__(self, value, action):
        self.value = value
        self.action = action

    def __getitem__(self, item):
        if item == "checked":
            return self.value
        if item == "action":
            return self.action

    def __contains__(self, item):
        if item in ["checked", "action"]:
            return True
        else:
            return False


class ClipboardList(ListViewWindow):
    def __init__(self):
        super(ClipboardList, self).__init__()
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)


class ClipboardListUi(ItemToActionDictInListUi):
    def new_ui_item(self, key):
        ui_item = QStandardItem(key)
        #ui_item.setCheckable(True)
        self.ui_widget.model.appendRow(ui_item)
        return ui_item

    def __setitem__(self, key, value):
        #item = self.item_dict.get(key, self.new_item(key))

        if key in self.item_dict:
            item = self.key2item[key]
        else:
            item = self.new_ui_item(key)

        self.item_to_action_dict[key] = value["action"]
        self.item_dict[key] = value
        self.key2item[key] = item

    def do_nothing(self, text):
        pass

    def process_clipboard(self):
        clipboard = QtGui.QApplication.clipboard()
        #print clipboard.text()
        data = clipboard.mimeData()
        for form in data.formats():
            print form, '------------------', data.data(form)
            content = str(data.data(form)).decode(errors='replace')
            self.__setitem__(u"%s --> %s" % (form, content), {"action": self.do_nothing})
            #self.__setitem__(content, {"action": self.do_nothing})
            #self.__setitem__(form, {"action": self.do_nothing})


def main():
    app = QtGui.QApplication(sys.argv)
    clip_list = ClipboardListUi(list_window_class=ClipboardList)
    clipboard = QtGui.QApplication.clipboard()
    clipboard.dataChanged.connect(clip_list.process_clipboard)
    #clip_list["good"] = {"checked": False, "action": default_action}
    #clip_list["good"] = ListItem(True, default_action)
    clip_list.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()