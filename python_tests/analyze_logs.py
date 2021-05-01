import json
import os
import argparse
import cfusdlog
import statistics as st
import numpy as np
import matplotlib.pyplot as plt

LOG_PATH = os.path.join('decoded', 'log00.json')


def analyze_data(data_dict):
    before_rngNum = data_dict['logBefore']['rngNum']
    after_timestamps = data_dict['logAfter']['timestamp']
    skipped_rngNum = data_dict['logSkipped']['rngNum']

    time_shifts = [next_t - t for (t,next_t) in zip(after_timestamps, after_timestamps[1:])]

    mean_shift = st.mean(time_shifts)
    std_shift = st.stdev(time_shifts)

    # An "interface" to matplotlib.axes.Axes.hist() method
    n, bins, patches = plt.hist(time_shifts, bins=100, color='#0504aa',
                                alpha=0.7, rwidth=0.85)
    plt.grid(axis='y', alpha=0.75)
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.title('Histogram of time shifts')
    maxfreq = n.max()
    # Set a clean upper y-axis limit.
    plt.ylim(ymax=np.ceil(maxfreq / 10) * 10 if maxfreq % 10 else maxfreq + 10)
    plt.show()



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

    analyze_data(logData)

if __name__ == '__main__':
    main()
