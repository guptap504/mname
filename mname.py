# Renaming MP3s using the metadata

import mutagen
import os
from argparse import ArgumentParser
import subprocess


def get_metadata(s):
    try:
        song_name = str(s['TIT2'])
    except:
        song_name = ''
    try:
        artist_name1 = str(s['TPE1']).encode('ascii')
    except:
        artist_name1 = ''
    try:
        artist_name2 = str(s['TPE2']).encode('ascii')
    except:
        artist_name2 = ''
    if len(artist_name1) > 0:
        artist_name = artist_name1.decode('ascii')
    elif len(artist_name2) > 0:
        artist_name = artist_name2.decode('ascii')
    else:
        artist_name = ''
    try:
        album_name = str(s['TALB'])
    except:
        album_name = ''
    return song_name, artist_name, album_name


def rename_words(song: str):
    sn = song.lower()
    words = []
    for word in sn.split():
        n_word = word[0].upper() + word[1:]
        words.append(n_word)
    return ' '.join(words)


def rename_mp3(location: str):
    try:
        os.chdir(location)
    except:
        print('Incorrect path!')
        return
    for song in os.listdir():
        if '.mp3' in song.lower():
            s = mutagen.File(song)
            s_n, a_n, alb_n = get_metadata(s)
            s_n += '.mp3'
            if len(s_n) == 0:
                s_n = song
            if len(a_n) == 0:
                a_n = 'Unknown'
            if len(alb_n) == 0:
                alb_n = 'Unknown'

            s_n = rename_words(s_n)
            a_n = rename_words(a_n)
            alb_n = rename_words(alb_n)

            subprocess.run(
                args=['mkdir', '-p', '{}/{}/{}'.format(location, a_n, alb_n)], check=True)
            subprocess.run(args=['mv', '{}/{}'.format(location, song),
                                 '{}/{}/{}/{}'.format(location, a_n, alb_n, s_n)], check=True)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('location', help='Location of MP3s', type=str)
    args = parser.parse_args()
    if args.location:
        rename_mp3(args.location)
    else:
        print('No location given!', parser.print_help(), sep='\n')
