from typing import List, Tuple


def unitize_vector(a):
	magnitude = calculate_magnitude(a)
	if magnitude == 0:
		return (0, 0)
	
	return (a[0] / magnitude, a[1] / magnitude)

def multiply_vector(vector, amount):
	return (vector[0] * amount, vector[1] * amount)

def divide_vector(vector, amount):
	return (vector[0] / amount, vector[1] / amount)

def add_vectors(a, b):
	return (a[0] + b[0], a[1] + b[1])

def vector_from_a_to_b(a, b):
	return (b[0] - a[0], b[1] - a[1])

def calculate_magnitude(a):
	return (a[0] * a[0] + a[1] * a[1]) ** 0.5

def calculate_distance(a, b):
	return calculate_magnitude(vector_from_a_to_b(a, b))

k_constant = 9e9

class ChargedParticle:
	def __init__(self, charge, mass):
		self.charge = charge
		self.mass = mass
		self.velocity = (0, 0)

class World:
	def __init__(self):
		self.particles: List[Tuple[ChargedParticle, Tuple[float, float]]] = []

	def add_particle(self, particle, x, y):
		self.particles.append((particle, (x, y)))

	def apply_charges(self, timestep=0.01):
		"""Applies the charge forces on the particles in the World. This does not update the position of the particles, only their velocity.

		Args:
				timestep (float, optional): The amount of time to step by (dt). Defaults to 0.01.
		"""

		# forces_to_apply keeps track of changes before we move the particles
		forces_to_apply: List[Tuple[int, Tuple[float, float]]] = []

		for i in range(len(self.particles)):
			first_particle, first_position = self.particles[i]

			for j in range(len(self.particles)):
				if i == j:
					continue

				second_particle, second_position = self.particles[j]

				# Force to apply is in direction of other particle
				# k * Q * q / r^2
				# Unit check: N * m^2 / c^2 * c * c / m^2 = N (works!)
				unit_vector = unitize_vector(vector_from_a_to_b(first_position, second_position))
				magnitude = k_constant * first_particle * second_particle * calculate_distance(first_position, second_position)
				force = multiply_vector(unit_vector, magnitude)

				# apply the force `force` on the particle at position `j`
				forces_to_apply.append((j, force))

		for receiver_index, force in forces_to_apply:
			particle, position = self.particles[receiver_index]
			acceleration = divide_vector(add_vectors(position, force), particle.mass)
			particle.velocity = add_vectors(particle.velocity, multiply_vector(acceleration, timestep))
		
	def apply_velocities(self, timestep=0.01):
		"""
		Steps the particles through time by moving them according to their velocities.
		This method does not apply any forces.

		Args:
				timestep (float, optional): The amount of time to step by (dt). Defaults to 0.01.
		"""

		for i in range(len(self.particles)):
			particle, position = self.particles[i]
			# Update the position of the particle
			new_position = add_vectors(position, multiply_vector(particle.velocity, timestep))
			self.particles[i] = particle, new_position