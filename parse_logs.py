import os
import sys
import argparse
import re
import csv
from datetime import datetime, timezone
import pytz
import xlsxwriter

def main(arguments):

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('infile', help="Input file", type=argparse.FileType('r'))
    parser.add_argument('-o', '--outfile', help="Output file",
                        default=sys.stdout, type=argparse.FileType('w'))

    args = parser.parse_args(arguments)

    # Define field names.
    fieldnames = ['IP', 'Categories', 'Comment', 'ReportDate']
    # Begin CSV output.
    writer = csv.DictWriter(args.outfile, fieldnames=fieldnames)
    writer.writeheader()

     # Initialize empty list to hold addresses
    ipv4_addresses = list()

    for line in args.infile:
        # !! Match this format to your system's format.
        timestamp = "([a-zA-Z]+\s+[0-9]+ [0-9]+:[0-9]+:[0-9]+)"
        ipv4 = "([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})"
        comment = "(Invalid user [a-zA-Z0-9]+ from " + ipv4 + " port [0-9]+)"

        # The regex of the line we're looking for, built up from component regexps.
        combined_re = timestamp + " .* " + comment

        # Run the regexp.
        matches = re.findall(combined_re, line)
        # If this line is in the format we're looking for,
        if matches:
            # Pull the tuple out of the list.
            matches_flat = matches[0]

            # Remove duplicate addresses from the report.
            if matches_flat[2] not in ipv4_addresses:
                ipv4_addresses.append(matches_flat[2])
            else:
                continue

            ### !!! You may need to update this. ###
            # Parse log datetime to Python datetime object so we can update the timezone.
            # The format string should must your log files. Here we use the default in Debian/Redhat distros.
            attack_datetime = datetime.strptime(matches_flat[0], '%b %d %H:%M:%S')
            # Assume year is the current year.
            attack_datetime = attack_datetime.replace(datetime.now().year)
            # !! Set tzinfo to your system timezone using timezone.
            my_tz = pytz.timezone('America/New_York')
            attack_datetime = attack_datetime.replace(tzinfo=my_tz)

            # Format to ISO 8601 to make it universal and portable.
            attack_datetime_iso = attack_datetime.isoformat()

            # We'll add the categories column statically at this step.
            # Output as a CSV row.
            writer.writerow({
                'IP': matches_flat[2],
                'Categories': "18,22",
                'Comment': matches_flat[1],
                'ReportDate': attack_datetime_iso
            })

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))