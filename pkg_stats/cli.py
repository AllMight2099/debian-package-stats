import argparse
import requests
from bs4 import BeautifulSoup
import json 
from json.decoder import JSONDecodeError
import os
import gzip

def main() -> None:
    '''
    Entrypoint function

    Arguments:

    '''
    parser = argparse.ArgumentParser(
        description="Displays stats for debian packages of a particular architecture"
    )
    parser.add_argument(
        "arch", type=str,
        help="Input system architecture. Eg: arm, amd64, etc",
        default="all"
    )
    parser.add_argument(
        "-m", 
        "--mirror",
        type=str,
        default="http://ftp.uk.debian.org/debian/dists/stable/main/",
        help="Mirror link to fetch package information from. Defaults to debian's mirror"
    )
    parser.add_argument(
        "-i", 
        "--include-udeb", 
        help="Flag to include stats of udeb packages of the procided architecture", 
        action='store_true',
    )
    parser.add_argument(
        '-a', 
        '--all', 
        help="Finds package stats for all distributions",
        action="store_true"
    )
    parser.add_argument(
        '-n', 
        '--number',
        help="Input to displat top 'n' packages",
        default=10,
        type=int
    )
    
    args = parser.parse_args()
    arch = str.lower(args.arch)
    mirror = args.mirror
    udeb_flag = args.include_udeb
    all_flag = args.all
    n = args.number
    
    # file_path = read_json_lock(arch, udeb_flag)

    file_path = fetch_content_files(arch, mirror, udeb_flag)

    print_stats(file_path, udeb_flag, n)

    if not os.path.isdir('/var/tmp/pkg_stats'):
        os.makedirs('/var/tmp/pkg_stats')


def fetch_content_files(
    arch: str,
    mirror: str, 
    udeb: bool, 
) -> str:

    resp = requests.get(mirror)

    soup = BeautifulSoup(resp.content, 'html5lib')
    body = soup.prettify().splitlines()

    content_links = []

    file_link = ''
    for _ in body:
        temp = _.split()
        if temp[0]=='<a' and f'Contents-{arch}.gz' in temp[1]:
            file_link=mirror+'Contents-'+arch+'.gz'
            if udeb:
                file_link=mirror+'Contents-udeb-'+arch+'.gz'

    if file_link=='':
        raise Exception("Architecture not found")
    
    if udeb:
        output_zip_path = f'/var/tmp/pkg_stats/Content-udeb-{arch}.gz'
        output_file_path = f'/var/tmp/pkg_stats/Content-udeb-{arch}'
    else:
        output_zip_path = f'/var/tmp/pkg_stats/Content-{arch}.gz'
        output_file_path = f'/var/tmp/pkg_stats/Content-{arch}'
    
    print("Fetching data from "+file_link)
    print()
    data = requests.get(file_link)    
    open(output_zip_path, 'wb').write(data.content)
    with gzip.open(output_zip_path, 'rb') as temp:
        data = temp.read()
    with open(output_file_path, 'wb') as temp:
        temp.write(data)
    
    return output_file_path


def read_json_lock(
    arch: str,
    udeb: bool, 
) -> str:
    lock_file = {}
    if os.path.isfile('/var/tmp/pkg_stats/content_lock.json'):
        lock_file = open('/var/tmp/pkg_stats/content_lock.json').read()
    else:
        open('/var/tmp/pkg_stats/content_lock.json', 'w').close()
        lock_file = open('/var/tmp/pkg_stats/content_lock.json', 'r').read()
    try:
        lock_file = json.loads(lock_file)
    except JSONDecodeError:
        pass
    
    if arch in lock_file.keys():
        return True
    else:
        return False


def print_stats(
    file_path: str, 
    udeb: bool,
    n:int
    ) -> None:

    final_dict = {}

    data = open(file_path, 'r').readlines()

    for entry in data:
        package = entry.split()[1]
        # print(package)
        if package in final_dict:
            final_dict[package]+=1
        else:
            final_dict[package]=1
    count = 1
    sorted_values = sorted(final_dict.items(), key=lambda x:x[1], reverse=True)
    print(f"{'No.' : <10}{'Package Name' : <70}{'No. of files' : >10}")
    for i in range(n):
        print(f"{count : <10}{sorted_values[i][0] : <70}{sorted_values[i][1] : >10}")
        count+=1

