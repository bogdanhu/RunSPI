import math
class Punct:
    def __init__(self,PunctX,PunctY):
        self.x=PunctX
        self.y=PunctY
    def __sub__(self,other):
        distanta=math.sqrt(math.pow((self.x-other.x),2)+math.pow((self.y-other.y),2))
        return f"Distanta intre doua puncte este {distanta:.2f}"
if __name__=="__main__":
    PunctA=Punct(10,10)
    PunctB=Punct(20,20)
    print(PunctA-PunctB)
    #distanta euclidiana
    #sqrt((x2-x1)^2+(y2-y1)^2)
    #A-B=>distanta euclidiana