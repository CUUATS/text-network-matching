# This create an network object
from cuuats.datamodel import feature_class_factory as factory
from cuuats.datamodel import D
import os
from collections import defaultdict
import pandas as pd

class Network(object):

    def __init__(self, network_id, feature_source):
        self._id = network_id
        self._scr = feature_source

        self._index = defaultdict(list)
        self.build_network()

    def __repr__(self):
        return '<Network %s>' % (str(self._id),)

    def build_network(self):
        APPROACH_NAME = "PCD.PCDQC.StreetIntersectionApproach"
        SEGMENT_NAME = "PCD.PCDQC.StreetSegment"
        streetintersectionapproach = "pcd.pcdqc.streetintersectionapproach_set"
        self._approach = factory(self._scr, follow_relationships=True)
        self._segment = self._approach.related_classes[SEGMENT_NAME]
        # self._intersection = self._approach.related_classes[INTERSECTION_NAME]

        seg_dict = {}
        d_dict = defaultdict(list)
        for segment in self._segment.objects.filter(Name='W Nevada St'):
            seg_name = self._remove_direction(segment.Name).upper()
            sid = int(segment.SegmentID)
            segment_list = []
            for approach in getattr(segment, streetintersectionapproach):
                d = self._chg_dir(approach.LegDir)
                dir_dict = {}
                for r_approach in getattr(approach.IntersectionID, streetintersectionapproach):
                    r_seg_name = self._remove_direction(r_approach.SegmentID.Name.upper())
                    if r_seg_name != seg_name:
                        dir_dict[r_seg_name] = d
                        dir_dict['id'] = sid
                d_dict[seg_name].append(dir_dict)
        # seg_dict[seg_name] = dir_dict
        import pdb; pdb.set_trace()

    def _chg_dir(self, direction):
        if direction == "E":
            return "W"
        elif direction == "W":
            return "E"
        elif direction == "S":
            return "N"
        elif direction == "N":
            return "S"

    def _remove_direction(self, str):
        if str is not None:
            replacement_list = ["W ", "S ", "E ", "N "]
            for r in replacement_list:
                if str[0:2] == r:
                    str = str[2: len(str)]
            return str



        # self._index = \
        #     [(f.Name, [f.SegmentID, f.OBJECTID]) for f in self._feature.objects.filter(InUrbanizedArea=D('Yes'))]




def main():
    SDE_DB = r"C:\Connection\PCD_Edit_SN.sde"
    SEGMENT_NAME = "PCD.PCDQC.StreetIntersectionApproach"
    FC_PATH = os.path.join(SDE_DB, SEGMENT_NAME)
    a_net = Network("a_net", FC_PATH)

if __name__ == "__main__":
    main()
