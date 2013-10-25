#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt4 import QtGui
import sys
from iconizer.qtconsole.list_window import ItemToActionDictInListUi, ListItem


class ClipboardListUi(ItemToActionDictInListUi):
    def new_item(self, key):
        pass


def default_action(item):
    print "click action"
    QtGui.QApplication.quit()


def main():
    app = QtGui.QApplication(sys.argv)
    clip_list = ItemToActionDictInListUi()
    #clip_list["good"] = {"checked": False, "action": default_action}
    clip_list["good"] = ListItem(True, default_action)
    clip_list.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()