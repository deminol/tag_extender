import os
import mutagen
import argparse
from datetime import datetime as dt
import dicttoxml

# script argument parser
parser = argparse.ArgumentParser(description='Tag extender for XML-feed')
parser.add_argument('-i', '--input', help="input file path" ) 
parser.add_argument('-d', '--folder', help="input folder") 
parser.add_argument('-o', '--output', help="output xml file" )
args = parser.parse_args()

# get tag data
def get_tag(media, tag, def_tag=None):
    return media.tags.getall(tag)[0].text[0] if len(media.tags.getall(tag)) else def_tag

# get info from media file
def get_info(file):
    media = mutagen.File(file)
    return dict(title    = get_tag(media, 'TIT2'),
                artist   = get_tag(media, 'TPE1'),
                album    = get_tag(media, 'TALB'),
                duration = dt.utcfromtimestamp(media.info.length).strftime('%H:%M:%S')
    )

# convert dict to xml
def convert(data):
    return dicttoxml.dicttoxml(data, custom_root='item', attr_type=False)

# main routine
def main(args):
    # single file
    if args.input:
        data = convert(get_info(args.input))

    # or folder process
    elif args.folder:
        # data = [convert(get_info(f)) for f in os.listdir(args.folder)]
        data = convert([get_info(os.path.join(args.folder, f)) for f in os.listdir(args.folder)])

    # or nothing
    else:
        print("Nothing done. You must set --input or --folder")
        exit(0)

    # output to file
    if args.output:
        with open(args.output, 'bw') as file:
            print("File {} ({} bytes) saved".format(args.output, file.write(data)))

    # or to STDOUT
    else:
        print(data)


if __name__ == "__main__":
    # start main routine
    main(args)