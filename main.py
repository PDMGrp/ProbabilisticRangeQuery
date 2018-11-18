import MongoDB
import matplotlib
import matplotlib.colors as colors
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import numpy as np
import random
import time
import datetime
import math

Threshold=0.95
print("Confidence Threshold: ",Threshold)

min_temp = float(input("Please enter your minimum temperature: "))
min_humid = float(input("Please enter your minimum humidity: "))
max_temp = float(input("Please enter your maximum temperature: "))
max_humid = float(input("Please enter your maximum humidity: "))

sw_range = int(input("Please enter the Sliding Window size: "))
start_time = input("Please enter your start time of query (YYYY-M-D-H): ")
stime_list = start_time.split('-')
start_time = datetime.datetime(int(stime_list[0]), int(stime_list[1]), int(stime_list[2]), int(stime_list[3]))

counter = 0
coord = []
circles = []

while True:
  Reading_List = MongoDB.main(sw_range, start_time, counter)
  print("Length of Reading_List:", len(Reading_List))

  ctr=1 
  Check_List = []
  Num_Of_Sensors = 58

  plt.axes()
  
  while ctr <= Num_Of_Sensors:
    i=0
    while i < len(Reading_List):
      sensor_name = "sensor"+str(ctr)
      if ctr==Reading_List[i][1]:   # to check if the sensor id is the same ctr's value
        Check_List.append(Reading_List[i])
      i+=1
      
    Yes_ctr = 0     #to count number of readings fall in the user-given range query
    No_ctr = 0      #to count number of readings fall out of the user-given range query

    if len(Check_List) > 0:
      s_min_temp = Check_List[0][2]
      s_min_hum = Check_List[0][3]
    else:
      s_min_temp = 0
      s_min_hum = 0
      
    s_max_hum = 0
    s_max_temp = 0

    i=0
    while i<len(Check_List):

      if(Check_List[i][2] < s_min_temp):
        s_min_temp = Check_List[i][2]

      if(Check_List[i][2] > s_max_temp):
        s_max_temp = Check_List[i][2]

      if(Check_List[i][3] < s_min_hum):
        s_min_hum = Check_List[i][3]

      if(Check_List[i][3] > s_max_hum):
        s_max_hum = Check_List[i][3]

      if(Check_List[i][2]>=min_temp and Check_List[i][2]<=max_temp) and (Check_List[i][3]>=min_humid and Check_List[i][3]<=max_humid):
        Yes_ctr+=1
      else:
        No_ctr+=1

      i+=1

    if No_ctr == len(Check_List):
      probability = 100
    else:
      probability = No_ctr/len(Check_List)

    if len(Check_List) == 0:
      print("No readings returned for the %s during the given range!" % sensor_name)
    elif probability >= Threshold:
      print("Warning: the %s is in danger with confidence %f!" % (sensor_name,probability))
    else:
      print("No action is required: %s %f" % (sensor_name, probability))
      
    coord.append([s_min_temp,s_min_hum,s_max_temp,s_max_hum])


    #draw circle inside rectangle
    
    nohr=1

    circle_list = []

    
    end_time = start_time + datetime.timedelta(hours = nohr)
    if len(Check_List) > 0:

      temp_min = Check_List[0][2]
      humid_min = Check_List[0][3]
      temp_max = 0
      humid_max = 0

      loop_time = start_time
      while nohr<=sw_range:
        i=0
        while i<len(Check_List):
          if Check_List[i][0]>=start_time and Check_List[i][0]<=end_time:
            if(Check_List[i][2] < s_min_temp):
                temp_min = Check_List[i][2]
            if(Check_List[i][2] > s_max_temp):
                temp_max = Check_List[i][2]
            if(Check_List[i][3] < s_min_hum):
                humid_min = Check_List[i][3]
            if(Check_List[i][3] > s_max_hum):
                humid_max = Check_List[i][3]
          i+=1

        p1=math.floor(abs(temp_max-temp_min)/2)
        p2=math.floor(abs(humid_max-humid_min)/2)

        circle = plt.Circle((temp_min+p1,humid_min+p2), .5)

        circle_list.append(circle)
        #plt.gca().add_patch(circle)

        nohr+=1
        loop_time = end_time
        end_time = loop_time + datetime.timedelta(hours = nohr)


    circles.append(circle_list)

    Check_List.clear()    
    ctr+=1

  
  #rectangle = plt.Rectangle((min_temp, min_humid), max_temp - min_temp, max_humid - min_humid, fc='y', linestyle='dashed')
  #plt.gca().add_patch(rectangle)

  #Color_List = list(colors._colors_full_map.values())

  number_of_colors = 100
  color = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
             for i in range(number_of_colors)]

  i=0
  while i<len(coord):
    plt.close()
    plt.axes()
    rectangle = plt.Rectangle((min_temp, min_humid), max_temp - min_temp, max_humid - min_humid, fc='y', linestyle='dashed')
    plt.gca().add_patch(rectangle)
    for x in range(0,i+1):
      MBR = plt.Rectangle((coord[x][0], coord[x][1]), coord[x][2] - coord[x][0], coord[x][3] - coord[x][1], fc=color[x])
      plt.gca().add_patch(MBR)
      for y in range (0,len(circles[x])):
        plt.gca().add_patch(circles[x][y])
    i+=1

    plt.axis('scaled')
    plt.show()
    time.sleep(2)

    

  #plt.axis('scaled')
  #plt.show()

  counter+= 1
  
  Key = input("Enter Y to check the sensor situations, N to stop checking: ")
  if Key=='N' or Key=='n':
    break
        




    

