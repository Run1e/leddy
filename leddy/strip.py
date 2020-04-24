from random import choice, randint

from .led import LEDContext
import numpy as np


class Strip:
	def __init__(self, count):
		self.count = count
		self.data = np.zeros(count * 3)
		self.data.resize(count, 3)
		self.leds = [LEDContext(index, self.data) for index in range(count)]
		self.gens = dict()

	def random(self):
		index = randint(0, self.count - 1)
		return self.leds[index]

	def random_available(self):
		available = [led for led in self.leds if led.index not in self.gens]

		if not available:
			return None

		return choice(available)

	def get(self, index):
		return self.leds[index]

	def get_opposite(self, index):
		return self.leds[(index + self.count // 2) % self.count]

	def set(self, led, color):
		self.gens.pop(led.index, None)
		led.set(*color)

	def set_all(self, color):
		self.gens.clear()

		for led in self.leds:
			led.set(*color)

	def assign(self, led, generator):
		self.gens[led.index] = (led, generator(led))
		led.needs_prep = True

	def assign_random(self, func, *args, **kwargs):
		led = self.random()
		self.assign(led, func, *args, **kwargs)

	def assign_available(self, func, *args, **kwargs):
		led = self.random_available()

		if led is None:
			return

		self.assign(led, func, *args, **kwargs)

	def assign_all(self, func, *args, **kwargs):
		for led in self.leds:
			self.assign(led, func, *args, **kwargs)

	def assign_all_available(self, func, *args, **kwargs):
		for led in filter(lambda led: led.index not in self.gens, self.leds):
			self.assign(led, func, *args, **kwargs)
