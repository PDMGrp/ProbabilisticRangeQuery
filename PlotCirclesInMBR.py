counter=1
end_time = start_time + counter

temp_min = Check_List[0][2]
humid_min = Check_List[0][3]
temp_max = 0
humid_max = 0

while counter<=12:
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

    circle = plt.Circle((p1,p2), 5)
    plt.gca().add_patch(circle)

    counter+=1
    start_time = end_time
    end_time = start_time + counter


    
    
