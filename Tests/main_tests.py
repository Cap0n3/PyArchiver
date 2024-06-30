import os
import shutil
import unittest
import glob
import sys
import inspect
from unittest.mock import patch
from io import StringIO
import subprocess

# To reference the main.py file, we need to add the parent directory to the path
CURR_DIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
PARENT_DIR = os.path.dirname(CURR_DIR)
sys.path.insert(0, PARENT_DIR)

from main import main  # Import the main function from main.py
from backup_utility import BackupUtility


class MainTestCase(unittest.TestCase):
    def setUp(self):
        print("Setting up test cases...")
        # Create temporary test directories relative to the current directory
        self.source_dir = os.path.join(CURR_DIR, "test_source")
        self.destination_dir = os.path.join(CURR_DIR, "test_destination")
        os.makedirs(self.source_dir, exist_ok=True)
        os.makedirs(self.destination_dir, exist_ok=True)

        # Create some test files in the source directory
        self.file_contents = {
            "file1.txt": b"Test file 1 contents",
            "file2.txt": b"Test file 2 contents",
            "file3.txt": b"Test file 3 contents",
        }

        # Write the test files to the source directory
        for filename, contents in self.file_contents.items():
            file_path = os.path.join(self.source_dir, filename)
            with open(file_path, "wb") as file:
                file.write(contents)

        # Create a subfolder in the source directory
        self.subFolder1_path = os.path.join(self.source_dir, "subFolder1")
        os.makedirs(self.subFolder1_path, exist_ok=True)

        # Create some test files in the subfolder
        self.subFile_contents = {
            "subFile1.txt": b"Test subfile 1 contents",
            "subFile2.txt": b"Test subfile 2 contents",
            "subFile3.txt": b"Test subfile 3 contents",
        }

        # Write the test files to the subfolder
        for filename, contents in self.subFile_contents.items():
            file_path = os.path.join(self.subFolder1_path, filename)
            with open(file_path, "wb") as file:
                file.write(contents)

    #@unittest.skip("Skipping tearDown to inspect created files")
    def tearDown(self):
        # Remove temporary test directories
        shutil.rmtree(self.source_dir)
        shutil.rmtree(self.destination_dir)

    @unittest.skip("Skipping test_main_backup")
    def test_main_backup(self):
        subprocess.run(
            [
                "poetry",
                "run",
                "python",
                "main.py",
                "backup",
                f"{self.source_dir}/file1.txt",
                f"{self.source_dir}/file2.txt",
                "--destination",
                f"{self.destination_dir}",
            ],
            check=True,
        )
        self.assertTrue(os.path.isfile(os.path.join(self.destination_dir, "file1.txt")))
        self.assertTrue(os.path.isfile(os.path.join(self.destination_dir, "file2.txt")))
    
    #@unittest.skip("Skipping test_main_extract")
    def test_main_extract(self):
        # Create an archive first (with passphrase)
        backup_utility = BackupUtility(destination=self.destination_dir, archive=True, passphrase="abc")
        backup_list = [
            os.path.join(self.source_dir, 'file1.txt'),
            os.path.join(self.source_dir, 'file2.txt'),
            os.path.join(self.source_dir, 'file3.txt'),
            self.subFolder1_path
        ]
        backup_utility.process_list(backup_list, verbose=True)
        # Check if there's a .7z file
        archive_files = glob.glob(os.path.join(self.destination_dir, '*.7z'))
        self.assertTrue(len(archive_files) > 0, "No .7z archive file found in the destination directory")
        
        # Get name of the archive file
        archive_file_name = archive_files[0]
        
        print(f"FILE NAME IS {archive_file_name}")
        
        # Extract the archive
        subprocess.run(
            [
                "poetry",
                "run",
                "python",
                "main.py",
                "extract",
                "--archive-path",
                f"{archive_file_name}",
                "--destination",
                f"{self.destination_dir}",
                "--passphrase",
                "abc"
            ],
            check=True,
        )
        
        #self.assertTrue(os.path.isfile(os.path.join(self.destination_dir, 'file1.txt')))
        
    # #@unittest.skip("Skipping test_main_backup")
    # @patch('sys.argv', ['main.py', 'backup', 'test_source/file1.txt', 'test_source/file2.txt', '--destination', 'test_destination'])
    # def test_main_backup(self):
    #     with patch('sys.stdout', new=StringIO()) as fake_output:
    #         main()
    #         output = fake_output.getvalue().strip()
    #         print(output)
    #         # Check if the files were backed up
    #         self.assertTrue(os.path.isfile(os.path.join(self.destination_dir, 'file1.txt')))
    #         self.assertTrue(os.path.isfile(os.path.join(self.destination_dir, 'file2.txt')))

    # @unittest.skip("Skipping test_main_extract")
    # @patch('sys.argv', ['main.py', 'extract', '--archive-path', 'test_destination/archive.7z', '--destination', 'test_destination'])
    # def test_main_extract(self):
    #     # Create an archive first
    #     backup_utility = BackupUtility(destination=self.destination_dir, archive=True, passphrase="abc")
    #     backup_list = [
    #         os.path.join(self.source_dir, 'file1.txt'),
    #         os.path.join(self.source_dir, 'file2.txt'),
    #         os.path.join(self.source_dir, 'file3.txt'),
    #         self.subFolder1_path
    #     ]
    #     backup_utility.process_list(backup_list, verbose=True)
    #     archive_files = glob.glob(os.path.join(self.destination_dir, '*.7z'))
    #     self.assertTrue(len(archive_files) > 0, "No .7z archive file found in the destination directory")

    #     # Rename the archive file to match the expected name
    #     archive_file_path = archive_files[0]
    #     os.rename(archive_file_path, os.path.join(self.destination_dir, 'archive.7z'))

    #     with patch('sys.stdout', new=StringIO()) as fake_output:
    #         main()
    #         output = fake_output.getvalue().strip()
    #         # Check if the files were extracted
    #         extracted_path = os.path.join(self.destination_dir, 'archive')
    #         self.assertTrue(os.path.isfile(os.path.join(extracted_path, 'file1.txt')))
    #         self.assertTrue(os.path.isfile(os.path.join(extracted_path, 'file2.txt')))
    #         self.assertTrue(os.path.isfile(os.path.join(extracted_path, 'file3.txt')))
    #         self.assertTrue(os.path.isdir(os.path.join(extracted_path, 'subFolder1')))


if __name__ == "__main__":
    unittest.main()
