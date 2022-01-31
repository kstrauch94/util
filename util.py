import time
import functools
from typing import Dict
from collections import defaultdict

from typing import Any, Optional, Callable

import sys

from math import copysign


class TimerError(Exception):
	pass


class Timer:
	timers: Dict[str, float] = defaultdict(lambda: 0)

	def __init__(self, name: str):
		self.name = name

		self._time_start: Optional[float] = None

	def start(self) -> None:

		if self._time_start is not None:
			raise TimerError("Timer started twice without stopping")

		self._time_start = time.perf_counter()

	def stop(self) -> float:

		if self._time_start is None:
			raise TimerError("Timer stopped without starting")

		stop = time.perf_counter() - self._time_start
		self._time_start = None

		Timer.timers[self.name] += stop

		return stop

	def __enter__(self) -> "Timer":
		self.start()

		return self

	def __exit__(self, *exc_info: Any) -> None:
		self.stop()

	def __call__(self, func) -> Callable:

		@functools.wraps(func)
		def wrapper_timer(*args, **kwargs):
			with self:
				return func(*args, **kwargs)

		return wrapper_timer


class Count:
	counts = defaultdict(lambda: 0)

	def __init__(self, name: str):
		self.name = name

	def __enter__(self) -> "Count":
		Count.counts[self.name] += 1

		return self

	def __exit__(self, *exc_info: Any) -> None:
		pass

	def __call__(self, func) -> Callable:
		@functools.wraps(func)
		def wrapper_count(*args, **kwargs):
			with self:
				return func(*args, **kwargs)

		return wrapper_count

	@classmethod
	def add(cls, name, amt=1) -> None:
		Count.counts[name] += amt


def print_stats(step, accu):
	time_prop = 0
	for name, time_taken in sorted(Timer.timers.items()):
		if "Propagation" in name:
			time_prop += time_taken
			continue
		else:
			print(f"{name:19}  :   {time_taken:.3f}")
			accu[f"{name:24}"] = time_taken

	print("{name:19}  :   {time_taken:.3f}".format(name="Time for propagation", time_taken=time_prop))
	accu["{name:24}".format(name="Time for propagation")] = time_taken


	for name, count in sorted(Count.counts.items()):
		print(f"{name:24}  :   {count}")
		accu[f"{name:24}"] = count



def get_size(obj, seen=None):
	"""
	Recursively finds size of objects
	from this website(14.10.2020):
	https://goshippo.com/blog/measure-real-size-any-python-object/
	"""
	size = sys.getsizeof(obj)
	if seen is None:
		seen = set()
	obj_id = id(obj)
	if obj_id in seen:
		return 0
	# Important mark as seen *before* entering recursion to gracefully handle
	# self-referential objects
	seen.add(obj_id)
	if isinstance(obj, dict):
		size += sum([get_size(v, seen) for v in obj.values()])
		size += sum([get_size(k, seen) for k in obj.keys()])
	elif hasattr(obj, '__dict__'):
		size += get_size(obj.__dict__, seen)
	elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes, bytearray)):
		size += sum([get_size(i, seen) for i in obj])
	return size


def sign(y):
	return copysign(1, y)


#testBit() returns a nonzero result, 2**offset, if the bit at 'offset' is one.
def test_bit(int_type, offset):
    mask = 1 << offset
    return(int_type & mask)

# setBit() returns an integer with the bit at 'offset' set to 1.
 
def set_bit(int_type, offset):
    mask = 1 << offset
    return(int_type | mask)

# clearBit() returns an integer with the bit at 'offset' cleared.

def clear_bit(int_type, offset):
    mask = ~(1 << offset)
    return(int_type & mask)

# toggleBit() returns an integer with the bit at 'offset' inverted, 0 -> 1 and 1 -> 0.

def toggle_bit(int_type, offset):
    mask = 1 << offset
    return(int_type ^ mask)

# returns False if bit at offset is 0, True otherwise
def is_bit_true(int_type, offset):
	if test_bit(int_type, offset) > 0:
		return True
	return False