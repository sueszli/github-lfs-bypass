# merge data chunks into data-merged directory (they're chunked to bypass git-lfs)
chmod +x lfs-merge.sh
./lfs-merge.sh

# untar data-merged/merged.tar into data-merged
tar -xf data-merged/merged.tar -C data-merged

# remove data-merged/merged.tar
rm -f data-merged/merged.tar
