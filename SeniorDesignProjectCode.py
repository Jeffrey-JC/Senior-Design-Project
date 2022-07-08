import drivers
from datetime import datetime, date
import time
import regex
from ina219 import INA219
import matplotlib.pyplot as plt
from gpiozero import Button
from signal import pause
import os
import sys

currentTime = datetime.now()
fileName = currentTime.strftime("%Y-%m-%d %H-%M-%S")
currentDate = currentTime.strftime("%m/%d/%Y")
ina = INA219(shunt_ohms=0.1,
             max_expected_amps = 0.6,
             address = 0x41)

ina2 = INA219(shunt_ohms=0.1,
             max_expected_amps = 0.6,
             address = 0x40)

ina3 = INA219(shunt_ohms=0.1,
             max_expected_amps = 0.6,
             address = 0x45)

ina4 = INA219(shunt_ohms=0.1,
             max_expected_amps = 0.6,
             address = 0x44)
display= drivers.Lcd()

ina.configure(voltage_range = ina.RANGE_16V,
              gain = ina.GAIN_AUTO,
              bus_adc=ina.ADC_128SAMP,
              shunt_adc=ina.ADC_128SAMP)

ina2.configure(voltage_range = ina2.RANGE_16V,
              gain = ina2.GAIN_AUTO,
              bus_adc=ina2.ADC_128SAMP,
             shunt_adc=ina2.ADC_128SAMP)

ina3.configure(voltage_range = ina3.RANGE_16V,
              gain = ina3.GAIN_AUTO,
              bus_adc=ina3.ADC_128SAMP,
             shunt_adc=ina3.ADC_128SAMP)

ina4.configure(voltage_range = ina4.RANGE_16V,
              gain = ina4.GAIN_AUTO,
              bus_adc=ina4.ADC_128SAMP,
             shunt_adc=ina4.ADC_128SAMP)

status = True 

def sensor_code():
    global status

    if status:
        start = time.perf_counter()
        while status:
            c = ina.current()
            c2 = ina2.current()
            c3 = ina3.current()
            c4 = ina4.current()
            string = "{:.3f}   " + str('{0:0.2f}mA'.format(c))
            string2 = str('{0:0.2f}mA'.format(c2))
            string3 = str('{0:0.2f}mA'.format(c3))
            string4 = str('{0:0.2f}mA'.format(c4))
            display.lcd_display_string(str('{0:0.2f}mA      '.format(c)) + str('{0:0.2f}mA'.format(c2)), 2)
            display.lcd_display_string(str('{0:0.2f}mA      '.format(c3)) + str('{0:0.2f}mA'.format(c4)), 4)
            file = open("/home/pi/Desktop/" + fileName + ".txt", "a")
            end = time.perf_counter() - start
            print(end)
            file.write(string.format(end) + "     "  + string2 + "     "  + string3 + "     "  + string4 + "\n")
            if button.is_pressed and end > 1:
                status = False
                sensor_code()
    else:
        f = open("/home/pi/Desktop/" + fileName+'.txt','r')
        new_str = f.read()
        g = regex.findall('\d*\.?\d+',new_str)
        #print(g)
        plt.xlabel('Time (s)')
        plt.ylabel ('Current (mA)')
        plt.title('Time vs Current Graph')
        x1 = [0]
        y1 = [0]
        y2 = [0]
        y3 = [0]
        y4 = [0]
        t=0
        total1 = 0
        total2 = 0
        total3 = 0
        total4 = 0
        s = [float(x) for x in g]
        for i in range (7, len(g), 5):
            #print(s[i])
            #print(s[i+1])
            #print(s[i+2])
            x1.append(s[i])
            y1.append(s[i+1])
            y2.append(s[i+2])
            y3.append(s[i+3])
            y4.append(s[i+4])
            total1 +=s[i+1]
            total2 +=s[i+2]
            total3 +=s[i+3]
            total4 +=s[i+4]
            plt.plot(x1, y1, c="blue")
            plt.plot(x1, y2, c="red")
            plt.plot(x1, y3, c="green")
            plt.plot(x1, y4, c="purple")
            t += 1
        f = open("/home/pi/Desktop/" + fileName+'.txt', 'a')
        avg1 = total1/(t)
        avg2 = total2/(t)
        avg3 = total3/(t)
        avg4 = total4/(t)
        f.write("Solar cell 1 average is {0:.2f}\n".format(avg1))
        f.write("Solar cell 2 average is {0:.2f}\n".format(avg2))
        f.write("Solar cell 3 average is {0:.2f}\n".format(avg3))
        f.write("Solar cell 4 average is {0:.2f}\n".format(avg4))
        f.close()
        plt.legend(["Sensor 1","Sensor 2", "Sensor 3", "Sensor 4"], loc="upper right")
        plt.grid()
        plt.savefig("/home/pi/Desktop/" + fileName + ".png", dpi = 300, bbox_inches='tight')
        #plt.show()
        os.execl(sys.executable, sys.executable, *sys.argv)
    

button = Button(23)

try:
    file = open("/home/pi/Desktop/" + fileName + ".txt", "a")
    file.write(currentDate + "\nTime(s) Current1   Current2   Current3   Current4\n")
    file.close()
    display.lcd_display_string("Sensor 1   Sensor 2", 1)
    display.lcd_display_string("Sensor 3   Sensor 4", 3)
    
    button.when_pressed = sensor_code
    pause()
        #x1.append(end)
        #y1.append(c)
        #y2.append(c2)
        #plt.plot(x1, y1)
        #plt.plot(x1, y2)
       #plt.savefig('It_worked.png')
        
except KeyboardInterrupt:
    quit()
    
    
finally:
    pass