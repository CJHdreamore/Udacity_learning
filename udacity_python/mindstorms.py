import turtle
bro = turtle.Turtle()
def draw_square(some_turtle):
    for i in range(1,5):
        some_turtle.forward(100)
        some_turtle.right(90)

def draw_60triangle(some_turtle):
     angle = 120
     for i in range(1,4):
         some_turtle.forward(100)
         some_turtle.right(angle)

def draw_unclose_circle(some_turtle):
    for i in range(200):
        some_turtle.backward(1)
        some_turtle.left(1)



def draw_picture():
    window = turtle.Screen()
    window.bgcolor('red')
    bro = turtle.Turtle()
    bro.shape("turtle")
    bro.color("blue")
    bro.speed(30)
    angle = 20
    for i in range(1,360/angle + 1):
        draw_60triangle(bro)
        bro.right(angle)
    bro.right(90)
    bro.forward(200)
    window.exitonclick()

#draw_picture()
