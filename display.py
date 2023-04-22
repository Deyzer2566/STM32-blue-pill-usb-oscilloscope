import serial
p = serial.Serial('COM6')
import threading
import pygame
width = 1366
height = 360

pygame.init()
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption('Osci')
clock = pygame.time.Clock()
def make_packet():
    return bytes([1,timeout&255, (timeout>>8)&255])
arr = []
running = True
timeout = 10
packet = make_packet()
p.write(packet)
offtime = 0
curtime = 0
offY = height/2
pygame.font.init() # you have to call this at the start,
                   # if you want to use this module.
my_font = pygame.font.SysFont('Comic Sans MS', 10)
count_of_labels=15
def read_packet():
    global curtime
    global offtime
    global timeout
    global arr
    while running:
        t = p.read(2)
        t = int.from_bytes(t,byteorder='little');
        curtime += timeout
        arr+=[(curtime,t/4095*height)]
thread1 = threading.Thread(target=read_packet)
thread1.daemon=True
thread1.start()
k = 1
while(running):
    screen.fill((255,255,255))
    pygame.draw.line(screen,(0,0,0),(0,height/2),(width,height/2))
    pygame.draw.line(screen,(0,0,0),(width/2,0),(width/2,height))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEWHEEL:#-1 - приближение, 1 - отдаление
            timeout += event.y
            if(timeout < 1):
                timeout = 1
                k += 0.25
            if(event.y == 1 and k > 1):
                k -= 0.25
                timeout = 1
            packet = make_packet()
            p.write(packet)
    points_on_screen = (curtime-offtime)/timeout*k
    if(points_on_screen >= width):
        arr.clear()
        offtime = curtime
    print(timeout,k)
    for i in range(count_of_labels):
        text_surface = my_font.render(str(round(i/count_of_labels*width*timeout/k,2)), False, (0, 0, 0))
        screen.blit(text_surface, (i/count_of_labels*width,height/2))
        pygame.draw.line(screen, (0,0,0), (i/count_of_labels*width,0),(i/count_of_labels*width,height))
    for i in range(len(arr)-1):
        ct = (arr[i][0]-offtime)/timeout*k
        cm = height - arr[i][1]/2 - offY
        
        nt = (arr[i+1][0]-offtime)/timeout*k
        nm = height - arr[i+1][1]/2 - offY
        
        pygame.draw.line(screen,(0,0,0),(ct,cm),(nt,nm),2)
    pygame.display.flip()
timeout=0
packet = make_packet()
p.write(packet)
pygame.quit()
p.close()