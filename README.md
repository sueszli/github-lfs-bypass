```
 _________________
|# :           : #|
|  :           :  |
|  :           :  | github lfs exploit -
|  :           :  | github storage bills, no more
|  :___________:  |
|     _________   |
|    | __      |  |
|    ||  |     |  |
\____||__|_____|__|
```

<br>

github commits are restricted to 25-50 MiB, varying based on the push method [^1].

to handle files beyond this limit, git lfs (large file storage) pointers are necessary, referencing an external lfs server [^2].

however, this method incurs a monthly cloud storage fee to github [^3].

the scripts provided in this repository allow you to bypass the file size limit by committing a large file in small chunks.

- **split phase:** this script takes a large file as an argument, splits the file into smaller chunks of a specified size (50mb in this case) and stores these chunks in a temporary directory. each chunk is then added to a git repository and pushed to a remote repository → it is ran just once, when initializing the project.

- **merge phase:** this script concatenates all the chunks into a single file and checks the checksum of the merged file against the original checksum to ensure the file has not been corrupted during the split and merge process → it is ran on each clone.

<br><br>

> _ethical concerns_
> 
> i recognize that the methods outlined in this project raise ethical questions surrounding the potential for freeriding on github's generosity. my primary goal is not to exploit the platform, but rather to facilitate more reproducible data-driven research. i apologize for the clickbaity title.
> 
> while github is an excellent resource for code sharing, its current file size constraints can present obstacles for researchers working with large datasets. my hope is that github, or similar platforms, will evolve to provide more robust data management tools akin to those offered by kaggle or dedicated data hosting platforms.
> 
> if the community believes this repository presents a significant ethical issue, i am absolutely willing to take it down immediately. please reach out to me directly with concerns or suggestions for alternative approaches.

<br><br>

[^1]: docs: https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github#file-size-limits
[^2]: nice comment: wokwokwok, 2021 on hackernews, https://news.ycombinator.com/item?id=27134972#:~:text=of%20such%20projects-,wokwokwok,-on%20May%2013
[^3]: https://docs.github.com/en/billing/managing-billing-for-git-large-file-storage/about-billing-for-git-large-file-storage
