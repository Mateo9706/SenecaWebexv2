
def convert(quality):
    qual = quality.split("%")
    #print(qual)
    #quality = 2 * (dBm + 100) #where dBm: [-100 to - 50]
    dBm = (int(qual[0])/2) - 100 #where quality: [0 to 100]
    #print(str(dBm) + " dBm")
    return str(dBm)


#convert("50%")