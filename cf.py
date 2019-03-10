""" Classify an image with TensorFlow Lite - Pretrained Inception v4 model """
import argparse
import json
import os
import os.path
import socket
import time
import uuid
from time import gmtime, strftime
import datetime
import psutil
from PIL import Image, ImageDraw, ImageFont
from edgetpu.classification.engine import ClassificationEngine
from font_fredoka_one import FredokaOne
from inky import InkyPHAT
import socket
import minifiutil


# Function to read labels from text files.
def ReadLabelFile(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    ret = {}
    for line in lines:
        pair = line.strip().split(maxsplit=1)
        ret[int(pair[0])] = pair[1].strip()
    return ret


def main():
    try:
        # yyyy-mm-dd hh:mm:ss
        currenttime = strftime("%Y-%m-%d %H:%M:%S", gmtime())

        # Write text with weather values to the canvas
        inkydatetime = strftime("%d/%m %H:%M")

        # IoT Host Name
        host = os.uname()[1]

        # - start timing
        starttime = datetime.datetime.now().strftime('%m/%d/%Y %H:%M:%S')
        start = time.time()

        # Ip address
        ipaddress = minifiutil.IP_address()

        parser = argparse.ArgumentParser()
        parser.add_argument(
            '--image', help='File path of the image to be recognized.', required=True)
        args = parser.parse_args()

        # Prepare labels.
        labels = ReadLabelFile('/opt/demo/canned_models/imagenet_labels.txt')

        # Initialize engine.
        engine = ClassificationEngine('/opt/demo/canned_models/inception_v4_299_quant_edgetpu.tflite')

        # Run inference.
        img = Image.open(args.image)

        scores = {}
        kCount = 1

        # Iterate Inference Results
        for result in engine.ClassifyWithImage(img, top_k=5):
            scores['label_' + str(kCount)] = labels[result[0]]
            scores['score_' + str(kCount)] = "{:.2f}".format(result[1])
            kCount = kCount + 1

        # end of processing
        end = time.time()

        # Output JSON
        row = {}
        row.update(scores)
        uuid2 = '{0}_{1}'.format(strftime("%Y%m%d%H%M%S", gmtime()), uuid.uuid4())
        cpuTemp = int(float(minifiutil.getCPUtemperature()))
        usage = psutil.disk_usage("/")

        # Format Fields
        row['host'] = os.uname()[1]
        row['cputemp'] = str(round(cpuTemp, 2))
        row['ipaddress'] = str(ipaddress)
        row['endtime'] = '{0:.2f}'.format(end)
        row['runtime'] = '{0:.2f}'.format(end - start)
        row['systemtime'] = datetime.datetime.now().strftime('%m/%d/%Y %H:%M:%S')
        row['starttime'] = str(starttime)
        row['diskfree'] = "{:.1f}".format(float(usage.free) / 1024 / 1024)
        row['memory'] = str(psutil.virtual_memory().percent)
        row['uuid'] = str(uuid2)
        row['imagename'] = str(os.path.basename(args.image))

        # Output JSON
        json_string = json.dumps(row)
        print(json_string)

        # Current Minute for Display
        currentminute = int(datetime.datetime.now().minute)

        # Once an hour update display
        if currentminute == 1:
            # Set up the display
            inky_display = InkyPHAT("red")
            inky_display.set_border(inky_display.BLACK)

            # Create a new canvas to draw on
            # 212x104
            img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
            draw = ImageDraw.Draw(img)

            # Load the FredokaOne font
            font = ImageFont.truetype(FredokaOne, 18)

            # draw data
            draw.text((0, 0), "{}".format(row['imagename']), inky_display.RED, font=font)
            draw.text((0, 22), "{}".format(row['ipaddress']), inky_display.RED, font=font)
            draw.text((0, 44), "{}".format(row['label_1']), inky_display.RED, font=font)
            draw.text((0, 66), "{}".format(row['systemtime']), inky_display.RED, font=font)

            # Display the data on Inky pHAT
            inky_display.set_image(img)
            inky_display.show()

    except:
        print("Fail to send.")


if __name__ == '__main__':
    main()
