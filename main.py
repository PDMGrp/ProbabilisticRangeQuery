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
import functools

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
minmax = []

convex_hulls = []
total_points_list = []


def convex_hull_graham(points):
    '''
    Returns points on convex hull in CCW order according to Graham's scan algorithm.
    By Tom Switzer <thomas.switzer@gmail.com>.
    '''
    TURN_LEFT, TURN_RIGHT, TURN_NONE = (1, -1, 0)

    def cmp(a, b):
        return (a > b) - (a < b)

    def turn(p, q, r):
        return cmp((q[0] - p[0])*(r[1] - p[1]) - (r[0] - p[0])*(q[1] - p[1]), 0)

    def _keep_left(hull, r):
        while len(hull) > 1 and turn(hull[-2], hull[-1], r) != TURN_LEFT:
            hull.pop()
        if not len(hull) or hull[-1] != r:
            hull.append(r)
        return hull

    points = sorted(points)
    l = functools.reduce(_keep_left, points, [])
    u = functools.reduce(_keep_left, reversed(points), [])
    return l.extend(u[i] for i in range(1, len(u) - 1)) or l





while True:
  Reading_List = MongoDB.main(sw_range, start_time, counter, minmax)
  print("Length of Reading_List:", len(Reading_List))

  ctr=1 
  Check_List = []
  Num_Of_Sensors = 58

  plt.axes()

  print("Sensor ID\t(Min_temp, Min_humid)\t(Max_temp,Max_humid)\tProb(within_range)\tConfidence_to_be_in_danger\tStatus")
  print("---------------------------------------------------------------------------------------------------------------------------------------------------")
  
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
      probability = 1
    else:
      probability = No_ctr/len(Check_List)

    if len(Check_List) == 0:
      #print("No readings returned for the %s during the given range!" % sensor_name)
      print("%s  \t(null, null)\t\t(null, null)\t\tN/A\t\t\tN/A\t\t\t\tNo Records found!" % sensor_name)
    elif probability >= Threshold:
      #print("Warning: the %s is in danger with confidence %f!" % (sensor_name,probability))
      print("%s  \t(%f, %f)\t(%f, %f)\t%f\t\t%f\t\t\t** DANGER **" % (sensor_name, s_min_temp,s_min_hum,s_max_temp,s_max_hum,100-(probability*100), probability*100))
    else:
      print("%s  \t(%f, %f)\t(%f, %f)\t%f\t\t%f\t\t\tNOT IN DANGER." % (sensor_name, s_min_temp,s_min_hum,s_max_temp,s_max_hum,100-(probability*100), probability*100))
      #print("No action is required: %s %f" % (sensor_name, probability))
    
    coord.append([s_min_temp,s_min_hum,s_max_temp,s_max_hum])


    #draw circle inside rectangle
    
    nohr=1

    circle_list = []
    convex_hull_list = []
    sensor_points_list = []

    
    end_time = start_time + datetime.timedelta(hours = nohr)
    if len(Check_List) > 0:

      temp_min = Check_List[0][2]
      humid_min = Check_List[0][3]
      temp_max = 0
      humid_max = 0

      loop_time = start_time
      while nohr<=sw_range:
        i=0
        points_list = []

        while i<len(Check_List):
          if Check_List[i][0]>=loop_time and Check_List[i][0]<=end_time:
            points_list.append((Check_List[i][2], Check_List[i][3]))
            if(Check_List[i][2] < temp_min):
                temp_min = Check_List[i][2]
            if(Check_List[i][2] > temp_max):
                temp_max = Check_List[i][2]
            if(Check_List[i][3] < humid_min):
                humid_min = Check_List[i][3]
            if(Check_List[i][3] > humid_max):
                humid_max = Check_List[i][3]
          i+=1

        p1=math.floor(abs(temp_max-temp_min)/2)
        p2=math.floor(abs(humid_max-humid_min)/2)

        convex_hull_list.append(convex_hull_graham(points_list))
        sensor_points_list.append(points_list)
        #circle = plt.Circle((temp_min+p1,humid_min+p2), .5)

        circle_list.append((temp_min, humid_min, temp_max, humid_max))
        #plt.gca().add_patch(circle)

        nohr+=1
        loop_time = end_time
        end_time = loop_time + datetime.timedelta(hours = nohr)


    circles.append(circle_list)
    convex_hulls.append(convex_hull_list)
    total_points_list.append(sensor_points_list)

    Check_List.clear()    
    ctr+=1

  
  #rectangle = plt.Rectangle((min_temp, min_humid), max_temp - min_temp, max_humid - min_humid, fc='y', linestyle='dashed')
  #plt.gca().add_patch(rectangle)

  #Color_List = list(colors._colors_full_map.values())

  number_of_colors = 100
  color = []
  for i in range(number_of_colors):
    randColor = "#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
    if randColor not in color:
      color.append(randColor)
  # color = ["#"+''.join([random.choice('0123456789ABCDEF89ABCDEF') for j in range(6)])
  #            for i in range(number_of_colors)]

  i=0
  while i<len(coord):
    plt.axes()
    rectangle = plt.Rectangle((min_temp, min_humid), max_temp - min_temp, max_humid - min_humid, fc='y')
    plt.gca().add_patch(rectangle)
    #for x in range(0, i+1):
    MBR = plt.Rectangle((coord[i][0], coord[i][1]), coord[i][2] - coord[i][0], coord[i][3] - coord[i][1], fc=color[2], alpha=0.3)
    plt.gca().add_patch(MBR)
    if (coord[i][0] + coord[i][1] + coord[i][0] + coord[i][1]) > 0:
      plt.text(0.5*(coord[i][0]+coord[i][2]), 0.5*(coord[i][1]+coord[i][3]), 'Sensor'+str(i+1), horizontalalignment='center', verticalalignment='center', fontsize=10, color='red')
    #print(circles[i])
    #print(coord[i])
    if(len(circles[i])>0):
      for y in range (0,len(circles[i])):
        cir = plt.Rectangle((circles[i][y][0],circles[i][y][1]), circles[i][y][2] - circles[i][y][0], circles[i][y][3] - circles[i][y][1], alpha = 1, fc='none', linestyle='dashed')
        plt.gca().add_patch(cir)
    if(len(convex_hulls[i])>0):
      for y in range(0, len(convex_hulls[i])):
        if convex_hulls[i][y]:
          x_coordiate = [obj[0] for obj in convex_hulls[i][y]]
          y_coordinate = [obj[1] for obj in convex_hulls[i][y]]
          # coordinates for scatter points
          x_co = [obj[0] for obj in total_points_list[i][y]]
          y_co = [obj[1] for obj in total_points_list[i][y]]
          # uncomment this line to plot all the points inside the hulls
          # plt.gca().add_artist(plt.scatter(x_co, y_co, label='skitscat', color=color[y], s=1, marker="o"))

          plt.gca().add_artist(plt.scatter(x_coordiate, y_coordinate, label='skitscat', color=color[y], s=1, marker="o"))

          plt.gca().add_patch(plt.Polygon(convex_hulls[i][y], fill=0, linestyle='--', linewidth=0.5,alpha=0.3, color=color[y]))


    i+=1
    #plt.axis('scaled')


    if minmax[2] > max_temp:
      xmax = minmax[2] + 10
    else:
      xmax = max_temp + 10
    if minmax[3] > max_humid:
      ymax = minmax[3] + 10
    else:
      ymax = max_humid + 10
    plt.xlim(minmax[0] - 5, xmax)
    plt.ylim(0, ymax)
    plt.savefig('sensor'+str(i)+'.jpg')
    plt.show()
    time.sleep(1)
    plt.close()

  #plt.axis('scaled')
  #plt.show()
  #time.sleep(2)  

    

  #plt.axis('scaled')
  #plt.show()

  counter+= 1
  
  Key = input("Enter Y to check for the next window between the period %s - %s: ", (str(start_time+datetime.timedelta(hours=1)), str(start_time + datetime.timedelta(hours = 1+sw_range))))
  if Key=='N' or Key=='n':
    break
        




    

