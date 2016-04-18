#!/usr/bin/python

import socket
from threading import Thread
from geometry_msgs.msg import Twist
import rospy

class Server(object):
    
    # initialize host, port, socket publisher and establish client connection
    def init(self):
        self.host = "127.0.0.1"
        self.port = 9081
        self.sock = socket.socket()
        self.sock.bind((self.host,self.port))
        self.sock.listen(1)
        self.client, self.cl_addr = self.sock.accept()

        self.thread = Thread(target = self.run)

        self.publisher = rospy.Publisher("/turtle1/cmd_vel",Twist,queue_size=10)
        self.twist = Twist()

    # main loop
    # recive data(x-linear and z-angular) speed and publish
    def run(self):
        while not rospy.is_shutdown():
            self.data = self.client.recv(11)
            xz = self.data.split(",")
            x = float(xz[0])
            z = float(xz[1])
            # print("x: " + str(x) + " data: " + str(xz))
            self.twist.linear.x = x
            self.twist.angular.z = z
            self.publisher.publish(self.twist)
            rospy.Rate(10).sleep()
        self.client.close()
        self._Thread__stop()

    # initialize basics and start thread
    def start(self):
        self.init()
        self.thread.start()
if __name__ == "__main__":
    rospy.init_node("ros_blender_server")
    server = Server()
    server.start()