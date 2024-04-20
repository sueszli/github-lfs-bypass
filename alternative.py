import hashlib
import sys
import pathlib
import subprocess


"""
this is an alternative implementation in python.

i chose to rewrite it in bash because it's: simpler, faster, more robust
"""


def assert_matching_checksums(filepath1: pathlib.Path, filepath2: pathlib.Path) -> None:
    print(f"verifying checksums...")
    checksum1 = hashlib.md5(pathlib.Path(filepath1).read_bytes()).hexdigest()
    checksum2 = hashlib.md5(pathlib.Path(filepath2).read_bytes()).hexdigest()
    assert checksum1 == checksum2, f"checksums do not match: {checksum1} != {checksum2}"
    print(f"checksums match: {checksum1} == {checksum2}")


def assert_matching_filesizes(filepath1: pathlib.Path, filepath2: pathlib.Path) -> None:
    print(f"verifying file sizes...")
    filesize1 = filepath1.stat().st_size
    filesize2 = filepath2.stat().st_size
    assert filesize1 == filesize2, f"file sizes do not match: {filesize1} != {filesize2}"
    print(f"file sizes match: {filesize1} == {filesize2}")


def split():
    filepath = pathlib.Path(sys.argv[1])

    assert pathlib.Path(".git").exists(), "put this script inside the git directory"
    assert filepath.exists(), f"file does not exist: {filepath}"
    assert filepath.is_file(), f"not a file: {filepath}"
    assert not any([sibling.name == ".git" for sibling in list(filepath.parent.glob("*"))]), f"{filepath} should not be in a .git directory"

    # create tmp directory
    tmp_dir_path = pathlib.Path("tmp")
    shutil.rmtree(tmp_dir_path, ignore_errors=True)
    tmp_dir_path.mkdir()
    print(f"created new directory: {tmp_dir_path}")

    # don't track tmp directory
    gitignore_path = pathlib.Path(".gitignore")
    gitignore_path.touch()
    already_ignored = any([line.strip() == f"{tmp_dir_path}/" for line in gitignore_path.read_text().split("\n")])
    if not already_ignored:
        with open(gitignore_path, "a") as f:
            f.write(f"{tmp_dir_path}/\n")
        print(f"added {tmp_dir_path} to .gitignore")
    subprocess.run(["git", "add", ".gitignore"])
    subprocess.run(["git", "commit", "-m", "lfs-hack auto commit: .gitignore"])
    subprocess.run(["git", "push"])

    # copy file to tmp directory
    shutil.copy(filepath, tmp_dir_path)
    print(f"copied {filepath.name} to {tmp_dir_path} directory")

    # create checksum file
    with open(tmp_dir_path / f"{filepath.name}.md5", "w") as f:
        f.write(hashlib.md5(pathlib.Path(tmp_dir_path / filepath.name).read_bytes()).hexdigest())
    print(f"created checksum file: *.md5")

    # split file into chunks in tmp directory
    chunk_size = 50 * 1024 * 1024
    num_chunks = (filepath.stat().st_size // chunk_size) + 1
    for i in range(num_chunks):
        with open(tmp_dir_path / f"{filepath.name}.{i}", "wb") as f:
            f.write((tmp_dir_path / filepath.name).read_bytes()[i * chunk_size : (i + 1) * chunk_size])
    (tmp_dir_path / filepath.name).unlink()
    print(f"finished creating chunks")

    # create data file
    data_dir_path = pathlib.Path("data")
    shutil.rmtree(data_dir_path, ignore_errors=True)
    data_dir_path.mkdir()
    print(f"created new directory: {data_dir_path}")

    # copy each chunk into data directory, commit, and push
    for i in range(num_chunks):
        chunkfile_path = tmp_dir_path / f"{filepath.name}.{i}"
        shutil.copy(chunkfile_path, data_dir_path)
        subprocess.run(["git", "add", data_dir_path / chunkfile_path.name])
        subprocess.run(["git", "commit", "-m", f"lfs-hack auto commit: {chunkfile_path}"])
        subprocess.run(["git", "push"])
        print(f"\033[92mprogress: {i}/{num_chunks} \033[0m")
    print(f"finished pushing chunks")

    # upload checksum file
    shutil.copy(tmp_dir_path / f"{filepath.name}.md5", data_dir_path)
    subprocess.run(["git", "add", data_dir_path / f"{filepath.name}.md5"])
    subprocess.run(["git", "commit", "-m", f"auto commit: {filepath.name}.md5"])
    subprocess.run(["git", "push"])
    print(f"finished pushing checksum file")


def merge():
    data_dir_path = pathlib.Path("data")

    assert data_dir_path.exists(), f"directory does not exist: {data_dir_path}"
    for file in data_dir_path.iterdir():
        suffix = file.name.split(".")[-1]
        assert suffix.isdigit() or suffix == "md5", f"unexpected file: {file}"

    # merge all chunks together
    data_file_paths = sorted(list(data_dir_path.glob("*")))
    chunk_files = [file for file in data_file_paths if file.suffix != ".md5"]
    dst_path = data_dir_path / data_file_paths[0].stem
    with open(dst_path, "wb") as f:
        for chunk_file in chunk_files:
            f.write(chunk_file.read_bytes())
    print(f"finished merging {len(chunk_files)} chunks into {dst_path}")

    # verify checksum
    given_checksum = hashlib.md5(dst_path.read_bytes()).hexdigest()
    expected_checksum = (data_dir_path / f"{dst_path.name}.md5").read_text().strip()
    assert given_checksum == expected_checksum, f"checksum mismatch: {given_checksum} != {expected_checksum}"
    print(f"checksum verified: {given_checksum} == {expected_checksum}")

    # remove chunks
    for file in data_file_paths:
        file.unlink()
    print(f"removed all chunks")


if __name__ == "__main__":
    split()
    # merge()
