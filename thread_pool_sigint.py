import concurrent.futures as ft
import signal
import threading as th
import time


def main() -> int:
	""" Main - Runs threads in a thread pool, has stop `SIGINT` event Ctrl+C """
	print('Starting ...\n', end='', flush=True)

	functions_count = 3
	function_timeout = 0.5
	signal_timeout = 0.5

	functions = [
		(function_main_run, i+1, function_timeout)
		for i in range(functions_count)]

	# Run
	Runner.run(*functions, signal_timeout=signal_timeout)

	print('Exiting ...\n', end='', flush=True)
	return 0


def function_main_run(idx: int, function_timeout: float = 1.0):
	""" Print function for each `function_timeout` seconds timeout """
	frame_num = 0
	timeout = max(0.1, function_timeout)
	while Runner.is_running():
		frame_num += 1
		print(f'[{idx}] Runner: {frame_num}\n', end='', flush=True)
		time.sleep(timeout)


class Runner:
	""" Run a thread with an inner thread pool """
	running = False
	main_thread = None
	thread_pool = None

	@classmethod
	def is_running(cls) -> bool:
		""" Check if main thread is running """
		return cls.running is True

	@classmethod
	def stop(cls):
		""" Stop main thread and thread pool """
		cls.running = False
		if cls.thread_pool is not None:
			cls.thread_pool.shutdown()
			cls.thread_pool = None
		if cls.main_thread is not None:
			cls.main_thread.join(0)
			cls.main_thread = None

	@classmethod
	def register_sigint(cls):
		def signal_interrupt(*args):
			print('[SIGINT] Pressed: Ctrl+C\n', end='', flush=True)
			cls.stop()
			signal.signal(signal.SIGINT, signal.SIG_DFL)
		signal.signal(signal.SIGINT, signal_interrupt)

	@classmethod
	def run(cls, *functions: list | tuple, signal_timeout: float = 0.5):
		""" Run functions in a thread pool, exit with Ctrl+C """
		functions_count = len(functions)
		if functions_count == 0:
			print('WARNING: No functions provided, will not run any Threads!\n', end='', flush=True)
			return

		def main_thread():
			cls.thread_pool = ft.ThreadPoolExecutor(functions_count)
			for fn in functions:
				cls.thread_pool.submit(*fn)

		print(f'Running {functions_count} threads in a pool, exit with Ctrl+C...\n', end='', flush=True)

		cls.register_sigint()
		cls.running = True

		cls.main_thread = th.Thread(target=main_thread)
		cls.main_thread.start()

		timeout = max(0.1, signal_timeout)
		while cls.is_running():
			time.sleep(timeout)


if __name__ == '__main__':
	raise SystemExit(main())
