import sys


PRINT_NAME_PADD = 0
PRINT_OBJ_SIZE = True


def main() -> int:
	global PRINT_NAME_PADD
	PRINT_NAME_PADD = 10

	# Immutable
	print_mutable(None)                # Size: 16
	print_mutable(bool)                # Size: 28
	print_mutable(int)                 # Size: 28
	print_mutable(bytes)               # Size: 33
	print_mutable(tuple)               # Size: 40
	print_mutable(str)                 # Size: 49

	# Mutable
	print_mutable(object)              # Size: 16
	print_mutable(complex)             # Size: 32
	print_mutable(range, 0)            # Size: 48
	print_mutable(bytearray, b'')      # Size: 56
	print_mutable(slice, 0)            # Size: 56
	print_mutable(list)                # Size: 56
	print_mutable(dict)                # Size: 64
	print_mutable(enumerate, tuple())  # Size: 72
	print_mutable(memoryview, b'')     # Size: 184
	print_mutable(set)                 # Size: 216
	print_mutable(frozenset)           # Size: 216
	return 0


def print_mutable(cls, *cls_args):
	col = '":'
	length = PRINT_NAME_PADD + len(col)
	name = getattr(cls, '__name__', str(cls)) + col
	mut_type = 'Immutable' if is_immutable(cls, *cls_args) else 'Mutable'
	if PRINT_OBJ_SIZE:
		if cls is None:
			size = sys.getsizeof(None)
		else:
			size = sys.getsizeof(cls(*cls_args))
	else:
		size = -1
	print(f'Type "{name:{length}s} {mut_type}' + (f' (Size: {size})' if size >= 0 else ''))


def is_immutable(cls, *cls_args) -> bool:
	""" check if `cls` state cannot be modified after it is created """
	if cls is None: return True
	return cls(*cls_args) is cls(*cls_args)


def is_mutable(cls, *cls_args) -> bool:
	""" check if `cls` state can be modified after it is created """
	if cls is None: return False
	return not (cls(*cls_args) is cls(*cls_args))


if __name__ == '__main__':
	raise SystemExit(main())

