import turtle

def draw_tree(t, length, angle_left, angle_right, depth, reduction_factor, max_branches, current_branch=0):
    if depth == 0 or current_branch >= max_branches:
        return
    else:
        # Set the color and line thickness based on the depth
        if depth == 10:  # The first (trunk) branch is brown and thicker
            t.pencolor("brown")
            t.pensize(5)
        else:  # The remaining branches are green and thinner
            t.pencolor("green")
            t.pensize(2)

        t.forward(length)  # Draw the current branch

        t.left(angle_left)  # Turn left
        # Draw the left subtree with a reduced branch length
        draw_tree(t, length * reduction_factor, angle_left, angle_right, depth - 1, reduction_factor, max_branches, current_branch + 1)

        t.right(angle_left + angle_right)  # Turn right (this is a larger angle to account for both directions)
        # Draw the right subtree with a reduced branch length
        draw_tree(t, length * reduction_factor, angle_left, angle_right, depth - 1, reduction_factor, max_branches, current_branch + 1)

        t.left(angle_right)  # Restore the left turn
        t.backward(length)  # Return to the previous position (undo the forward movement)

def main():
    # User input for tree drawing parameters
    angle_left = float(input("Enter the left branch angle: "))
    angle_right = float(input("Enter the right branch angle: "))
    starting_length = float(input("Enter the starting branch length: "))
    depth = int(input("Enter the recursion depth: "))
    reduction_factor = float(input("Enter the branch length reduction factor (e.g., 0.7 for 70%): "))
    max_branches = 7  # Limit to 7 main branches

    # Set up the turtle window
    screen = turtle.Screen()
    screen.bgcolor("white")  # Set the background color to white
    t = turtle.Turtle()
    t.left(90)  # Make the turtle face upwards (this is the root branch direction)
    t.speed(0)  # Set the drawing speed to the fastest possible

    # Start the drawing from the center of the screen
    t.penup()  # Lift the pen to avoid drawing during positioning
    t.setpos(0, -200)  # Position the turtle at the bottom of the screen
    t.pendown()  # Lower the pen to start drawing

    # Draw the tree
    draw_tree(t, starting_length, angle_left, angle_right, depth, reduction_factor, max_branches)

    # Keep the window open
    screen.mainloop()

if __name__ == "__main__":
    main()
