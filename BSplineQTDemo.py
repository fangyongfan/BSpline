import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QComboBox
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt, QPoint
import BSplineTool
import BSplineTool2

# class DrawingBoard(QWidget):
#     def __init__(self):
#         super().__init__()
#
#         self.myoriginPoints = []  # 存储点坐标的列表
#         self.myctrlPoints=[]
#         self.mycurvePoints=[]
#         self.initUI()
#
#     def initUI(self):
#         self.setWindowTitle('画板')
#         self.setGeometry(100, 100, 800, 600)
#
#         self.button_draw_lines = QPushButton('生成曲线', self)
#         self.button_clear = QPushButton('清空', self)
#
#         self.button_draw_lines.clicked.connect(self.drawLines)
#         self.button_clear.clicked.connect(self.clearBoard)
#
#         self.layout = QVBoxLayout()
#         self.layout.addWidget(self.button_draw_lines)
#         self.layout.addWidget(self.button_clear)
#         self.layout.addStretch(1)
#         self.setLayout(self.layout)
#
#     def paintEvent(self, event):
#
#         painter = QPainter(self)
#         pen = QPen()
#
#
#         #画插值点
#         pen.setColor(Qt.green)
#         pen.setWidth(5)  # 设置点的宽度
#         painter.setPen(pen)
#         for point in self.mycurvePoints:
#             painter.drawPoint(QPoint(*point))
#         pen.setWidth(1)
#         pen.setStyle(Qt.SolidLine)
#         painter.setPen(pen)
#         for i in range(len(self.mycurvePoints) - 1):
#             painter.drawLine(QPoint(*self.mycurvePoints[i]), QPoint(*self.mycurvePoints[i + 1]))
#         #画控制点
#         pen.setColor(Qt.red)
#         pen.setWidth(2)  # 设置点的宽度
#         painter.setPen(pen)
#         for point in self.myctrlPoints:
#             painter.drawPoint(QPoint(*point))
#             painter.drawEllipse(QPoint(*point), 5, 5)
#         pen.setWidth(2)
#         pen.setDashPattern([2, 2])
#         painter.setPen(pen)
#         for i in range(len(self.myctrlPoints) - 1):
#             painter.drawLine(QPoint(*self.myctrlPoints[i]), QPoint(*self.myctrlPoints[i + 1]))
#         #画型值点（最后再画，不然被插值点挡住）
#         pen.setColor(Qt.blue)
#         pen.setWidth(10)  # 设置点的宽度
#         painter.setPen(pen)
#         for point in self.myoriginPoints:
#             painter.drawPoint(point)
#         # pen.setWidth(1)
#         # painter.setPen(pen)
#         # for i in range(len(self.myoriginPoints) - 1):
#         #     painter.drawLine(self.myoriginPoints[i], self.myoriginPoints[i + 1])
#
#
#
#     def mousePressEvent(self, event):
#         if event.button() == Qt.LeftButton:
#             self.myoriginPoints.append(event.pos())
#             self.update()
#
#     def drawLines(self):
#         if len(self.myoriginPoints) >= 3:
#             origin_points_list = [(point.x(), point.y()) for point in self.myoriginPoints]
#             self.myctrlPoints, self.mycurvePoints = BSplineTool2.generateCurvePoints(origin_points_list)
#             self.update()
#         else:
#             print("请至少在窗口上绘制3个型值点")
#
#     def clearBoard(self):
#         self.myoriginPoints = []
#         self.myctrlPoints = []
#         self.mycurvePoints = []
#         self.update()
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     board = DrawingBoard()
#     board.show()
#     sys.exit(app.exec_())



class DrawingBoard(QWidget):
    def __init__(self):
        super().__init__()

        self.myoriginPoints = []  # 存储点坐标的列表
        self.myctrlPoints = []
        self.mycurvePoints = []
        self.initUI()

    def initUI(self):
        self.setWindowTitle('画板')
        self.setGeometry(100, 100, 800, 600)

        self.button_draw_lines = QPushButton('生成曲线', self)
        self.button_clear = QPushButton('清空', self)

        self.combo_curve_type = QComboBox(self)
        self.combo_curve_type.addItems(['开曲线', '闭曲线'])

        self.button_draw_lines.clicked.connect(self.drawLines)
        self.button_clear.clicked.connect(self.clearBoard)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.combo_curve_type)
        self.layout.addWidget(self.button_draw_lines)
        self.layout.addWidget(self.button_clear)
        self.layout.addStretch(1)
        self.setLayout(self.layout)

    def paintEvent(self, event):

        painter = QPainter(self)
        pen = QPen()


        #画插值点
        pen.setColor(Qt.green)
        pen.setWidth(5)  # 设置点的宽度
        painter.setPen(pen)
        for point in self.mycurvePoints:
            painter.drawPoint(QPoint(*point))
        pen.setWidth(1)
        pen.setStyle(Qt.SolidLine)
        painter.setPen(pen)
        for i in range(len(self.mycurvePoints) - 1):
            painter.drawLine(QPoint(*self.mycurvePoints[i]), QPoint(*self.mycurvePoints[i + 1]))
        #画控制点
        pen.setColor(Qt.red)
        pen.setWidth(2)  # 设置点的宽度
        painter.setPen(pen)
        for point in self.myctrlPoints:
            painter.drawPoint(QPoint(*point))
            painter.drawEllipse(QPoint(*point), 5, 5)
        pen.setWidth(2)
        pen.setDashPattern([2, 2])
        painter.setPen(pen)
        for i in range(len(self.myctrlPoints) - 1):
            painter.drawLine(QPoint(*self.myctrlPoints[i]), QPoint(*self.myctrlPoints[i + 1]))
        #画型值点（最后再画，不然被插值点挡住）
        pen.setColor(Qt.blue)
        pen.setWidth(10)  # 设置点的宽度
        painter.setPen(pen)
        for point in self.myoriginPoints:
            painter.drawPoint(point)
        # pen.setWidth(1)
        # painter.setPen(pen)
        # for i in range(len(self.myoriginPoints) - 1):
        #     painter.drawLine(self.myoriginPoints[i], self.myoriginPoints[i + 1])

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.myoriginPoints.append(event.pos())
            self.update()

    def drawLines(self):
        if len(self.myoriginPoints) >= 3:
            origin_points_list = [(point.x(), point.y()) for point in self.myoriginPoints]

            curve_type = self.combo_curve_type.currentText()
            if curve_type == '开曲线':
                self.myctrlPoints, self.mycurvePoints = BSplineTool.generateCurvePoints(origin_points_list)
            else:
                self.myctrlPoints, self.mycurvePoints = BSplineTool2.generateCurvePoints(origin_points_list)

            self.update()
        else:
            print("请至少在窗口上绘制3个型值点")

    def clearBoard(self):
        self.myoriginPoints = []
        self.myctrlPoints = []
        self.mycurvePoints = []
        self.update()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    board = DrawingBoard()
    board.show()
    sys.exit(app.exec_())



