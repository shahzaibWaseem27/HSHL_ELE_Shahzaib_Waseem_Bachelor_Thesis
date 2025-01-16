# pulse_sensor.py

from machine import ADC, Pin
from utime import ticks_ms, ticks_diff, sleep_ms

# Initialize the ADC for the pulse sensor
PULSE_SENSOR_PIN = 28  # Adjust the pin based on your setup
pulse_sensor = ADC(Pin(PULSE_SENSOR_PIN))

# Default sampling and configuration parameters
SAMPLING_INTERVAL = 10  # Sampling interval in milliseconds
WINDOW_SIZE = 5         # Moving average window size
THRESHOLD_K = 1.5       # Threshold multiplier for standard deviation
TIMEOUT_MS = 5000       # Timeout for collecting valid samples
UNCOVERED_VALUE = 65535 # Value indicating no finger is on the sensor

def collect_samples(num_samples):
    """
    Collect samples from the pulse sensor, ensuring valid data.

    Args:
        num_samples (int): Number of valid samples to collect.

    Returns:
        list: Collected samples (list of ADC values).
    """
    samples = []
    start_time = ticks_ms()

    while len(samples) < num_samples:
        if ticks_diff(ticks_ms(), start_time) > TIMEOUT_MS:
            print(f"Timeout reached. Collected {len(samples)} valid samples.")
            break

        value = pulse_sensor.read_u16()

        # Skip if no finger is detected
        if value >= UNCOVERED_VALUE:
            print("No finger detected on the sensor. Skipping sample.")
            continue

        samples.append(value)
        sleep_ms(SAMPLING_INTERVAL)

    if len(samples) == 0:
        print("No valid samples collected. Ensure the finger is placed on the sensor.")
    return samples

def moving_average(samples, window_size):
    """
    Apply a moving average filter to the samples.

    Args:
        samples (list): Raw ADC samples.
        window_size (int): Size of the moving average window.

    Returns:
        list: Smoothed samples.
    """
    if len(samples) < window_size:
        return samples  # Not enough data for moving average
    return [sum(samples[i:i + window_size]) / window_size for i in range(len(samples) - window_size + 1)]

def calculate_threshold(filtered_samples, k):
    """
    Calculate a dynamic threshold using mean and standard deviation.

    Args:
        filtered_samples (list): Filtered ADC values.
        k (float): Multiplier for standard deviation.

    Returns:
        float: Dynamic threshold value.
    """
    mean_value = sum(filtered_samples) / len(filtered_samples)
    squared_diffs = [(x - mean_value) ** 2 for x in filtered_samples]
    std_dev = (sum(squared_diffs) / len(filtered_samples)) ** 0.5
    return mean_value + k * std_dev

def detect_peaks(filtered_samples, threshold):
    """
    Detect peaks in the filtered samples.

    Args:
        filtered_samples (list): Filtered ADC values.
        threshold (float): Dynamic threshold value.

    Returns:
        list: Indices of detected peaks.
    """
    peaks = []
    for idx in range(1, len(filtered_samples) - 1):  # Avoid first and last indices
        if (
            filtered_samples[idx] > threshold and
            filtered_samples[idx] > filtered_samples[idx - 1] and
            filtered_samples[idx] > filtered_samples[idx + 1]
        ):
            peaks.append(idx)
    return peaks

def calculate_heart_rate(peaks, sampling_interval):
    """
    Calculate heart rate in BPM using detected peaks.

    Args:
        peaks (list): Indices of detected peaks.
        sampling_interval (int): Sampling interval in milliseconds.

    Returns:
        int: Heart rate in BPM, or None if not enough peaks are detected.
    """
    if len(peaks) < 2:
        print("Not enough peaks detected to calculate heart rate.")
        return None

    intervals = [(peaks[i] - peaks[i - 1]) * sampling_interval for i in range(1, len(peaks))]
    avg_interval = sum(intervals) / len(intervals)
    return round(60000 / avg_interval)  # Convert to BPM

def get_bpm(num_samples=100, window_size=5, threshold_k=1.5):
    """
    Calculate BPM from the pulse sensor.

    Args:
        num_samples (int): Number of valid samples to collect.
        window_size (int): Moving average window size.
        threshold_k (float): Threshold multiplier for peak detection.

    Returns:
        int: Heart rate in BPM, or None if heart rate cannot be determined.
    """
    # Collect valid samples
    raw_samples = collect_samples(num_samples)
    if not raw_samples:
        return None  # No valid samples collected

    # Apply moving average filter
    filtered_samples = moving_average(raw_samples, window_size)

    # Calculate dynamic threshold
    threshold = calculate_threshold(filtered_samples, threshold_k)

    # Detect peaks
    peaks = detect_peaks(filtered_samples, threshold)

    # Calculate heart rate
    bpm = calculate_heart_rate(peaks, SAMPLING_INTERVAL)
    return bpm
