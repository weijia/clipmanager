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
        self.installEventFilter(self)

    def eventFilter(self, object, event):
        if event.type() == QtCore.QEvent.WindowActivate:
            print "widget window has gained focus"
            clipboard = QtGui.QApplication.clipboard()
            print clipboard.text()
        '''
        elif event.type()== QtCore.QEvent.WindowDeactivate:
            print "widget window has lost focus"
        elif event.type()== QtCore.QEvent.FocusIn:
            print "widget has gained keyboard focus"
        elif event.type()== QtCore.QEvent.FocusOut:
            print "widget has lost keyboard focus"
        '''


class ClipboardListUi(ItemToActionDictInListUi):
    def new_ui_item(self, key):
        ui_item = QStandardItem(key)
        ui_item.setCheckable(True)
        self.ui_widget.model.appendRow(ui_item)
        return ui_item

    def __setitem__(self, key, value):
        #item = self.item_dict.get(key, self.new_item(key))

        if key in self.item_dict:
            item = self.key2item[key]
        else:
            item = self.new_ui_item(key)

        if ("checked" in value) and (value["checked"]):
            item.setCheckState(Qt.Checked)
        else:
            item.setCheckState(Qt.Unchecked)
        self.item_to_action_dict[key] = value["action"]
        self.item_dict[key] = value
        self.key2item[key] = item


def main():
    app = QtGui.QApplication(sys.argv)
    clip_list = ClipboardListUi(list_window_class=ClipboardList)
    #clip_list["good"] = {"checked": False, "action": default_action}
    clip_list["good"] = ListItem(True, default_action)
    clip_list.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()