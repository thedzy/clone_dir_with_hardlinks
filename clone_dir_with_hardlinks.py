#!/usr/bin/env python3

"""
Script:	clone_dir_with_hardlinks.py
Date:	2020-02-01
Platform: MacOS/Linux
Description:
Clones a directory with hardlinks
"""
import os
import optparse


def main(source, target, warn, merge, follow_links, verbose):
    # Make sure paths are full absolute paths
    source = os.path.abspath(source)
    target = os.path.abspath(target)

    # Check source and target paths
    if not os.path.isdir(source):
        print('Source does not exist or is not a directory')
        exit()

    if os.path.exists(target):
        if os.path.isfile(target):
            print('Target cannot be a file')
            exit()
    else:
        os.makedirs(target)

    # Clean up if we are not merging
    if not merge:
        # Prompt to continue if not skipping warnings
        if warn:
            print('Continue? (y/n) ')
            proceed = None
            while proceed is None:
                answer = input().lower()[0]
                proceed = True if answer in ('y', 'n') else None

            if answer != 'y':
                print('Stopping')
                exit()
            else:
                if verbose > 1:
                    print('Continuing')

        # Clean out old directory and recreate
        for root, dirs, files in os.walk(target, followlinks=False, topdown=False):
            for file in files:
                if verbose > 2:
                    print('Removing {}'.format(os.path.join(root, file)))
                os.remove(os.path.join(root, file))
            os.rmdir(root)
        os.makedirs(target)

    # Loop through and recreate the directory structure and then link files
    for root, dirs, files in os.walk(source, followlinks=follow_links):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            dir_path = dir_path.replace(source, target, 1)
            os.makedirs(dir_path, exist_ok=True)

        for file in files:
            if file == '.DS_Store':
                continue
            org_file_path = os.path.join(root, file)
            new_file_path = org_file_path.replace(source, target, 1)
            if os.path.exists(new_file_path):
                if verbose > 1:
                    print('Skipping {}'.format(new_file_path))
            else:
                if verbose:
                    print('Linking  {} => {}'.format(new_file_path, org_file_path))
                try:
                    os.link(org_file_path, new_file_path)
                except FileExistsError:
                    continue

    if verbose:
        print('Exiting')


if __name__ == '__main__':
    parser = optparse.OptionParser('%prog [options]\nClone directory with hardlinks', version='%prog 1.0', )

    parser.add_option('-s', '--source',
                      action='store', dest='source', default=None,
                      help='The directory that will be replicated')

    parser.add_option('-t', '--target',
                      action='store', dest='target', default=None,
                      help='The directory that the files will be replicated into')

    parser.add_option('--skip', '--skip-warning',
                      action='store_false', dest='warn', default=True,
                      help='Skip the prompt to remove the target first.  '
                           'Needed for cron jobbing, does not apply when merging')

    parser.add_option('-m', '--merge',
                      action='store_true', dest='merge', default=False,
                      help='Merge the two directories. Not recommended.')

    parser.add_option('-f', '--follow_links',
                      action='store_true', dest='follow', default=False,
                      help='Follow sym links when cloning. WARNING, can crate circular redundancy')

    parser.add_option('-v', '',
                      action='count', dest='verbose', default=0,
                      help='Level of verbosity')

    options, args = parser.parse_args()

    if options.source is None or options.target is None:
        parser.print_help()
        exit()

    main(options.source, options.target, options.warn, options.merge, options.follow, options.verbose)
