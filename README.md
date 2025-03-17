 _________________
|  :           :  | chunk commits.
|  :           :  | get unlimited free storage on github.
|  :           :  | 
|  :           :  | 
|  :___________:  | 
|     _________   | 
|    | __      |  |
|    ||  |     |  |
\____||__|_____|__|

github commits are restricted to 25-50 MiB, varying based on the push method [^1].

to handle files beyond this limit, git lfs (large file storage) pointers are necessary, referencing an external lfs server [^2].

however, this method incurs a monthly cloud storage fee to github [^3].

[^1]: https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github#file-size-limits
[^2]: https://news.ycombinator.com/item?id=27134972#:~:text=of%20such%20projects-,wokwokwok,-on%20May%2013
[^3]: https://docs.github.com/en/billing/managing-billing-for-git-large-file-storage/about-billing-for-git-large-file-storage

# usage

```bash
#
# upload to github
#

# compress data outside of repository
tar -czvf merged.tar.gz <huge-directory/>

# chunk and upload inside the repository
./upload.sh ./../merged.tar.gz

#
# download from github
#

# clone
git clone <https://github.com/user/project>
cd <project>

# merge chunks back together, verify checksum
./download.sh
```
