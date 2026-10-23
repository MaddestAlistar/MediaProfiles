#!/usr/bin/env python3
"""Offline release-title preference scorer. NOT a Radarr/Sonarr import file."""
import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def detect(title):
    s = title.lower()
    match = lambda pat: re.search(pat, s) is not None
    if match(r'(?:2160p|4k|uhd)') and match(r'remux'):
        base = 'uhd-remux'
    elif match(r'1080p') and match(r'remux'):
        base = '1080p-remux'
    elif match(r'(?:2160p|4k|uhd)') and match(r'web[ ._-]?dl'):
        base = '2160p-webdl'
    elif match(r'(?:2160p|4k|uhd)') and match(r'web[ ._-]?rip'):
        base = '2160p-webrip'
    elif match(r'1080p') and match(r'blu[ ._-]?ray|bdrip'):
        base = '1080p-bluray'
    elif match(r'1080p') and match(r'web[ ._-]?(?:dl|rip)'):
        base = '1080p-webdl'
    elif match(r'720p'):
        base = '720p'
    else:
        base = 'unknown'
    flags = {
        'dolby-vision': match(r'(?<![a-z])(?:dv|dolby[ ._-]?vision)(?![a-z])'),
        'hdr10': match(r'hdr10(?:\+)?|\bhdr\b'),
        'atmos': match(r'atmos'),
        'truehd': match(r'true[ ._-]?hd'),
        'dts-hd-ma': match(r'dts[ ._-]?hd[ ._-]?(?:ma|master)'),
        'hevc': match(r'hevc|h[ ._-]?265|x265'),
        '10bit': match(r'10[ ._-]?bit'),
        'cam': match(r'(?<![a-z])cam(?![a-z])'),
        'telesync': match(r'(?<![a-z])(?:ts|telesync)(?![a-z])')
    }
    return base, flags

def score(release, profile):
    title = release['title'] if isinstance(release, dict) else release
    gb = release.get('size_gb') if isinstance(release, dict) else None
    base, flags = detect(title)
    points = profile['base'].get(base, 0)
    parts = [('quality:'+base, points)]
    for k, val in profile['bonus'].items():
        if flags.get(k):
            points += val
            parts.append((k, val))
    for k, val in profile['penalties'].items():
        if flags.get(k):
            points += val
            parts.append((k, val))
    limit = profile.get('maxGB',0)
    if limit and gb is not None and gb > limit:
        points -= 650
        parts.append(('over-size-limit', -650))
    return {'title':title, 'size_gb':gb, 'score':points, 'matched':parts}

def main():
    ap=argparse.ArgumentParser(description='Compare release names using LiangYou preferences.')
    ap.add_argument('--profile',choices=['balanced-4k','storage-saver','remux-first'],default='balanced-4k')
    ap.add_argument('--file',default=str(ROOT/'examples'/'releases.json'),help='JSON array of objects with title and optional size_gb')
    opts=ap.parse_args()
    profile=json.loads((ROOT/'profiles'/f'{opts.profile}.json').read_text(encoding='utf-8'))
    releases=json.loads(Path(opts.file).read_text(encoding='utf-8'))
    for r in sorted((score(x,profile) for x in releases),key=lambda x:-x['score']):
        print(f"{r['score']:>5} | {r['size_gb'] or '?':>5} GB | {r['title']}")
        print("      "+", ".join(f"{key}:{points:+}" for key,points in r['matched']))
if __name__=='__main__':
    main()
