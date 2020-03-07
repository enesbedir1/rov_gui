from PyQt5 import QtCore, QtGui, QtWidgets
from master.arducam.arducam import Video
from master.server.server import Server,packing,packing_joy
from master.joystick.joystick import Joy
from threading import Thread
import cv2
import time

class Ui_photomastic(object):
    def setupUi(self, photomastic):
        photomastic.setObjectName("photomastic")
        photomastic.resize(800, 600)
        self.verticalLayout = QtWidgets.QVBoxLayout(photomastic)
        self.verticalLayout.setObjectName("verticalLayout")
        self.photomastic_lb = QtWidgets.QLabel(photomastic)
        self.photomastic_lb.setText("")
        self.photomastic_lb.setObjectName("photomastic_lb")
        self.verticalLayout.addWidget(self.photomastic_lb)

        self.retranslateUi(photomastic)
        QtCore.QMetaObject.connectSlotsByName(photomastic)

    def retranslateUi(self, photomastic):
        _translate = QtCore.QCoreApplication.translate
        photomastic.setWindowTitle(_translate("photomastic", "photomastic"))

class Ui_mapping(object):
    def setupUi(self, mapping):
        mapping.setObjectName("mapping")
        mapping.resize(800, 600)
        self.verticalLayout = QtWidgets.QVBoxLayout(mapping)
        self.verticalLayout.setObjectName("verticalLayout")
        self.mapping_lb = QtWidgets.QLabel(mapping)
        self.mapping_lb.setText("")
        self.mapping_lb.setObjectName("mapping_lb")
        self.verticalLayout.addWidget(self.mapping_lb)
        self.retranslateUi(mapping)
        QtCore.QMetaObject.connectSlotsByName(mapping)
    def retranslateUi(self, mapping):
        _translate = QtCore.QCoreApplication.translate
        mapping.setWindowTitle(_translate("mapping", "mapping"))

class CameraShowThread(QtCore.QThread):
    changePixmap = QtCore.pyqtSignal(QtGui.QImage)

    def run(self):

        video1 = Video(port=2000, selection=0)
        video2 = Video(port=5800, selection=1)
        video3 = Video(port=5000, selection=2)

        frame = []
        ctr = 0
        while True:

            if ui.camera_var == 0:

                time.sleep(0.5)
                continue

            if ui.camera_var == 1:
                if not video1.frame_available():
                    continue
                frame = video1.frame()
            elif ui.camera_var == 2:
                if not video2.frame_available():
                    continue
                frame = video2.frame()
            elif ui.camera_var == 3:
                if not video3.frame_available():
                    continue
                frame = video3.frame()
            if frame == []:
                continue
            rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            rgbImage = cv2.resize(rgbImage, (1280, 720), interpolation=cv2.INTER_LINEAR)
            self.frame_qt = QtGui.QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0], rgbImage.shape[1]*rgbImage.shape[2],QtGui.QImage.Format_RGB888)
            self.changePixmap.emit(self.frame_qt)

class MainThread(QtCore.QThread):
    def run(self):

        # TCP
        self.s = Server(port=5555)
        self.s.setupConnection()
        ui.rovKeys = []

        while True:
            # print(self.s.connection)
            if self.s.new_conn:
                ui.rovKeys = []
                self.s.new_conn = False



            # if not self.gripper_cb.isChecked():
            #     ui.joy.pressed_buttons = []

            # Status Check Start ----------------------------------------------
            if ui.rovKeys:
                key = ui.rovKeys.pop(0)
                self.s.datasend(packing(key))


            if ui.joy.pressed_buttons:
                button = ui.joy.pressed_buttons.pop(0)
                self.s.datasend(packing_joy(button))

class MikroThread(QtCore.QThread):
    def run(self):

        # TCP
        print("check 1")
        self.s = Server(port=5567)
        print("check 2")
        self.s.setupConnection()
        print("check 3")
        ui.microKeys = []

        while True:

            if self.s.new_conn:
                ui.microKeys = []
                self.s.new_conn = False

            # Status Check Start ----------------------------------------------
            if ui.microKeys:
                key = ui.microKeys.pop(0)
                self.s.datasend(packing(key))

            if ui.joy.pressed_buttons:
                button = ui.joy.pressed_buttons.pop(0)
                self.s.datasend(packing_joy(button))


class Ui_rov_gui(object):
    def setupUi(self, rov_gui):
        rov_gui.setObjectName("rov_gui")
        rov_gui.setWindowModality(QtCore.Qt.WindowModal)
        rov_gui.resize(1280, 920)
        self.main_gl = QtWidgets.QWidget(rov_gui)
        self.main_gl.setObjectName("main_gl")
        self.gridLayout = QtWidgets.QGridLayout(self.main_gl)
        self.gridLayout.setObjectName("gridLayout")
        self.rightside_gl = QtWidgets.QGridLayout()
        self.rightside_gl.setObjectName("rightside_gl")
        self.main_tw = QtWidgets.QTabWidget(self.main_gl)
        self.main_tw.setObjectName("main_tw")
        self.TASKS = QtWidgets.QWidget()
        self.TASKS.setObjectName("TASKS")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.TASKS)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.autonomous_gb = QtWidgets.QGroupBox(self.TASKS)
        self.autonomous_gb.setObjectName("autonomous_gb")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.autonomous_gb)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.stop_autonomous_pb = QtWidgets.QPushButton(self.autonomous_gb)
        self.stop_autonomous_pb.setObjectName("stop_autonomous_pb")
        self.gridLayout_3.addWidget(self.stop_autonomous_pb, 2, 1, 1, 1)
        self.mapping_cb = QtWidgets.QCheckBox(self.autonomous_gb)
        self.mapping_cb.setObjectName("mapping_cb")
        self.gridLayout_3.addWidget(self.mapping_cb, 2, 2, 1, 1)
        self.fly_auto_hl = QtWidgets.QHBoxLayout()
        self.fly_auto_hl.setObjectName("fly_auto_hl")
        self.fly_pb = QtWidgets.QPushButton(self.autonomous_gb)
        self.fly_pb.setObjectName("fly_pb")
        self.fly_auto_hl.addWidget(self.fly_pb)
        self.fly2_pb = QtWidgets.QPushButton(self.autonomous_gb)
        self.fly2_pb.setObjectName("fly2_pb")
        self.fly_auto_hl.addWidget(self.fly2_pb)
        self.fly3_pb = QtWidgets.QPushButton(self.autonomous_gb)
        self.fly3_pb.setObjectName("fly3_pb")
        self.fly_auto_hl.addWidget(self.fly3_pb)
        self.gridLayout_3.addLayout(self.fly_auto_hl, 1, 1, 1, 2)
        self.test_autonomous_pb = QtWidgets.QPushButton(self.autonomous_gb)
        self.test_autonomous_pb.setObjectName("test_autonomous_pb")
        self.gridLayout_3.addWidget(self.test_autonomous_pb, 0, 1, 1, 2)
        self.verticalLayout_2.addWidget(self.autonomous_gb)
        self.mapping_gb = QtWidgets.QGroupBox(self.TASKS)
        self.mapping_gb.setObjectName("mapping_gb")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.mapping_gb)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.stop_mapping_pb = QtWidgets.QPushButton(self.mapping_gb)
        self.stop_mapping_pb.setObjectName("stop_mapping_pb")
        self.gridLayout_4.addWidget(self.stop_mapping_pb, 3, 0, 1, 1)
        self.createmap_pb = QtWidgets.QPushButton(self.mapping_gb)
        self.createmap_pb.setObjectName("createmap_pb")
        self.gridLayout_4.addWidget(self.createmap_pb, 3, 1, 1, 1)
        self.start_mapping_pb = QtWidgets.QPushButton(self.mapping_gb)
        self.start_mapping_pb.setObjectName("start_mapping_pb")
        self.gridLayout_4.addWidget(self.start_mapping_pb, 2, 0, 1, 1)
        self.start2_mapping_pb = QtWidgets.QPushButton(self.mapping_gb)
        self.start2_mapping_pb.setObjectName("start2_mapping_pb")
        self.gridLayout_4.addWidget(self.start2_mapping_pb, 2, 1, 1, 1)
        self.test_mapping_pb = QtWidgets.QPushButton(self.mapping_gb)
        self.test_mapping_pb.setObjectName("test_mapping_pb")
        self.gridLayout_4.addWidget(self.test_mapping_pb, 1, 0, 1, 2)
        self.verticalLayout_2.addWidget(self.mapping_gb)
        self.subwaycar_gb = QtWidgets.QGroupBox(self.TASKS)
        self.subwaycar_gb.setObjectName("subwaycar_gb")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.subwaycar_gb)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.tpicos_pb = QtWidgets.QPushButton(self.subwaycar_gb)
        self.tpicos_pb.setObjectName("tpicos_pb")
        self.gridLayout_6.addWidget(self.tpicos_pb, 1, 0, 1, 2)
        self.createphotom_pb = QtWidgets.QPushButton(self.subwaycar_gb)
        self.createphotom_pb.setObjectName("createphotom_pb")
        self.gridLayout_6.addWidget(self.createphotom_pb, 3, 0, 1, 1)
        self.start_photomastic_pb_2 = QtWidgets.QPushButton(self.subwaycar_gb)
        self.start_photomastic_pb_2.setObjectName("start_photomastic_pb_2")
        self.gridLayout_6.addWidget(self.start_photomastic_pb_2, 0, 1, 1, 1)
        self.start_photomastic_pb = QtWidgets.QPushButton(self.subwaycar_gb)
        self.start_photomastic_pb.setObjectName("start_photomastic_pb")
        self.gridLayout_6.addWidget(self.start_photomastic_pb, 0, 0, 1, 1)
        self.stop_photomastic_pb = QtWidgets.QPushButton(self.subwaycar_gb)
        self.stop_photomastic_pb.setObjectName("stop_photomastic_pb")
        self.gridLayout_6.addWidget(self.stop_photomastic_pb, 3, 1, 1, 1)
        self.verticalLayout_2.addWidget(self.subwaycar_gb)
        self.keyboard_gb = QtWidgets.QGroupBox(self.TASKS)
        self.keyboard_gb.setObjectName("keyboard_gb")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.keyboard_gb)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gripper_cb = QtWidgets.QCheckBox(self.keyboard_gb)
        self.gripper_cb.setObjectName("gripper_cb")
        self.horizontalLayout.addWidget(self.gripper_cb)
        self.microrov_cb = QtWidgets.QCheckBox(self.keyboard_gb)
        self.microrov_cb.setObjectName("microrov_cb")
        self.horizontalLayout.addWidget(self.microrov_cb)
        self.cable_cb = QtWidgets.QCheckBox(self.keyboard_gb)
        self.cable_cb.setObjectName("cable_cb")
        self.horizontalLayout.addWidget(self.cable_cb)
        self.verticalLayout_2.addWidget(self.keyboard_gb)
        self.camera_gl = QtWidgets.QGridLayout()
        self.camera_gl.setObjectName("camera_gl")
        self.bottomcam_pb = QtWidgets.QPushButton(self.TASKS)
        self.bottomcam_pb.setObjectName("bottomcam_pb")
        self.camera_gl.addWidget(self.bottomcam_pb, 2, 2, 1, 1)
        self.closecam_pb = QtWidgets.QPushButton(self.TASKS)
        self.closecam_pb.setObjectName("closecam_pb")
        self.camera_gl.addWidget(self.closecam_pb, 3, 1, 1, 1)
        self.mivrorovcam_pb = QtWidgets.QPushButton(self.TASKS)
        self.mivrorovcam_pb.setObjectName("mivrorovcam_pb")
        self.camera_gl.addWidget(self.mivrorovcam_pb, 3, 2, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.camera_gl.addItem(spacerItem, 0, 0, 4, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.camera_gl.addItem(spacerItem1, 0, 3, 4, 1)
        self.frontcam_pb = QtWidgets.QPushButton(self.TASKS)
        self.frontcam_pb.setObjectName("frontcam_pb")
        self.camera_gl.addWidget(self.frontcam_pb, 2, 1, 1, 1)
        self.takephoto_pb = QtWidgets.QPushButton(self.TASKS)
        self.takephoto_pb.setObjectName("takephoto_pb")
        self.camera_gl.addWidget(self.takephoto_pb, 1, 1, 1, 2)
        self.verticalLayout_2.addLayout(self.camera_gl)
        self.main_tw.addTab(self.TASKS, "")
        self.INFO = QtWidgets.QWidget()
        self.INFO.setObjectName("INFO")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.INFO)
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.info_label = QtWidgets.QLabel(self.INFO)
        self.info_label.setText("")
        self.info_label.setObjectName("info_label")
        self.gridLayout_5.addWidget(self.info_label, 0, 0, 1, 1)
        self.main_tw.addTab(self.INFO, "")
        self.rightside_gl.addWidget(self.main_tw, 0, 0, 1, 1)
        self.counterstart_pb = QtWidgets.QPushButton(self.main_gl)
        self.counterstart_pb.setObjectName("counterstart_pb")
        self.rightside_gl.addWidget(self.counterstart_pb, 2, 0, 1, 1)
        self.counter_lcd = QtWidgets.QLCDNumber(self.main_gl)
        self.counter_lcd.setObjectName("counter_lcd")
        self.rightside_gl.addWidget(self.counter_lcd, 1, 0, 1, 1)
        self.ROV_LOGO_lb = QtWidgets.QLabel(self.main_gl)
        self.ROV_LOGO_lb.setObjectName("ROV_LOGO_lb")
        self.rightside_gl.addWidget(self.ROV_LOGO_lb, 3, 0, 1, 1)
        self.status_gl = QtWidgets.QGridLayout()
        self.status_gl.setObjectName("status_gl")
        self.microrov_st_lb = QtWidgets.QLabel(self.main_gl)
        self.microrov_st_lb.setObjectName("microrov_st_lb")
        self.status_gl.addWidget(self.microrov_st_lb, 2, 2, 1, 1)
        self.microrov_lb = QtWidgets.QLabel(self.main_gl)
        self.microrov_lb.setObjectName("microrov_lb")
        self.status_gl.addWidget(self.microrov_lb, 2, 0, 1, 1)
        self.vehicle_lb = QtWidgets.QLabel(self.main_gl)
        self.vehicle_lb.setObjectName("vehicle_lb")
        self.status_gl.addWidget(self.vehicle_lb, 0, 0, 1, 1)
        self.vehicle_st_lb = QtWidgets.QLabel(self.main_gl)
        self.vehicle_st_lb.setObjectName("vehicle_st_lb")
        self.status_gl.addWidget(self.vehicle_st_lb, 0, 2, 1, 1)
        self.h1_hl = QtWidgets.QFrame(self.main_gl)
        self.h1_hl.setFrameShape(QtWidgets.QFrame.HLine)
        self.h1_hl.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.h1_hl.setObjectName("h1_hl")
        self.status_gl.addWidget(self.h1_hl, 1, 0, 1, 3)
        self.vehicle_vl = QtWidgets.QFrame(self.main_gl)
        self.vehicle_vl.setFrameShape(QtWidgets.QFrame.VLine)
        self.vehicle_vl.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.vehicle_vl.setObjectName("vehicle_vl")
        self.status_gl.addWidget(self.vehicle_vl, 0, 1, 1, 1)
        self.microrov_vl = QtWidgets.QFrame(self.main_gl)
        self.microrov_vl.setFrameShape(QtWidgets.QFrame.VLine)
        self.microrov_vl.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.microrov_vl.setObjectName("microrov_vl")
        self.status_gl.addWidget(self.microrov_vl, 2, 1, 1, 1)
        self.rightside_gl.addLayout(self.status_gl, 4, 0, 1, 1)
        self.rightside_gl.setRowStretch(3, 70)
        self.gridLayout.addLayout(self.rightside_gl, 0, 1, 1, 1)
        self.leftside_gl = QtWidgets.QGridLayout()
        self.leftside_gl.setObjectName("leftside_gl")
        self.camera_gb = QtWidgets.QGroupBox(self.main_gl)
        self.camera_gb.setObjectName("camera_gb")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.camera_gb)
        self.verticalLayout.setObjectName("verticalLayout")
        self.cam_label = QtWidgets.QLabel(self.camera_gb)
        self.cam_label.setText("")
        self.cam_label.setObjectName("cam_label")
        self.cam_label.resize(1280,720)
        self.verticalLayout.addWidget(self.cam_label)
        self.verticalLayout.setStretch(0, 90)
        self.leftside_gl.addWidget(self.camera_gb, 0, 0, 1, 1)
        self.warnings_vl = QtWidgets.QVBoxLayout()
        self.warnings_vl.setObjectName("warnings_vl")
        self.warnings_lb = QtWidgets.QLabel(self.main_gl)
        self.warnings_lb.setObjectName("warnings_lb")
        self.warnings_vl.addWidget(self.warnings_lb)
        self.warnings_st_lb = QtWidgets.QLabel(self.main_gl)
        self.warnings_st_lb.setText("")
        self.warnings_st_lb.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.warnings_st_lb.setObjectName("warnings_st_lb")
        self.warnings_vl.addWidget(self.warnings_st_lb)
        self.warnings_vl.setStretch(0, 20)
        self.warnings_vl.setStretch(1, 80)
        self.leftside_gl.addLayout(self.warnings_vl, 1, 0, 1, 1)
        self.leftside_gl.setRowStretch(0, 80)
        self.leftside_gl.setRowStretch(1, 20)
        self.gridLayout.addLayout(self.leftside_gl, 0, 0, 1, 1)
        self.gridLayout.setColumnStretch(0, 80)
        rov_gui.setCentralWidget(self.main_gl)
        self.retranslateUi(rov_gui)
        self.main_tw.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(rov_gui)
        # AEB

        self.microrov_key = [ord("W"), ord("A"), ord("S"), ord("D"), ord("Q"), ord("E")]
        self.masterRov_key = [ord("J"), ord("K")]
        self.microKeys = list()
        self.rovKeys = list()

        self.joy = Joy()
        joy_timer = Thread(target=self.joy.joy_get)
        joy_timer.start()

        self.message = ""
        self.warnings_list = []
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(lambda: self.timer_func())
        self.timer.start(100)
        self.camera_var = 0

        self.th = CameraShowThread(rov_gui)
        self.th.changePixmap.connect(self.setImage)
        self.th.start()

        self.mainThread = MainThread(rov_gui)
        self.mainThread.start()


        self.mikroThread = MikroThread(rov_gui)
        self.mikroThread.start()

        rov_gui.keyReleaseEvent = self.releasedkey

        self.counterstart_pb.clicked.connect(self.f_counterstart_pb)
        self.bottomcam_pb.clicked.connect(self.f_bottomcam_pb)
        self.frontcam_pb.clicked.connect(self.f_frontcam_pb)
        self.closecam_pb.clicked.connect(self.f_closecam_pb)
        self.takephoto_pb.clicked.connect(self.f_takephoto_pb)
        self.mivrorovcam_pb.clicked.connect(self.f_microrovcam_pb)
        self.fly_pb.clicked.connect(self.f_fly_pb)
        self.fly2_pb.clicked.connect(self.f_fly2_pb)
        self.fly3_pb.clicked.connect(self.f_fly3_pb)
        self.test_autonomous_pb.clicked.connect(self.f_test_autonomous_pb)
        self.stop_autonomous_pb.clicked.connect(self.f_stop_autonomous_pb)
        self.createmap_pb.clicked.connect(self.f_createmap_pb)
        self.start_mapping_pb.clicked.connect(self.f_start_mapping_pb)
        self.start2_mapping_pb.clicked.connect(self.f_start2_mapping_pb)
        self.test_mapping_pb.clicked.connect(self.f_test_mapping_pb)
        self.stop_mapping_pb.clicked.connect(self.f_stop_mapping_pb)
        self.createphotom_pb.clicked.connect(self.f_createphotom_pb)
        self.start_photomastic_pb.clicked.connect(self.f_start_photomastic_pb)
        self.start_photomastic_pb_2.clicked.connect(self.f_start_photomastic_pb_2)
        self.tpicos_pb.clicked.connect(self.f_tpicos_pb)
        self.stop_photomastic_pb.clicked.connect(self.f_stop_photomastic_pb)

    # Definitions of buttons functions
    def setImage(self, image):
        self.cam_label.setPixmap(QtGui.QPixmap.fromImage(image))

    def f_counterstart_pb(self):
        pass

    def f_frontcam_pb(self):
        self.camera_var = 1

    def f_bottomcam_pb(self):
        self.camera_var = 2

    def f_microrovcam_pb(self):
        self.camera_var = 3

    def f_takephoto_pb(self):
        pass

    def f_closecam_pb(self):
        self.camera_var = 0

    def f_fly_pb(self):
        pass
    def f_fly2_pb(self):
        pass
    def f_fly3_pb(self):
        pass
    def f_test_autonomous_pb(self):
        pass
    def f_stop_autonomous_pb(self):
        pass
    def f_test_mapping_pb(self):
        pass
    def f_start_mapping_pb(self):
        pass
    def f_start2_mapping_pb(self):
        pass

    def f_createmap_pb(self):
        self.mapping = QtWidgets.QWidget()
        ui = Ui_mapping()
        ui.setupUi(self.mapping)
        self.mapping.show()

    def f_stop_mapping_pb(self):
        pass
    def f_start_photomastic_pb(self):
        pass
    def f_start_photomastic_pb_2(self):
        pass
    def f_tpicos_pb(self):
        pass

    def f_createphotom_pb(self):
        self.photomastic = QtWidgets.QWidget()
        ui = Ui_photomastic()
        ui.setupUi(self.photomastic)
        self.photomastic.show()
    def f_stop_photomastic_pb(self):
        pass

    def timer_func(self):
        if self.mainThread.s.connection == True:
            self.vehicle_st_lb.setText("Connected")
        else:
            self.vehicle_st_lb.setText("-")

        if self.mikroThread.s.connection == True:
            self.microrov_st_lb.setText("Connected")
        else:
            self.microrov_st_lb.setText("-")

        if not self.warnings_list:
            return
        if len(self.warnings_list) > 8:
            self.warnings_list = self.warnings_list[len(self.warnings_list)-8:len(self.warnings_list)]
        self.message = ""
        for i in self.warnings_list[::-1]:
            self.message = "\n       " + str(i) + self.message
        self.warnings_lb.setText(self.message)

    def releasedkey(self, e):
        key = e.key()
        # print(self.microrov_cb)
        if self.microrov_cb.isChecked() and key in self.microrov_key:
            if len(self.microKeys) > 10:
                self.microKeys = self.microKeys[0:10]
            self.microKeys.append(key)
        elif self.cable_cb.isChecked() and key in self.masterRov_key:
            if len(self.rovKeys) > 10:
                self.rovKeys = self.rovKeys[0:10]
            self.rovKeys.append(key)

    def retranslateUi(self, rov_gui):
        _translate = QtCore.QCoreApplication.translate
        rov_gui.setWindowTitle(_translate("rov_gui", "ITUROV GUI 2020"))
        self.autonomous_gb.setTitle(_translate("rov_gui", "autonomous"))
        self.stop_autonomous_pb.setText(_translate("rov_gui", "stop"))
        self.mapping_cb.setText(_translate("rov_gui", "mapping"))
        self.fly_pb.setText(_translate("rov_gui", "start"))
        self.fly2_pb.setText(_translate("rov_gui", "start 2"))
        self.fly3_pb.setText(_translate("rov_gui", "start 3"))
        self.test_autonomous_pb.setText(_translate("rov_gui", "test"))
        self.mapping_gb.setTitle(_translate("rov_gui", "mapping"))
        self.stop_mapping_pb.setText(_translate("rov_gui", "stop"))
        self.createmap_pb.setText(_translate("rov_gui", "create map"))
        self.start_mapping_pb.setText(_translate("rov_gui", "start "))
        self.start2_mapping_pb.setText(_translate("rov_gui", "start 2"))
        self.test_mapping_pb.setText(_translate("rov_gui", "test"))
        self.subwaycar_gb.setTitle(_translate("rov_gui", "subway car"))
        self.tpicos_pb.setText(_translate("rov_gui", "take pic of surface"))
        self.createphotom_pb.setText(_translate("rov_gui", "create photomastic"))
        self.start_photomastic_pb_2.setText(_translate("rov_gui", "start 2 "))
        self.start_photomastic_pb.setText(_translate("rov_gui", "start"))
        self.stop_photomastic_pb.setText(_translate("rov_gui", "stop"))
        self.keyboard_gb.setTitle(_translate("rov_gui", "keyboard shortcuts"))
        self.gripper_cb.setText(_translate("rov_gui", "gripper"))
        self.microrov_cb.setText(_translate("rov_gui", "microrov"))
        self.cable_cb.setText(_translate("rov_gui", "cable"))
        self.bottomcam_pb.setText(_translate("rov_gui", "bottom camera"))
        self.closecam_pb.setText(_translate("rov_gui", "close camera"))
        self.mivrorovcam_pb.setText(_translate("rov_gui", "microROV camera"))
        self.frontcam_pb.setText(_translate("rov_gui", "front camera"))
        self.takephoto_pb.setText(_translate("rov_gui", "take photo"))
        self.main_tw.setTabText(self.main_tw.indexOf(self.TASKS), _translate("rov_gui", "TASKS"))
        self.main_tw.setTabText(self.main_tw.indexOf(self.INFO), _translate("rov_gui", "INFO"))
        self.counterstart_pb.setText(_translate("rov_gui", "start"))
        self.ROV_LOGO_lb.setText(_translate("rov_gui", "ROV_LOGO"))
        self.microrov_st_lb.setText(_translate("rov_gui", "-"))
        self.microrov_lb.setText(_translate("rov_gui", "microrov:"))
        self.vehicle_lb.setText(_translate("rov_gui", "vehicle:"))
        self.vehicle_st_lb.setText(_translate("rov_gui", "-"))
        self.camera_gb.setTitle(_translate("rov_gui", "camera"))
        self.warnings_lb.setText(_translate("rov_gui", "WARNINGS"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    rov_gui = QtWidgets.QMainWindow()
    ui = Ui_rov_gui()
    ui.setupUi(rov_gui)
    rov_gui.show()
    sys.exit(app.exec_())

