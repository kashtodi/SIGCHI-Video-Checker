# SIGCHI Video Checker
Verify video and subtitle files for compliance
## By Kashyap Todi. www.kashyaptodi.com

## Requirements:
* Python (3.6 or later)
* FFMPEG (https://www.ffmpeg.org)

## How to use:

1. **Before running the check_format.py script**: Prepare a folder containing all video and subtitle files. Do not include any other files, or any sub-folders.
2. **Run the script via terminal/command-line**:
To execute the checker, include the folder path (relative or absolute) as a command-line argument
`python3 check_format.py path/to/folder`
The default value for time limit is 15 minutes, with a 30 second tolerance. 
Optionally, you can specify the `time limit` for videos (in minutes), and a `tolerance` (in seconds).  For example, set time limit to 20.0 minutes and tolerance to 45 seconds:
`python3 check_format.py path/to/folder -t 20.0 -d 45`
3. **Generated reports**: Once the script completes checking the folder, it generates two reports (JSON format), and prints out their location. The `per-category-report.json` file summarises all submissions by categories of issues, and the `per-submission-report.json` lists out all issues (if any) for each submission.



