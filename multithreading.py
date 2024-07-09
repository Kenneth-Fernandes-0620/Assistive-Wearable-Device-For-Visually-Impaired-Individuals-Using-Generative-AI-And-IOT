import threading

def worker():
  """Function to be executed in a separate thread."""
  print("Running in a separate thread!")
  # Perform some work here

# Create a thread object
thread = threading.Thread(target=worker)
thread2 = threading.Thread(target=worker)

# Start the thread
thread.start()
thread2.start()

# The main thread continues execution here
print("Main thread doing something else...")
