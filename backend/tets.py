import torch
print("CUDA available:", torch.cuda.is_available())
print("Current device:", torch.cuda.current_device() if torch.cuda.is_available() else "CPU only")
print("Device name:", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "CPU only")
