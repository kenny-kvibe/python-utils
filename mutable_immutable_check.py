import sys


NAME_PADD = 10
PRINT_OBJ_SIZE = True


def main() -> int:
	# Immutable (Re-referenced)
	print_mut(None)                # Size: 16
	print_mut(False)               # Size: 28
	print_mut(True)                # Size: 28
	print_mut(bool)                # Size: 28
	print_mut(int)                 # Size: 28
	print_mut(bytes)               # Size: 33
	print_mut(tuple)               # Size: 40
	print_mut(str)                 # Size: 49

	# Mutable (Mutated)
	print_mut(object)              # Size: 16
	print_mut(float)               # Size: 24
	print_mut(complex)             # Size: 32
	print_mut(range, 0)            # Size: 48
	print_mut(bytearray, b'')      # Size: 56
	print_mut(list)                # Size: 56
	print_mut(slice, 0)            # Size: 56
	print_mut(dict)                # Size: 64
	print_mut(enumerate, tuple())  # Size: 72
	print_mut(memoryview, b'')     # Size: 184
	print_mut(frozenset)           # Size: 216
	print_mut(set)                 # Size: 216
	return 0


def print_mut(cls, *cls_args):
	name_rsep = '":'
	length = NAME_PADD + len(name_rsep)
	name = getattr(cls, '__name__', str(cls)) + name_rsep
	mut_type = 'Re-referenced' if is_same_reference(cls, *cls_args) else 'Mutated'
	if PRINT_OBJ_SIZE:
		if cls is None or cls is True or cls is False:
			size = sys.getsizeof(cls)
		else:
			size = sys.getsizeof(cls(*cls_args))
	else:
		size = -1
	print(f'Type "{name:{length}s} {mut_type}' +
		(f' (Size: {size})' if size >= 0 else ''))


def is_same_reference(cls, *cls_args) -> bool:
	""" check if `cls` uses same reference """
	if cls is None or cls is True or cls is False: return True
	return cls(*cls_args) is cls(*cls_args)


def is_mutated(cls, *cls_args) -> bool:
	""" check if `cls` mutated """
	return not is_same_reference(cls, *cls_args)


if __name__ == '__main__':
	raise SystemExit(main())

