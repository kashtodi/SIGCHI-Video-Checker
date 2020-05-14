# Kashyap Todi. 13 May, 2020.
# Script to check a folder containing video and subtitle files for compliance to SIGCHI requirements.
# Before running the script, create a folder with all video and subtitle files (no sub-folders or other files)
# Include the path to this folder as the argument
# Optionally, include a time limit (and additional tolerance) for checking if videos are within the given limit
# The script generates 2 report files (JSON format), located in the present working directory.

import os
import glob
import json
import sys
import subprocess
import argparse

pwd = os.getcwd()
if len(sys.argv) == 1:
    raise Exception("Missing 1 argument - path to folder containing videos and subtitles")

if not os.path.isdir(sys.argv[1]):
    raise Exception("Argument #1 should be path to a directory")

# Change to videos directory
os.chdir(sys.argv[1])

parser = argparse.ArgumentParser()
parser.add_argument("--timelimit", "-t", help="Max. duration of videos (in minutes)", default="15")
parser.add_argument("--tolerance", "-d", help="Tolerance for exceeding max. duration (in seconds)", default="30")
args = parser.parse_args()

max_duration = args.timelimit
duration_tolerance = args.tolerance

# Return duration (in seconds)
def get_length(filename):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    return float(result.stdout)
    

# Get file names in directory
all_files = glob.glob("*.*")
srt_files = glob.glob("*.srt")
sbv_files = glob.glob("*.sbv")
txt_files = glob.glob("*.txt")
zip_files = glob.glob("*.zip")
xml_files = glob.glob("*.xml")
# Possible subtitle files (srt, sbv, txt, zip, xml)
subtitle_files = srt_files + sbv_files + txt_files + zip_files + xml_files
video_files = [f for f in all_files if f not in subtitle_files]
invalid_files = {}
invalid_format = {}
over_time_limit = {}
no_subtitles = []
invalid_subtitles = {}
good_files = []

# Check video files, and corresponding subtitle files. The script expects video and subtitle files to have the same name (e.g. PCS ID, DOI, etc.)
for file in video_files:
    ext = os.path.splitext(file)[-1].lower()
    filename = os.path.splitext(file)[0].lower()
    if ext == ".mp4":
        duration = get_length(file)
        # Check if duration under limit
        if (duration > max_duration + duration_tolerance):
            over_time_limit[file] = round(duration - max_duration)
        else:
            srt_file = [s for s in srt_files if filename + "." in s]
            if len(srt_file) > 0 :
                good_files.append(file) # Perfect submission
    # Not an mp4 file
    if ext != ".mp4": invalid_format[file] = ext

    subtitle_file = [s for s in subtitle_files if filename + "." in s]
    if len(subtitle_file) == 0 : 
        no_subtitles.append(file) # Subtitles missing
        continue
    srt_file = [s for s in srt_files if filename + "." in s]
    if len(srt_file) == 0: invalid_subtitles[file] = os.path.splitext(subtitle_file[0])[-1] # Not an SRT file

invalid_files = {"Wrong video format":invalid_format, "No subtitles": no_subtitles, "Wrong subtitle format":invalid_subtitles, "Over time limit": over_time_limit}

os.chdir(pwd)

# Create a category-wise report 
with open('per-category-report.json', 'w') as fp:
    json.dump(invalid_files, fp, indent = 2)

reports = {}

# Create a submission-wise report
for file in video_files:
    ext = os.path.splitext(file)[-1].lower()
    filename = os.path.splitext(file)[0].lower()
    reports[filename] = []
    if file in over_time_limit.keys():
        reports[filename].append("Over time limit by " + str(over_time_limit[file]) + " seconds")
    if file in invalid_format.keys():
        reports[filename].append("Wrong video format (" + invalid_format[file].upper() +") - MP4 file required")
    if file in no_subtitles:
        reports[filename].append("No subtitles - SRT file required")
    if file in invalid_subtitles.keys():
        reports[filename].append("Wrong subtitle format (" + invalid_subtitles[file].upper() + ") - SRT file required")
    if file in good_files: reports[filename] = ["No issues found"]


with open('per-submission-report.json', 'w') as fp:
    json.dump(reports, fp, indent = 2)

print("Reports available at " + pwd)