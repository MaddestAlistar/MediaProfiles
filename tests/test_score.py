import json
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from score_releases import detect,score

class TitleScoring(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.profile=json.loads((ROOT/'profiles'/'balanced-4k.json').read_text(encoding='utf-8'))
    def test_remux(self):
        base,flags=detect('Film.2160p.UHD.BluRay.REMUX.DV.Atmos')
        self.assertEqual(base,'uhd-remux')
        self.assertTrue(flags['dolby-vision'])
        self.assertTrue(flags['atmos'])
    def test_webdl(self):
        self.assertEqual(detect('Film.2160p.WEB-DL.HEVC.10bit')[0],'2160p-webdl')
    def test_cam_penalty(self):
        self.assertLess(score('Movie.720p.CAM',self.profile)['score'],0)
    def test_hierarchy(self):
        remux=score('Film.2160p.REMUX',self.profile)['score']
        web=score('Film.2160p.WEB-DL',self.profile)['score']
        self.assertGreater(remux,web)
    def test_storage_limit(self):
        p=json.loads((ROOT/'profiles'/'storage-saver.json').read_text(encoding='utf-8'))
        self.assertLess(score({'title':'Film.2160p.REMUX','size_gb':60},p)['score'],score({'title':'Film.1080p.WEB-DL','size_gb':5},p)['score'])

if __name__=='__main__': unittest.main()
