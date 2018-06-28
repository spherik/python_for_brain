#!/usr/local/bin/python2
from cfflib import *
import sys
import getopt
import argparse

class Connectome:

    def __init__(self, filename):
        self.cff=load(filename)

    def PrintInfo(self):
        self.cff.print_summary()

    def WriteMetadata(self, output_path):
        metadatas = self.cff.get_connectome_metadata()
        for metadata in metadatas:
            metadata.load()
            metadata.tmpsrc = output_path+metadata.src # this is used by save_data
            util.save_data(metadata)

    def WriteNetworks(self,output_path):
        networks = self.cff.get_connectome_network()
        for network in networks:
            network.load()
            network.tmpsrc = output_path+network.src # this is used by save_data
            util.save_data(network)

    def WriteVolumes(self,output_path):
        volumes = self.cff.get_connectome_volume()
        for volume in volumes:
            volume.load()
            volume.tmpsrc = output_path+volume.src # this is used by save_data
            util.save_data(volume)

    def WriteTracks(self, output_path):
        tracks = self.cff.get_connectome_track()
        for track in tracks:
            track.load()
            track.tmpsrc = output_path+track.src # this is used by save_data
            util.save_data(track)

    def WriteSurfaces(self, output_path):
        surfaces = self.cff.get_connectome_surface()
        for surface in surfaces:
            surface.load()
            surface.tmpsrc = output_path+surface.src # this is used by save_data
            util.save_data(surface)

    def WriteDatas(self, output_path):
        datas = self.cff.get_connectome_data()
        for data in datas:
            data.load()
            data.tmpsrc = output_path+data.src # this is used by save_data
            util.save_data(data)

    def WriteFiles(self,output_path):
        # self.WriteMetadata(output_path)
        self.WriteNetworks(output_path)
        self.WriteVolumes(output_path)
        self.WriteTracks(output_path)
        self.WriteSurfaces(output_path)
        self.WriteDatas(output_path)

def main(argv):

    connectome = Connectome(argv.input)

    # Print contents
    connectome.PrintInfo()

    # Write all contents
    connectome.WriteFiles(argv.output)

    # Write only networks
    #connectome.WriteNetworks(argv.output)

    # Write only volumes
    #connectome.WriteVolumes(argv.output)

    # Write only tracks
    #connectome.WriteTracks(argv.output)

    # Write only surfaces
    #connectome.WriteSurfaces(argv.output)

    # Write only data
    #connectome.WriteDatas(argv.output)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input')
    parser.add_argument('-o', '--output')
    args = parser.parse_args()
    if args.input == None or args.output == None:
        print >>sys.stderr, "Usage: cffExtract.py -i input_file -o output_path"
        sys.exit(2)

    sys.exit(main(args))
