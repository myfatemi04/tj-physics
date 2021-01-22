# Made by Michael Fatemi (c) 2021

import pygame
import time

# A cart contains position, mass, velocity, and color, in that order

POSITION = 0
MASS = 1
VELOCITY = 2
COLOR = 3

carts = [
	# (-2, 1, 2, (255, 0, 0)),
	# (2, 1, 0, (0, 0, 255)),
	# (-3, 1, 2, (255, 0, 0)),
	(-4, 2, 25, (0, 0, 255)),
	(-2, 0.5, 0, (255, 0, 0)),
	(-1, 0.5, 0, (255, 0, 0)),
	(0, 0.5, 0, (0, 255, 0)),
	(1, 0.5, 0, (0, 255, 0)),
]

leftmost_pos = -5
rightmost_pos = 5
screen_width = 640
screen_height = 480
cart_y = 400
cart_phys_width = 0.50
cart_phys_height = 0.24
cart_screen_width = screen_width * cart_phys_width / (leftmost_pos - rightmost_pos)
cart_screen_height = 24 # cart_phys_height / (leftmost_pos - rightmost_pos)

scale_pos = lambda position: (position - leftmost_pos) / (rightmost_pos - leftmost_pos)

# At each time step, check for any collisions
# Where there are collisions, calculate the new velocities of the carts
# Update velocities after calculations have completed
# After all velocities for all carts have been updated, update the positions of the carts

def step(carts, dt):
	carts = sorted(carts)

	# Check for collisions
	# If there is a cart where you would have been, mark that as the collision, and stop checking
	# Each 'collision' is a pair of carts: the cart sending the collision, the cart receiving the collision
	collisions = set()
	# print(carts)
	for i in range(len(carts)):
		position, mass, velocity, _ = carts[i]

		# we're moving to the left
		if velocity <= 0 and i - 1 >= 0:
			cart_before = carts[i - 1]
			cart_before_velocity = cart_before[VELOCITY]

			# the other cart is moving to the left (relatively)
			if cart_before_velocity - velocity > 0:
				cart_before_right_bound = cart_before[POSITION] + cart_phys_width / 2
				next_left_bound = position - cart_phys_width / 2
				
				if cart_before_right_bound > next_left_bound:
					# this is a collision
					collisions.add((i, i - 1))

		# we're moving to the right
		elif velocity > 0 and i + 1 < len(carts):
			cart_after = carts[i + 1]
			cart_after_velocity = cart_after[VELOCITY]

			# the other cart is moving to the right (relatively)
			if cart_after_velocity - velocity < 0:
				cart_after_left_bound = cart_after[0] - cart_phys_width / 2
				next_right_bound = position + cart_phys_width / 2
				if cart_after_left_bound < next_right_bound:
					# this is a collision
					collisions.add((i, i + 1))

	velocity_updates = []

	if collisions:
		print(collisions)

	# Calculate the velocity changes of the carts
	for first_id, second_id in collisions:
		_, first_mass, first_velocity, _ = carts[first_id]
		_, second_mass, second_velocity, _ = carts[second_id]
		first_momentum = first_mass * first_velocity
		second_momentum = second_mass * second_velocity
		
		# Pretend they're converging on the center of mass
		# What are their relative velocities to the center of mass?
		com_momentum = first_momentum + second_momentum
		com_velocity = com_momentum / (first_mass + second_mass)

		first_cart_velocity_relative_to_com = first_velocity - com_velocity # should be positive
		second_cart_velocity_relative_to_com = second_velocity - com_velocity # should be negative

		print(com_velocity, first_velocity, second_velocity)

		velocity_updates.append((first_id, second_cart_velocity_relative_to_com * second_mass / first_mass))
		velocity_updates.append((second_id, first_cart_velocity_relative_to_com * first_mass / second_mass))

	for cart_id, velocity_update in velocity_updates:
		carts[cart_id] = (
			carts[cart_id][0],
			carts[cart_id][1],
			carts[cart_id][2] + velocity_update,
			carts[cart_id][3]
		)
		
	# Update the positions of the carts
	for i, cart in enumerate(carts):
		position, mass, velocity, color = cart
		carts[i] = (position + velocity * dt, mass, velocity, color)

	return carts

def draw_carts(screen, carts):
	for cart in carts:
		position, mass, velocity, color = cart
		scaled_x = scale_pos(position)
		screen_x = scaled_x * screen_height
		screen_y = cart_y

		cart_rect = pygame.Rect(
			screen_x - cart_screen_width / 2,
			screen_y - cart_screen_height / 2,
			cart_screen_width,
			cart_screen_height
		)

		pygame.draw.rect(screen, color, cart_rect)

screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Crash... Boom")
pygame.display.flip()

background_color = (41, 45, 62) # VS Code dark theme background
cart_color = (247, 140, 108) # VS Code dark theme red

running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.constants.QUIT:
			running = False

	screen.fill(background_color)

	draw_carts(screen, carts)
	carts = step(carts, 0.01)
	time.sleep(0.01)

	pygame.display.flip()
