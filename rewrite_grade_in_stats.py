import json
import xmljson
from lxml.etree import parse
import glob
import subprocess
import codecs
import os
import time
import re
from multiprocessing import Pool
from multiprocessing import Process

for path in glob.glob("/Users/okada-toshiki/Library/Preferences/StepMania 5/LocalProfiles/00000000/Stats.xml"):
    with open(path) as f:
        xmllines = f.readlines()
        xmlline_num = 0
        score = 0

        for xmlline in xmllines:
            if '</Grade>' in xmlline:
                score = int(re.sub(r'\D', '', xmllines[xmlline_num + 1]))
                print(score)
                if "Failed" not in xmlline:
                    if score == 1000000:
                        xmlline = "<Grade>Tier01</Grade>\n"
                    elif score <= 1000000 and score >= 990000:
                        xmlline = "<Grade>Tier02</Grade>\n"
                    elif score <= 9900000 and score >= 950000:
                        xmlline = "<Grade>Tier03</Grade>\n"
                    elif score <= 9500000 and score >= 900000:
                        xmlline = "<Grade>Tier04</Grade>\n"
                    elif score <= 9000000 and score >= 890000:
                        xmlline = "<Grade>Tier05</Grade>\n"
                    elif score <= 8900000 and score >= 850000:
                        xmlline = "<Grade>Tier06</Grade>\n"
                    elif score <= 8500000 and score >= 800000:
                        xmlline = "<Grade>Tier07</Grade>\n"
                    elif score <= 8000000 and score >= 790000:
                        xmlline = "<Grade>Tier08</Grade>\n"
                    elif score <= 7900000 and score >= 750000:
                        xmlline = "<Grade>Tier09</Grade>\n"
                    elif score <= 7500000 and score >= 700000:
                        xmlline = "<Grade>Tier10</Grade>\n"
                    elif score <= 7000000 and score >= 690000:
                        xmlline = "<Grade>Tier11</Grade>\n"
                    elif score <= 6900000 and score >= 650000:
                        xmlline = "<Grade>Tier12</Grade>\n"
                    elif score <= 6500000 and score >= 600000:
                        xmlline = "<Grade>Tier13</Grade>\n"
                    elif score <= 6000000 and score >= 590000:
                        xmlline = "<Grade>Tier14</Grade>\n"
                    elif score <= 5900000 and score >= 550000:
                        xmlline = "<Grade>Tier15</Grade>\n"
                    else:
                        xmlline = "<Grade>Tier16</Grade>\n"

            xmlline_num += 1
            print(xmlline, file=codecs.open(
                "/Users/okada-toshiki/Library/Preferences/StepMania 5/LocalProfiles/00000000/Stats_new.xml", 'a', 'utf-8'), end='')
