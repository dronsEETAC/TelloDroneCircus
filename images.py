import base64
import ssl
from tkinter import *
import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk
from tkinter import messagebox
from djitellopy import Tello
import time
import cv2
import os
import paho.mqtt.client as mqtt
import threading
from Gallery import GalleryMedia

class escenarioImagenes:

    def Open(self, master, selectedBroker):
        self.drone = Tello()
        #self.galleryImages = galleryImages()
        self.galleryImages = GalleryMedia()
        print ('selected broker', selectedBroker)

        myFont3 = font.Font(family='Arial', size=10, weight='bold')

        self.windowImage = Toplevel(master)

        # Variables
        self.takePictureBool = False
        self.take_off = False
        self.connected = False
        self.detectingBool = False
        self.photo = None
        self.vect_images = []
        self.count = 0

        # MQTT conexión
        '''print("aaaa")
        self.global_broker_address = "broker.hivemq.com"
        self.global_broker_port = 8000  # 8883

        self.client = mqtt.Client("VideoService", transport="websockets")
        # self.client.username_pw_set("dronsEETAC", "mimara1456.")
        self.client.connect(self.global_broker_address, self.global_broker_port)
        self.client.loop_start()'''

        # Configuration
        self.windowImage.geometry("550x500")
        self.windowImage.rowconfigure(0, weight=1)
        self.windowImage.rowconfigure(1, weight=1)
        self.windowImage.rowconfigure(2, weight=1)


        self.windowImage.columnconfigure(0, weight=1)
        self.windowImage.columnconfigure(1, weight=1)


        self.windowImage.title("Foto Page")



        # Title label
        self.titlelabel = tk.Label(self.windowImage, text="TAKE YOUR PICTURE!", height=3)
        self.titlelabel.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky=N + S + E + W)
        self.titlelabel['font'] = myFont3

        self.picturesFrame = tk.LabelFrame(self.windowImage, text='Pictures')
        self.picturesFrame.grid(row=1, column=0, padx=5, pady=5, sticky=N + S + E + W)

        self.picturesFrame.rowconfigure(0, weight=1)
        self.picturesFrame.rowconfigure(1, weight=1)

        self.picturesFrame.columnconfigure(0, weight=1)
        self.picturesFrame.columnconfigure(1, weight=1)
        self.picturesFrame.columnconfigure(2, weight=1)

        self.canvas = Canvas(self.picturesFrame, width=320, height=240, bg='white')
        self.canvas.grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky=N + S + E + W)

        # Take picture button
        self.takePictureButton = Button(self.picturesFrame, text="Take Picture", height=1, bg='#0000FF',
                                        fg='#F8F8FF', command=self.takePicture)
        self.takePictureButton.grid(row=1, column=0, padx=5, pady=5, sticky=N + S + E + W)
        self.takePictureButton['font'] = myFont3

        # Send picture button
        self.sendButton = Button(self.picturesFrame, text="Send Picture", height=1, bg='#0000FF',
                                 fg='#F8F8FF', command=self.sendSave)
        self.sendButton.grid(row=1, column=1, padx=5, pady=5, sticky=N + S + E + W)
        self.sendButton['font'] = myFont3

        # Gallery button
        self.galleryButton = Button(self.picturesFrame, text="Image gallery", height=1, bg='#458B74',
                                    fg='#F8F8FF', command=self.gallery)
        self.galleryButton.grid(row=1, column=2, padx=5, pady=5, sticky=N + S + E + W)
        self.galleryButton['font'] = myFont3

        # Canvas




        self.commandsFrame = tk.LabelFrame (self.windowImage, text = 'Drone commands')
        self.commandsFrame.grid(row=1, column=1, padx=5, pady=5, sticky=N + S + E + W)

        self.commandsFrame.rowconfigure(0, weight=1)
        self.commandsFrame.rowconfigure(1, weight=1)
        self.commandsFrame.rowconfigure(2, weight=1)
        self.commandsFrame.rowconfigure(3, weight=1)
        self.commandsFrame.rowconfigure(4, weight=1)
        self.commandsFrame.rowconfigure(5, weight=1)
        self.commandsFrame.rowconfigure(5, weight=1)

        self.commandsFrame.columnconfigure(0, weight=1)
        self.commandsFrame.columnconfigure(1, weight=1)







        # Connect button
        self.connectButton = Button(self.commandsFrame, text="Connect", bg='#367E18',
                            fg='#F8F8FF', command=self.connect)
        self.connectButton.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky=N + S + E + W)
        self.connectButton['font'] = myFont3

        # TakeOff button
        self.takeoffDButton = Button(self.commandsFrame, text="Take Off", bg='#FF6103',
                                     fg='#F8F8FF', command=self.takeoff)
        self.takeoffDButton.grid(row=1, column=0, padx=5, pady=5, sticky=N + S + E + W)
        self.takeoffDButton['font'] = myFont3

        # Land button
        self.landDButton = Button(self.commandsFrame, text="Landing", bg='#FF6103',
                                     fg='#F8F8FF', command=self.land)
        self.landDButton.grid(row=1, column=1, padx=5, pady=5, sticky=N + S + E + W)
        self.landDButton['font'] = myFont3

        # Up button
        self.upButton = Button(self.commandsFrame, text="  Up  ", bg='#FF6103',
                               fg='#F8F8FF', command=self.up)
        self.upButton.grid(row=2, column=0, padx=5, pady=5, sticky=N + S + E + W)
        self.upButton['font'] = myFont3

        # Down button
        self.downButton = Button(self.commandsFrame, text="Down", bg='#FF6103',
                                 fg='#F8F8FF', command=self.down)
        self.downButton.grid(row=2, column=1, padx=5, pady=5, sticky=N + S + E + W)
        self.downButton['font'] = myFont3

        # Forward button
        self.forwardButton = Button(self.commandsFrame, text="Forward ",  bg='#FF8C00',
                                  fg='#F8F8FF', command=self.forward)
        self.forwardButton.grid(row=3, column=0, padx=5, pady=5, sticky=N + S + E + W)
        self.forwardButton['font'] = myFont3

        # Backward button
        self.backwardButton = Button(self.commandsFrame, text="Backward", bg='#FF8C00',
                                  fg='#F8F8FF', command=self.backward)
        self.backwardButton.grid(row=3, column=1, padx=5, pady=5, sticky=N + S + E + W)
        self.backwardButton['font'] = myFont3

        # Left button
        self.leftButton = Button(self.commandsFrame, text="  Left  ", bg='#FF8C00',
                                 fg='#F8F8FF', command=self.left)
        self.leftButton.grid(row=4, column=0, padx=5, pady=5, sticky=N + S + E + W)
        self.leftButton['font'] = myFont3

        # Right button
        self.rightButton = Button(self.commandsFrame, text=" Right ", bg='#FF8C00',
                                  fg='#F8F8FF', command=self.right)
        self.rightButton.grid(row=4, column=1, padx=5, pady=5, sticky=N + S + E + W)
        self.rightButton['font'] = myFont3


        # Rolate CW
        self.rotateCWButton = Button(self.commandsFrame, text="  Rotate CW  ", bg='#FF8C00',
                                  fg='#F8F8FF', command=self.rotateCW)
        self.rotateCWButton.grid(row=5, column=0, padx=5, pady=5, sticky=N + S + E + W)
        self.rotateCWButton['font'] = myFont3

        # Rotate CCW
        self.rotateCCWButton = Button(self.commandsFrame, text=" Rotate CCW ", bg='#FF8C00',
                                  fg='#F8F8FF', command=self.rotateCCW)
        self.rotateCCWButton.grid(row=5, column=1, padx=5, pady=5, sticky=N + S + E + W)
        self.rotateCCWButton['font'] = myFont3

        self.flipButton = Button(self.commandsFrame, text=" Flip ", bg='#FF8C00',
                                      fg='#F8F8FF', command=self.flip)
        self.flipButton.grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky=N + S + E + W)
        self.flipButton['font'] = myFont3

        self.closeButton = Button(self.windowImage, text="Close", bg='#367E18',
                                     fg='#F8F8FF', command=self.closeImg)
        self.closeButton.grid(row=2, column=0, columnspan = 2, padx=5, pady=5, sticky=N + S + E + W)
        self.closeButton['font'] = myFont3

        self.client = mqtt.Client("VideoService", transport="websockets")
        self.client.tls_set(
            ca_certs=None,
            certfile=None,
            keyfile=None,
            cert_reqs=ssl.CERT_REQUIRED,
            tls_version=ssl.PROTOCOL_TLS,
            ciphers=None,
        )

        if selectedBroker == 0:
            self.client.username_pw_set(
                "dronsEETAC", "mimara1456."
            )
            self.client.connect("dronseetac.upc.edu", 8883)
        else:
            print ('hivemq')
            self.client.connect("broker.hivemq.com", 8884)

        self.client.max_queued_messages_set(1)
        self.client.max_inflight_messages_set(1)
        self.client.subscribe('videoFrameAnna')
        print('Waiting connection')
        self.client.loop_start()

    def connect(self):
        try:
            self.connected = True
            # muestro el nivel de bateria
            self.connectButton['text'] = str(self.drone.get_battery())
            self.connectButton['bg'] = '#8B0000'
            print("Te has conectado correctamente al dron!")

            if not self.detectingBool:
                self.detectingBool = True
                x = threading.Thread(target=self.detecting)
                x.start()
            print("Se estan transmitiendo las imágenes de la cámara del dron")

        except Exception as e:
            messagebox.showerror("Error de conexión", "No se pudo conectar al dron. Por favor, inténtalo de nuevo.\nError: " + str(e), parent=self.windowImage)

    def takeoff(self):
        if self.connected:
            self.drone.takeoff()
            time.sleep(2)
            self.take_off = True
            self.takeoffDButton['text'] = 'flying'
            self.takeoffDButton['bg'] = '#8B0000'
            self.state = 'flying'
        else:
            messagebox.showwarning("Error", "Antes de despegar debes conectarte al dron", parent=self.windowImage)

    def land(self):
        self.drone.land()
        messagebox.showwarning("Success", "Ya estamos en casa", parent=self.windowImage)

    def forward(self):
        if self.take_off and self.connected:
            self.drone.go_xyz_speed(50, 0, 0, 100)
            time.sleep(1)
        else:
            messagebox.showwarning("Error", "Primero despega el dron", parent=self.windowImage)

    def backward(self):
        if self.take_off and self.connected:
            self.drone.go_xyz_speed(-50, 0, 0, 100)
            time.sleep(1)
        else:
            messagebox.showwarning("Error", "Primero despega el dron", parent=self.windowImage)

    def left(self):
        if self.take_off and self.connected:
            self.drone.go_xyz_speed(0, -50, 0, 100)
            time.sleep(1)
        else:
            messagebox.showwarning("Error", "Primero despega el dron", parent=self.windowImage)

    def right(self):
        if self.take_off and self.connected:
            self.drone.go_xyz_speed(0, 50, 0, 100)
            time.sleep(1)
        else:
            messagebox.showwarning("Error", "Primero despega el dron", parent=self.windowImage)

    def up(self):
        if self.take_off and self.connected:
            self.drone.go_xyz_speed(0, 0, 50, 100)
            time.sleep(1)
        else:
            messagebox.showwarning("Error", "Primero despega el dron", parent=self.windowImage)

    def down(self):
        if self.take_off and self.connected:
            self.drone.go_xyz_speed(0, 0, -50, 100)
            time.sleep(1)
        else:
            messagebox.showwarning("Error", "Primero despega el dron", parent=self.windowImage)

    def rotateCW(self):
        if self.take_off and self.connected:
            self.drone.rotate_clockwise(90)
            time.sleep(1)
        else:
            messagebox.showwarning("Error", "Primero despega el dron", parent=self.windowImage)

    def rotateCCW(self):
        if self.take_off and self.connected:
            self.drone.rotate_counter_clockwise(90)
            time.sleep(1)
        else:
            messagebox.showwarning("Error", "Primero despega el dron", parent=self.windowImage)

    def flip(self):
        if self.take_off and self.connected:
            self.drone.send_control_command("flip l")
            time.sleep(1)
        else:
            messagebox.showwarning("Error", "Primero despega el dron", parent=self.windowImage)
    def takePicture(self):
        if self.connected:
            self.count = self.count + 1
            self.frame = self.drone.get_frame_read().frame
            self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
            self.imgPicture = Image.fromarray(self.frame)
            self.imgPicture = self.imgPicture.resize((320, 240))

            self.photo = ImageTk.PhotoImage(self.imgPicture)
            self.canvas.delete("all")  # Borramos cualquier contenido previo en el canvas
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
            self.canvas.image = self.photo
            self.takePictureBool = True
            print("Foto tomada")
        else:
            messagebox.showwarning("Error", "Primero conéctate con el dron!", parent=self.windowImage)

    def sendSave(self):
        try:
            if self.photo and self.takePictureBool:
                self.vect_images.append(self.photo)
                frame_brg = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                cv2.imwrite("assets/telloImages/foto_tello" + str(self.count) + ".jpg", frame_brg)

                self.sendmqtt()

                print("Foto enviada y guardada")
                return self.photo
            else:
                print("No hay foto para enviar")
                return None
        except Exception as e:
            messagebox.showerror("Error de conexión",
                                 "No se pudo conectar al dron. Por favor, inténtalo de nuevo.\nError: " + str(e),
                                 parent=self.windowImage)

    def sendmqtt(self):
        image_path = "assets/telloImages/foto_tello" + str(self.count) + ".jpg"
        with open(image_path, "rb") as image_file:
            image_data = image_file.read()
            image_base64 = base64.b64encode(image_data)
            self.client.publish("ImagenAnna", payload=image_base64, qos=2)

    def gallery(self):
        type = 'Image'
        self.galleryImages.Open(self.windowImage,type, self.client)

    def closeImg(self):
        if self.connected:
            self.drone.streamoff()
            self.detectingBool = False
            cv2.destroyAllWindows()
        self.windowImage.destroy()


        '''if len(self.vect_images) == 0:
            messagebox.showwarning("Error", "No has guardado ninguna imagen!", parent=self.windowImage)
        else:
            print("Has guardado " + str(len(self.vect_images)) + "imagenes: " + str(self.vect_images))
            self.drone.streamoff()
            self.detectingBool = False
            self.windowImage.destroy()
            cv2.destroyAllWindows()'''

    def detecting(self):
        self.drone.streamon()
        cv2.namedWindow("Tello Camera", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Tello Camera", 640, 480)

        while self.detectingBool and self.connected:
            frame = self.drone.get_frame_read().frame  # Captura un frame desde la cámara del Tello
            #frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            cv2.imshow("Tello Camera", frame)  # Muestra el frame en una ventana
            cv2.waitKey(1)

