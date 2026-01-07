import turtle
import random

def draw_tree(branch_len, t, thickness):
    if branch_len > 5:
        # Set thickness based on branch depth
        t.pensize(thickness)
        
        # Draw the branch
        t.forward(branch_len)
        
        # Randomize angles for a more "natural" aesthetic
        angle = random.randint(18, 25)
        reduction = random.uniform(10, 15)
        
        # Right branch
        t.right(angle)
        draw_tree(branch_len - reduction, t, thickness * 0.7)
        
        # Left branch
        t.left(angle * 2)
        draw_tree(branch_len - reduction, t, thickness * 0.7)
        
        # Return to center
        t.right(angle)
        t.backward(branch_len)

def main():
    screen = turtle.Screen()
    screen.bgcolor("#1e1e1e")  # Aesthetic dark mode background
    
    t = turtle.Turtle()
    t.speed(0)
    t.left(90)
    t.up()
    t.backward(200)
    t.down()
    t.color("#a2d2fb")  # Aesthetic neon blue
    
    draw_tree(100, t, 10)
    screen.exitonclick()

if __name__ == "__main__":
    main()