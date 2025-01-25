import os
import time
import tempfile

# Test configuration
TEST_FILE_SIZE_MB = 100000  # Size of test file for benchmarking
DUMMY_TRACKER = "http://example.com/announce"


def generate_test_file(path, size_mb):
    """Generate a test file with random data"""
    with open(path, "wb") as f:
        f.write(os.urandom(size_mb * 1024 * 1024))


# def create_with_libtorrent(input_path, output_file):
#     import libtorrent as lt
#     fs = lt.file_storage()
#     if os.path.isdir(input_path):
#         lt.add_files(fs, input_path)
#     else:
#         fs.add_file(os.path.basename(input_path), os.path.getsize(input_path))
#
#     torrent = lt.create_torrent(fs, flags=lt.create_torrent.v1_only)
#     torrent.add_tracker(DUMMY_TRACKER)
#     lt.set_piece_hashes(torrent, os.path.dirname(input_path))
#
#     with open(output_file, "wb") as f:
#         f.write(lt.bencode(torrent.generate()))


def create_with_dottorrent(input_path, output_file):
    from dottorrent import Torrent

    torrent = Torrent(input_path, trackers=[DUMMY_TRACKER])
    torrent.generate()
    with open(output_file, "wb") as output_file_fp:
        torrent.save(output_file_fp)


def create_with_torf(input_path, output_file):
    from torf import Torrent

    t = Torrent(path=input_path, trackers=[DUMMY_TRACKER])
    t.generate()
    t.write(output_file)


def create_with_torrentool(input_path, output_file):
    from torrentool.api import Torrent

    torrent = Torrent.create_from(input_path)
    torrent.announce_urls = [DUMMY_TRACKER]
    torrent.to_file(output_file)


def create_with_py3createtorrent(input_path, output_file):
    from py3createtorrent import create_torrent

    create_torrent(input_path, output=output_file, trackers=[DUMMY_TRACKER])


def benchmark():
    """Run performance tests for all torrent libraries"""
    results = []

    with tempfile.TemporaryDirectory() as tmpdir:
        # Create test file
        test_file = os.path.join(tmpdir, "testfile.bin")
        generate_test_file(test_file, TEST_FILE_SIZE_MB)
        print(f"Created test file: {TEST_FILE_SIZE_MB}MB")

        # Define test cases
        libraries = [
            # ("libtorrent", create_with_libtorrent),
            ("dottorrent", create_with_dottorrent),
            ("torf", create_with_torf),
            ("torrentool", create_with_torrentool),
            ("py3createtorrent", create_with_py3createtorrent),
        ]

        # Run benchmarks
        for name, create_fn in libraries:
            output_path = os.path.join(tmpdir, f"output_{name}.torrent")
            error = None
            duration = None

            try:
                start_time = time.perf_counter()
                create_fn(test_file, output_path)
                duration = time.perf_counter() - start_time
            except Exception as e:
                error = str(e)
                if "No module named" in error:
                    error = "Library not installed"

            results.append((name, duration, error))
        print("Generation Completed...")

    # Display results
    print("\nBenchmark Results:")
    print("{:<15} {:<12} {:<20}".format("Library", "Time (s)", "Status"))
    print("-" * 45)
    for name, duration, error in results:
        if error:
            status = f"Error: {error}"
            time_str = "N/A"
        else:
            status = "Success"
            time_str = f"{duration:.4f}"
        print("{:<15} {:<12} {:<20}".format(name, time_str, status))


if __name__ == "__main__":
    # Check for required libraries
    # try:
    #     import libtorrent  # pylti1hrd exception
    # except ImportError:
    #     pass  # Handled during benchmarking

    benchmark()
