import numpy as np

class ColorTraker:
    def intializeTracker(self,myDrone):
        myDrone.for_back_velocity = 0
        myDrone.left_right_velocity = 0
        myDrone.up_down_velocity = 0
        myDrone.yaw_velocity = 0
        myDrone.speed = 0
        myDrone.streamon()
        return myDrone

    def trackColor(self,myDrone, info, w, h, pid, pLRError, pUDError, pFBError, mode):
        # si ha detectado color
        if info[0][0] != 0:

            # error de posicion en horizontal
            errorLR = info[0][0] - w // 2
            # ajusto la velocidad horizontal
            # solo uso el termino proporcional y el derivativo
            speedLR = int(pid[0] * errorLR + pid[1] * (errorLR - pLRError))
            # limito el valor obtenido al rango válido para la velocidad
            speedLR = int(np.clip(speedLR, -100, 100))

            # repido el proceso para el error vertical
            errorUD = info[0][1] - h // 2
            speedUD = int(pid[0] * errorUD + pid[1] * (errorUD - pUDError))
            speedUD = int(np.clip(speedUD, -100, 100))

            # y para el error cerca/lejos, que se calcula en función del area de la mancha de color
            errorFB = (info[1] - 30000) // 100
            speedFB = int(pid[0] * errorFB + pid[1] * (errorFB - pFBError))
            speedFB = int(np.clip(speedFB, -100, 100))

            # los siguientes ajustes en las velocidades obtenidas me dan resultados razonables
            print(-speedLR // 6, -speedUD // 4, speedFB // 5)
            if mode == 'front':
                myDrone.left_right_velocity = -speedLR // 6
                myDrone.up_down_velocity = -speedUD // 4
                myDrone.for_back_velocity = -speedFB // 5
            else:
                myDrone.left_right_velocity = -speedLR // 6
                # myDrone.up_down_velocity = -speedFB // 4
                myDrone.up_down_velocity = 0
                myDrone.for_back_velocity = speedUD // 5

        else:
            myDrone.left_right_velocity = 0
            myDrone.for_back_velocity = 0
            myDrone.up_down_velocity = 0
            myDrone.yaw_velocity = 0

        if myDrone.send_rc_control:
            myDrone.send_rc_control(myDrone.left_right_velocity, myDrone.for_back_velocity,
                                    myDrone.up_down_velocity, myDrone.yaw_velocity)
        return errorLR, errorUD, errorFB