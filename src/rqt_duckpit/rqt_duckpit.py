import os
import rospy
import rospkg
import cv_bridge
import sensor_msgs.msg
import duckietown_msgs.msg

from qt_gui.plugin import Plugin
from python_qt_binding import loadUi
from python_qt_binding.QtWidgets import QWidget, QLabel, QSlider

class RQTDuckpit(Plugin):

    def __init__(self, context):
        super(RQTDuckpit, self).__init__(context)
        # Give QObjects reasonable names
        self.setObjectName('Duckpit')

        # Process standalone plugin command-line arguments
        from argparse import ArgumentParser
        parser = ArgumentParser()
        # Add argument(s) to the parser.
        parser.add_argument("-q", "--quiet", action="store_true",
                      dest="quiet",
                      help="Put plugin in silent mode")
        args, unknowns = parser.parse_known_args(context.argv())
        if not args.quiet:
            print 'arguments: ', args
            print 'unknowns: ', unknowns

        # Create QWidget
        self._widget = QWidget()
        # Get path to UI file which should be in the "resource" folder of this package
        ui_file = os.path.join(rospkg.RosPack().get_path('rqt_duckpit'), 'resource', 'rqt_duckpit.ui')
        # Extend the widget with all attributes and children from UI file
        loadUi(ui_file, self._widget)
        # Give QObjects reasonable names
        self._widget.setObjectName('rqt_duckpit')
        # Show _widget.windowTitle on left-top of each plugin (when
        # it's set in _widget). This is useful when you open multiple
        # plugins at once. Also if you open multiple instances of your
        # plugin at once, these lines add number to make it easy to
        # tell from pane to pane.
        if context.serial_number() > 1:
            self._widget.setWindowTitle(self._widget.windowTitle() + (' (%d)' % context.serial_number()))
        # Add widget to the user interface
        context.add_widget(self._widget)

        self.veh = rospy.get_param('/veh',"megabot08")

        # Subscribers
        # self.camera_topic = '/' + self.veh + '/camera_node/image/compressed'
        # self.sub_camera = rospy.Subscriber(self.camera_topic, sensor_msgs.msg.CompressedImage, self.cbImage, queue_size=1)

        self.steps_ahead = 5
        self.cmd_topics = []
        self.cmd_topics.append('/' + self.veh + '/inverse_kinematics_node/car_cmd')
        self.cmd_node_name = 'cnn_node'
        for i in range(1,self.steps_ahead):
             self.cmd_topics.append('/' + self.veh + '/'+ self.cmd_node_name +'/car_cmd_'+str(i+1))

        self.sub_cmds = dict()
        for i in range(0, self.steps_ahead):
            self.sub_cmds[i] = rospy.Subscriber(self.cmd_topics[i], duckietown_msgs.msg.Twist2DStamped, self.cbCarCmds, callback_args=i+1)

        self._widget.h_slider.setValue(0)
        self._widget.h_slider_2.setValue(0)
        self._widget.h_slider_3.setValue(0)
        self._widget.h_slider_4.setValue(0)
        self._widget.h_slider_5.setValue(0)

        self._widget.label_val.setText("0")
        self._widget.label_val_2.setText("0")
        self._widget.label_val_3.setText("0")
        self._widget.label_val_4.setText("0")
        self._widget.label_val_5.setText("0")


        

    def cbCarCmds(self, msg,num):
        if num == 1:
            self._widget.h_slider.setValue(msg.omega)
            self._widget.label_val.setText(str(msg.omega))
        elif num == 2:
            self._widget.h_slider_2.setValue(msg.omega)
            self._widget.label_val_2.setText(str(msg.omega))
        elif num == 3:
            self._widget.h_slider_3.setValue(msg.omega)
            self._widget.label_val_3.setText(str(msg.omega))
        elif num == 4:
            self._widget.h_slider_4.setValue(msg.omega)
            self._widget.label_val_4.setText(str(msg.omega))
        elif num == 5:
            self._widget.h_slider_5.setValue(msg.omega)
            self._widget.label_val_5.setText(str(msg.omega))

    def shutdown_plugin(self):
        # TODO unregister all publishers here
        pass

    def save_settings(self, plugin_settings, instance_settings):
        # TODO save intrinsic configuration, usually using:
        # instance_settings.set_value(k, v)
        pass

    def restore_settings(self, plugin_settings, instance_settings):
        # TODO restore intrinsic configuration, usually using:
        # v = instance_settings.value(k)
        pass

    #def trigger_configuration(self):
        # Comment in to signal that the plugin has a way to configure
        # This will enable a setting button (gear icon) in each dock widget title bar
        # Usually used to open a modal configuration dialog