# -*- coding: utf-8 -*-

#AdList Sanitizer 0.1b#
#by M-A.Sc#
#Slow and dirty but multiplatform ;)#

# There's a bunch of Adlists floating around... With this script you can
# download multiple Adlists (lists.txt), filter and extract valid domains and subdomains entries,
# delete duplicates and specific domains and make yourself a nice customized and clean (sanitized:) AdList

import os
import requests
import re
from concurrent.futures import ThreadPoolExecutor

# parallel downloads
max_concurrent_downloads = 4

# AdList URLs
url_file = 'lists.txt'

# make dir if it doesnt exist
if not os.path.exists('download'):
    os.makedirs('download')

# download-function
def download_file(url):
    filename = url.split('/')[-1]
    filepath = os.path.join('download', filename)
    response = requests.get(url)
    if response.status_code == 200:
        with open(filepath, 'wb') as file:
            file.write(response.content)
        file_size = os.path.getsize(filepath)
        num_entries = len(response.content.decode().splitlines())
        print(f'{filename} was downloaded. Size: {file_size} Bytes, Number of Domains: {num_entries}')
    else:
        print(f'Error trying to download {filename}. Errorcode: {response.status_code}')

# multi download
def download_files(urls):
    with ThreadPoolExecutor(max_workers=max_concurrent_downloads) as executor:
        executor.map(download_file, urls)

# merge lists
def merge_files():
    files = os.listdir('download')
    merged_content = ''
    for file in files:
        filepath = os.path.join('download', file)
        with open(filepath, 'r') as f:
            file_content = f.read()
            merged_content += file_content
    with open('master.txt', 'w') as f:
        f.write(merged_content)
    print('Adlists got merged into master.txt')

# Remove duplicates
def remove_duplicates(input_list):
    return list(set(input_list))

# delete temporary data function
def delete_files():
    # delete download dir
    if os.path.exists('download'):
        for file in os.listdir('download'):
            file_path = os.path.join('download', file)
            os.remove(file_path)
        os.rmdir('download')
        print(" Folder download got deleted.")

    # delete temp .txt
    if os.path.exists('output.txt'):
        os.remove('output.txt')
        print("'output.txt' got deleted.")
    if os.path.exists('master.txt'):
        os.remove('master.txt')
        print("'master.txt' got deleted.")

# Statistics and output
def display_entry_stats():
    print(f"master.txt has {len(function_list)} Number of Rules.")


# main
if os.path.exists(url_file):
    with open(url_file, 'r') as file:
        urls = [line.strip() for line in file.readlines() if line.strip()]
        download_files(urls)
    merge_files()

    # put domain names into output.txt
    output_file_path = 'output.txt'

    with open("master.txt", "r") as master:
        function_list = remove_duplicated(master.readlines())

    sanity_file_path = 'sanity.txt'

    with open(sanity_file_path, 'w') as sanity_file:
        sanity_file.write("! Title: Nils Filter\n! Description: Merge of some good filters to make a better filter list.\n! Version: 1.0\n! Expires: 2 hours\n! Homepage: https://github.com/nilsbriggen/AdList-Creator/\n")
        for functions in function_list:
            sanity_file.write(functions + '\n')

    display_entry_stats()
else:
    print(f'Can not find "{url_file}"')
