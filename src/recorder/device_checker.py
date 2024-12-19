import sounddevice as sd

def check_audio_devices(target_device=None):
    """
    Check and list available audio devices, and optionally verify if a target device is available.

    Parameters:
        target_device (str, optional): Name of the device to check. Default is None.

    Returns:
        dict: A dictionary containing available devices and the status of the target device.
    """
    result = {
        "available_devices": [],
        "target_device_found": None
    }

    # List all available devices
    device_list = sd.query_devices()
    result["available_devices"] = [device['name'] for device in device_list]

    if target_device:
        # Check if the target device is in the available devices
        result["target_device_found"] = target_device in result["available_devices"]

    return result

# Example usage
def main():
    target = "default"
    devices = check_audio_devices(target)
    print("Available Devices:")
    for idx, device in enumerate(devices["available_devices"], start=1):
        print(f"{idx}: {device}")

    if target:
        if devices["target_device_found"]:
            print(f"\nThe device '{target}' is available.")
        else:
            print(f"\nThe device '{target}' is not available.")

if __name__ == "__main__":
    main()

