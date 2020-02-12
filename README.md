# clone_dir_with_hardlinks
## Clone a directory with hardlinks

If you cannot hardlink a directory keeping a structurally identical copy with hardlinks is close.  Cron job the processes to keep in sync.

```bash
Usage: clone_dir_with_hardlinks.py [options]
Clone directory with hardlinks

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -s SOURCE, --source=SOURCE
                        The directory that will be replicated
  -t TARGET, --target=TARGET
                        The directory that the files will be replicated into
  --skip, --skip-warning
                        Skip the prompt to remove the target first.  Needed
                        for cron jobbing, does not apply when merging
  -m, --merge           Merge the two directories. Not recommended.
  -f, --follow_links    Follow sym links when cloning. WARNING, can crate
                        circular redundancy
  -v                    Level of verbosity
```
