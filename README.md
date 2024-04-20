```
 _________________
|  :           :  | chunk files.
|  :           :  | avoid github cloud storage bills.
|  :           :  | 
|  :           :  | 
|  :___________:  | 
|     _________   | 
|    | __      |  |
|    ||  |     |  |
\____||__|_____|__|
```

github commits are restricted to 25-50 MiB, varying based on the push method [^1].

to handle files beyond this limit, git lfs (large file storage) pointers are necessary, referencing an external lfs server [^2].

however, this method incurs a monthly cloud storage fee to github [^3].

the scripts provided in this repository allow you to bypass the file size limit by committing a large file in small chunks.

<br><br>

**🔵 uploading:** the upload script takes a large file as an argument, splits the file into smaller chunks of a specified size (50mb in this case) and stores these chunks in a temporary directory. each chunk is then pushed to a remote repository.

```bash
./upload.sh ./../huge-file.tar
```

**🔴 downloading:** the download script should be run after each clone. concatenates all the chunks into a single file and checks the checksum of the merged file against the original checksum to ensure the file has not been corrupted during the whole process.

```bash
# clone and merge chunks back together
git clone https://github.com/user/project
./download.sh

# untar (or any other decompression)
tar -xf data-merged/merged.tar -C data-merged
rm -f data-merged/merged.tar
```

<br><br>

## footnotes

**ethical concerns:** i recognize that this project raises ethical questions surrounding the potential for freeriding on github's generosity. my primary goal is not to exploit the platform, but rather to facilitate more reproducible data-driven research. if the community believes this repository presents a significant ethical issue, i am absolutely willing to take it down immediately. please reach out to me directly with concerns or suggestions for alternative approaches.

[^1]: docs: https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github#file-size-limits
[^2]: nice comment: wokwokwok, 2021 on hackernews, https://news.ycombinator.com/item?id=27134972#:~:text=of%20such%20projects-,wokwokwok,-on%20May%2013
[^3]: https://docs.github.com/en/billing/managing-billing-for-git-large-file-storage/about-billing-for-git-large-file-storage
