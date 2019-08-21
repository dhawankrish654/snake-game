import pygame as p
import time
import random as rnd



scores_file=open("scores.txt","r+")
scores=[]


for line in scores_file:
	if line!="\n":
		a=line.split()
		scores.append(  [a[0], int(a[1])]  )


def sortFunc(x):
	return x[1]
scores.sort(key=sortFunc,reverse=True)


def write_scores(name,new_score):
	the_score = None
	for score in scores:
		if score[0] == name:
			the_score = score
			break

	if the_score != None:
		if the_score[1] < new_score:
			the_score[1] = new_score
	else:
		scores.append( [name, new_score] )

	scores.sort(key=sortFunc,reverse=True)

def write_to_file():
	scores_file.seek(0,0)
	for score in scores:
		scores_file.write(str(score[0])+" "+str(score[1])+"\n")

p.init()

#colors:

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green=(0,155,0)

#inputs

name=input("What is your name? ")

while True:
	FPS=int(input("please inter an integr between 10 and 60 for game speed: "))
	if FPS<10 or FPS>60:
		print("incorrect speed")
	else:
		break


#game features

display_width=1000
display_height=1000
step=10
blocksize=10
gameExitt=False
gameLosee=False
lead_x=rnd.randrange(0,display_width,blocksize)
lead_y=rnd.randrange(0,display_height,blocksize)
lead_x_change=0
lead_y_change=0
score=0
snake_lenght=1
apple_size=25
speed=FPS
plus_speed_per_score=10
max_score=0

gameDisplay = p.display.set_mode((display_width,display_height))
p.display.set_caption("snake game")

clock=p.time.Clock()

def plus_speed(score):
	global FPS
	FPS=speed+score//plus_speed_per_score

def gameLose():
	if lead_x>display_width-blocksize or lead_y>display_height-blocksize or lead_x<0 or lead_y<0:
		return True
	if gameExitt:
		return True
	return False

def gameExit(event):
	if event.type == p.QUIT :
		return True
	return False

def gamePause():
	pass

def whereissnake_go():
	pass
def snake_move_back(key):
	pass

def gameRestart():
	global lead_x, lead_y, lead_x_change, lead_y_change, score, snake_lenght
	lead_x=rnd.randrange(0,display_width,blocksize)
	lead_y=rnd.randrange(0,display_height,blocksize)
	lead_x_change=0
	lead_y_change=0
	score=0
	snake_lenght=1

def movingSnake(event):
	global lead_x_change, lead_y_change
	if event.key == p.K_LEFT:
		lead_x_change=-step
		lead_y_change= 0
	elif event.key == p.K_RIGHT:
		lead_x_change=step
		lead_y_change= 0
	elif event.key == p.K_UP:
		lead_x_change=0
		lead_y_change=-step
	elif event.key == p.K_DOWN:
		lead_x_change=0
		lead_y_change=step

def snake(snake_list,blocksize):
	for XoY in snake_list:
		p.draw.rect(gameDisplay,black,[XoY[0],XoY[1],blocksize,blocksize])

def text_objects(text,color,sizefont):
	font=p.font.SysFont(None,sizefont)
	textSurface=font.render(text,True,color)
	return textSurface , textSurface.get_rect()
	
def message_to_screen(msg,color,x=0,y=0,sizefont=20):
	textSurf,textRect=text_objects(msg,color,sizefont)
	textRect.center=(display_width/2+x),(display_height/2+y)
	gameDisplay.blit(textSurf,textRect)
	p.display.flip()

randapple_x=rnd.randrange(0,display_width,apple_size)
randapple_y=rnd.randrange(0,display_height,apple_size)

while  not gameExitt :
	snake_list=[]
	message_to_screen("if you want play again press space",sizefont=40,y=-30,color=black)
	for event in p.event.get():
		gameExitt=gameExit(event)
		if event.type == p.KEYDOWN:
			if event.key == p.K_SPACE:
				gameLosee=False
				gameRestart()
	while  not gameLosee :
		gameLosee=gameLose()
		for event in p.event.get():
			gameExitt=gameExit(event)
			if event.type == p.KEYDOWN:
				movingSnake(event)

		#snake move
		lead_x+=lead_x_change
		lead_y+=lead_y_change
		snake_head=[]
		snake_head.append(lead_x)
		snake_head.append(lead_y)
		snake_list.append(snake_head)
		if len(snake_list)>snake_lenght:
			del snake_list[0]
		for each_segment in snake_list[:-1]:
			if each_segment==snake_head:
				gameLosee=True
		gameDisplay.fill(white)
		p.draw.rect(gameDisplay,red,[randapple_x,randapple_y,apple_size,apple_size])
		snake(snake_list,blocksize)
		p.display.flip()

		#eat apple

		if ((lead_x>=randapple_x and lead_x<randapple_x+apple_size) or (lead_x+blocksize>=randapple_x and lead_x+blocksize<randapple_x+apple_size)) and ((lead_y>=randapple_y and lead_y<randapple_y+apple_size) or (lead_y+blocksize>=randapple_y and lead_y+blocksize<randapple_y+apple_size)):
			randapple_x=rnd.randrange(0,display_width,apple_size)
			randapple_y=rnd.randrange(0,display_height,apple_size)
			score+=1
			snake_lenght+=1
		message_to_screen("score:"+str(score),green,-320,-250)
		max_score=max(max_score,score)
		message_to_screen("your max score:"+str(max_score),green,-320,-230)
		plus_speed(score)

		clock.tick(FPS)
	message_to_screen("GAME OVER",red,0,100,60)
message_to_screen("GOODBYE MY FRIEND",green,y=40,sizefont=100)
time.sleep(1)
p.quit()

write_scores(name,max_score)

print("This is the 20 top scores of this game :")

for i in range(min(20,len(scores))):
	print(scores[i][0],scores[i][1])

write_to_file()
