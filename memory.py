import ctypes

import win32process

PROCESS_ALL_ACCESS = 0x1F0FFF

# Find the handle to the osu!.exe process
hWnd = ctypes.windll.user32.FindWindowW(None, "osu!")

# Get the process ID for osu!.exe
pid = win32process.GetWindowThreadProcessId(hWnd)[1]

# Open a handle to the process
h_process = ctypes.windll.kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)

# Allocate memory in the process
allocation = ctypes.windll.kernel32.VirtualAllocEx(
    h_process, 0, 0x1000, 0x1000, 0x40
)

# Read memory from the process
buffer = ctypes.create_string_buffer(b"\x48\x83\xF8\x04\x73\x1E")
bytes_read = ctypes.c_size_t()
ctypes.windll.kernel32.ReadProcessMemory(
    h_process, allocation, buffer, len(buffer), ctypes.byref(bytes_read)
)

# Print the memory contents
print("Memory contents:", buffer.value)

# Free the memory allocation
ctypes.windll.kernel32.VirtualFreeEx(h_process, allocation, 0, 0x8000)

# Close the handle to the process
ctypes.windll.kernel32.CloseHandle(h_process)
