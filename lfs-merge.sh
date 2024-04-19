# validate .gitignore
if [ ! -f .gitignore ]; then echo ".gitignore not found"; exit 1; fi
if ! grep -q "tmp/" .gitignore; then echo "tmp/ not in .gitignore"; exit 1; fi
if ! grep -q "data-merged/" .gitignore; then echo "data-merged/ not in .gitignore"; exit 1; fi

# validate ./data/* files
if [ ! -d data ]; then echo "data/ directory not found"; exit 1; fi
if ! ls data/*-chunk-* &> /dev/null && ! ls data/*.md5 &> /dev/null; then echo "invalid files found in data/"; exit 1; fi

# create data-merged directory
rm -rf data-merged
mkdir data-merged
echo "created data-merged directory"

# merge chunks into data-merged directory
cat data/*-chunk-* > data-merged/merged.tar
echo "merged chunks into data-merged/merged.tar"

# validate checksum
expected_checksum=$(cat data/*.md5)
actual_checksum=$(md5sum data-merged/merged.tar | awk '{ print $1 }')
if [ $expected_checksum != $actual_checksum ]; then echo "checksum mismatch"; exit 1; fi
echo "checksum matched: $expected_checksum == $actual_checksum"

echo "🟢 done"
exit 0
