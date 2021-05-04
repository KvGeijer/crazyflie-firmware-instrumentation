import json
import os
import argparse
import cfusdlog
import statistics as st
import numpy as np
import matplotlib.pyplot as plt
import csv

LOG_PATH = os.path.join('decoded', 'log00.json')


def analyze_data(filename, data_dict, remove_outliers=False):
    if filename[3] == "P":
        controller = "PID"
    elif filename[3] == "I":
        controller = "INDI"
    elif filename[3] == 'M':
        controller = 'Mellinger'
    else:
        raise ValueError

    if "Square" in filename:
        pattern = "Square"
    else:
        pattern = "Hover"



    after_timestamps = remove_extra_sec(data_dict['logAfter']['timestamp'])

    time_shifts = [next_t - t for (t,next_t) in zip(after_timestamps, after_timestamps[1:])]
    mean_shift = st.mean(time_shifts)

    if remove_outliers:
        time_shifts = [t for t in time_shifts if abs(t-mean_shift)<0.02]

    mean_shift = st.mean(time_shifts)
    std_shift = st.stdev(time_shifts)

    if max(time_shifts) < 6.5:
        plt_range = None
    else:
        plt_range = (0, 6.5)

    # An "interface" to matplotlib.axes.Axes.hist() method
    n, bins, patches = plt.hist(time_shifts, bins=120, color='#0504aa',
                                alpha=0.7, rwidth=0.85, range=plt_range)

    plt.text(0.994, n.max()/1.5, f"mean = {round(mean_shift,3)}\nstdev = {round(std_shift,3)}")
    plt.grid(axis='y', alpha=0.75)
    plt.xlabel('Time (ms)')
    plt.ylabel('Frequency')
    plt.title(f'Time shifts histogram: {controller}, {pattern}')
    maxfreq = n.max()
    # Set a clean upper y-axis limit.
    plt.ylim(ymax=np.ceil(maxfreq / 10) * 10 if maxfreq % 10 else maxfreq + 10)
    plt.show()


def save_after_timestamps(filename, data_dict):
    after_timestamps = remove_extra_sec(data_dict['logAfter']['timestamp'])
    time_shifts = [next_t - t for (t, next_t) in zip(after_timestamps, after_timestamps[1:])]

    name = filename + ".csv"
    with open(os.path.join("decoded", name), 'w') as f:
        writer = csv.writer(f)
        writer.writerow(time_shifts)


def remove_extra_sec(series, sec=5):
    first = series[0]
    last = series[-1]

    start_cutoff = first + sec*1000
    stop_cutoff = last + sec*1000

    # Ineffective, could use itertools
    result = []
    for value in series:
        if value < start_cutoff:
            continue
        elif value > stop_cutoff:
            break

        result.append(value)

    return result

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()

    file_path = os.path.join("raw_logs",args.filename)
    if not os.path.exists(file_path):
        file_path = os.path.join("decoded",args.filename)

    if ".json" not in args.filename:
        logData = cfusdlog.decode(file_path)
    else:
        with open(file_path, 'r') as f:
            logData = json.load(f)

    save_after_timestamps(args.filename, logData)
    analyze_data(args.filename, logData, True)

if __name__ == '__main__':
    main()
