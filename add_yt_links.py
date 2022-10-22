import os
import re
from datetime import timedelta
import getopt
import sys

argument_list = sys.argv[1:]

# Options
options = "hd:"
long_options = ["help", "dir"]
base_directory = ""
try:
    arguments, values = getopt.getopt(argument_list, options, long_options)
    for current_argument, current_value in arguments:

        if current_argument in ("-h", "--pelp"):
            print("\n-----\nAdds a time-stamped youtube link to each section of your file example: \n\n"
                  "add_yt_links -d /my/directory/\n\n"
                  "Please be careful as this will recursively edit all files in this directory and add a youtube link.\n\n"
                  )
            exit()

        elif current_argument in ("-d", "--rid"):
            base_directory = current_value
            if '"' in base_directory:
                base_directory = base_directory.replace('"', "")


except getopt.error as err:
    # output error, and return with an error code
    print(str(err))

if not base_directory:
    print("Please provide a directory or pass the option -h")
    exit()
choice = input(
    f"\nWARNING\nThis will recursively edit all files in this directory and add a youtube link\n\n"
    f"Using: '{base_directory}'\nPlease confirm that this is correct by pressing 'y' and enter.\n\n")
if choice.lower() != 'y':
    exit()


files = []
for root, d_names, f_names in os.walk(base_directory):
    for f in f_names:
        if f.endswith('.md') or f.endswith('.txt'):
            files.append(os.path.join(root, f))


def get_youtunbe_link_in_file(file: str) -> str:
    """
    Finds the 1st youtube link in the file.
    :param file: filename
    :return: str, youtube link if exists.
    """
    with open(
            file
    ) as f:
        for line in f.readlines():
            match = re.search("(?P<url>https?://[^\s]+)", line)
            if match:
                if "youtube" in match.string:
                    if "\n" in match.string:
                        youtube_link = match.string.replace('\n', "")
                        if re.search("&t=[0-9]+s", youtube_link):
                            clean_youtube_link = re.sub("&t=[0-9]+s", '', youtube_link)
                            return clean_youtube_link
                        return youtube_link
                    break

    return ""


def get_time_ranges_in_file(file: str, regex_pattern: str) -> list:
    """
    Gets all the timestamps in the file in question.
    :param file: str, filename
    :param regex_pattern: str, regex pattern to match to get the timestamps.
    :return: list, of strings.
    """
    with open(
            file
    ) as f:
        time_ranges = re.findall(
            regex_pattern,
            f.read(),
            re.MULTILINE
        )
        print(f"Found {len(time_ranges)} timestamps")
        return time_ranges
    return []


def add_youtube_links(youtube_link: str, file: str, timestamp_delimiter: str, re_pattern: str) -> None:
    """
    Adds a timestamped youtube link to the each section.
    :param youtube_link: youtube url.
    :param file: filename of file in question.
    :param timestamp_delimiter: timestamp delimiter
    :param re_pattern: regex pattern to match
    :return:
    """
    time_ranges = get_time_ranges_in_file(file=file, regex_pattern=re_pattern)
    if len(time_ranges) < 2:
        print("Skipping because video is shorter than 1 min. ")
        return
    with open(
            file
    ) as f:
        file_content = f.read()

    for time_range in time_ranges:
        start_time, _ = time_range.split(timestamp_delimiter)
        seconds = timedelta(
            hours=int(start_time.split(':')[0]),
            minutes=int(start_time.split(':')[1]),
            seconds=int(start_time.split(':')[2].split('.')[0]),
        ).seconds
        file_content = file_content.replace(
            time_range,
            f"\n{youtube_link}&t={seconds}s\n{time_range}"
        )

    with open(
            file, 'w'

    ) as f:
        f.write(file_content)


def get_regex_pattern_and_timestamp_delimiter(file: str) -> (str, str,):
    """
    Returns the re pattern and timestamp delimiter.
    :param file: str, File path of the file in question.
    :return: (re_pattern: str, timestamp_delimter: str, )
    """
    re_format_a = r'[0-9][0-9]:[0-5][0-9]:[0-5][0-9]\.[0-9][0-9][0-9] --> [0-9][0-9]:[0-5][0-9]:[0-5][0-9]\.[0-9][0-9][0-9]'
    re_format_b = r'[0-9][0-9]:[0-5][0-9]:[0-5][0-9]\.[0-9][0-9][0-9] --\\> [0-9][0-9]:[0-5][0-9]:[0-5][0-9]\.[0-9][0-9][0-9]'
    delimiter_a = r'-->'
    delimiter_b = r'--\>'

    with open(
            file
    ) as f:
        for line in f.readlines():
            match_format_a = re.search(
                r'[0-9][0-9]:[0-5][0-9]:[0-5][0-9]\.[0-9][0-9][0-9] --> [0-9][0-9]:[0-5][0-9]:[0-5][0-9]\.[0-9][0-9][0-9]',
                line)
            match_format_b = re.search(
                r'[0-9][0-9]:[0-5][0-9]:[0-5][0-9]\.[0-9][0-9][0-9] --\\> [0-9][0-9]:[0-5][0-9]:[0-5][0-9]\.[0-9][0-9][0-9]',
                line)
            if match_format_a:
                return (
                    re_format_a,
                    delimiter_a,
                )
            elif match_format_b:
                return (
                    re_format_b,
                    delimiter_b,
                )


processed_files = 0
for file in files:

    # Build the full file path
    full_file_path = os.path.join(base_directory, file)
    print(f"Working on file: {full_file_path}")

    # Check the regex match and timestamp delimiter to use.
    try:
        re_pattern, timestamp_delimiter = get_regex_pattern_and_timestamp_delimiter(file=full_file_path)
    except:
        print(f"Skipping: {full_file_path}")
        continue

    try:
        youtube_link = get_youtunbe_link_in_file(file=full_file_path)
        if youtube_link:
            add_youtube_links(
                youtube_link=youtube_link,
                file=full_file_path,
                timestamp_delimiter=timestamp_delimiter,
                re_pattern=re_pattern
            )
    except PermissionError:
        continue
    processed_files += 1

print(f"Processed: {processed_files} files.")
