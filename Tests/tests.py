import os
import shutil
import unittest
import glob
import sys
import inspect

# To reference the main.py file, we need to add the parent directory to the path
CURR_DIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
PARENT_DIR = os.path.dirname(CURR_DIR)
sys.path.insert(0, PARENT_DIR)

from main import BackupUtility

class BackupTestCase(unittest.TestCase):
    def setUp(self):
        # Create temporary test directories relative to the current directory
        self.source_dir = os.path.join(CURR_DIR, 'test_source')
        self.destination_dir = os.path.join(CURR_DIR, 'test_destination')
        os.makedirs(self.source_dir, exist_ok=True)
        os.makedirs(self.destination_dir, exist_ok=True)

        # Create some test files in the source directory
        self.file_contents = {
            'file1.txt': b'Test file 1 contents',
            'file2.txt': b'Test file 2 contents',
            'file3.txt': b'Test file 3 contents'
        }

        # Write the test files to the source directory
        for filename, contents in self.file_contents.items():
            file_path = os.path.join(self.source_dir, filename)
            with open(file_path, 'wb') as file:
                file.write(contents)

        # Create a subfolder in the source directory
        self.subFolder1_path = os.path.join(self.source_dir, 'subFolder1')
        os.makedirs(self.subFolder1_path, exist_ok=True)

        # Create some test files in the subfolder
        self.subFile_contents = {
            'subFile1.txt': b'Test subfile 1 contents',
            'subFile2.txt': b'Test subfile 2 contents',
            'subFile3.txt': b'Test subfile 3 contents'
        }

        # Write the test files to the subfolder
        for filename, contents in self.subFile_contents.items():
            file_path = os.path.join(self.subFolder1_path, filename)
            with open(file_path, 'wb') as file:
                file.write(contents)

    #@unittest.skip("Skipping cleanup test to inspect behavior")
    def tearDown(self):
        # Remove temporary test directories
        shutil.rmtree(self.source_dir)
        shutil.rmtree(self.destination_dir)

    #@unittest.skip("Skipping copy_item test")
    def test__copy_item(self):
        # Instantiate the backup utility
        backup_utility = BackupUtility(destination=self.destination_dir)

        # Get a file from the source directory
        file1_path = os.path.join(self.source_dir, 'file1.txt')

        # First, save a single file
        backup_utility._copy_item(file1_path, self.destination_dir, verbose=True)

        # Check if the file was backed up
        backup_path = os.path.join(self.destination_dir, 'file1.txt')
        self.assertTrue(os.path.isfile(backup_path))

        # Now save the subfolder
        backup_utility._copy_item(self.subFolder1_path, self.destination_dir, verbose=True)

        # Check if the subfolder was backed up
        backup_path = os.path.join(self.destination_dir, 'subFolder1')
        self.assertTrue(os.path.isdir(backup_path))

    #@unittest.skip("Skipping process_list test")
    def test_process_list(self):
        # Instantiate the backup utility
        backup_utility = BackupUtility(destination=self.destination_dir)

        # Create a list of files to backup
        backup_list = [
            os.path.join(self.source_dir, 'file1.txt'),
            os.path.join(self.source_dir, 'file2.txt'),
            os.path.join(self.source_dir, 'file3.txt'),
            self.subFolder1_path
        ]
        
        # Process the list without archive
        backup_utility.process_list(backup_list, verbose=True)

        # Check if the files and folder were backed up
        backup_path = os.path.join(self.destination_dir, 'file1.txt')
        self.assertTrue(os.path.isfile(backup_path))
        backup_path = os.path.join(self.destination_dir, 'file2.txt')
        self.assertTrue(os.path.isfile(backup_path))
        backup_path = os.path.join(self.destination_dir, 'file3.txt')
        self.assertTrue(os.path.isfile(backup_path))
        backup_path = os.path.join(self.destination_dir, 'subFolder1')
        self.assertTrue(os.path.isdir(backup_path))
    
    #@unittest.skip("Skipping extract_archive_with_passphrase test")
    def test_extract_archive_with_passphrase(self):
        # Create a list of files to backup
        backup_list = [
            os.path.join(self.source_dir, 'file1.txt'),
            os.path.join(self.source_dir, 'file2.txt'),
            os.path.join(self.source_dir, 'file3.txt'),
            self.subFolder1_path
        ]
        
        # Process the list with archive
        backup_utility = BackupUtility(destination=self.destination_dir, archive=True, passphrase="abc")
        backup_utility.process_list(backup_list, verbose=True)

        # Check if there's a file with .7z extension in destination directory
        archive_files = glob.glob(os.path.join(self.destination_dir, '*.7z'))
        self.assertTrue(len(archive_files) > 0, "No .7z archive file found in the destination directory")
        
        # Get name of the archive file
        archive_file_name = archive_files[0]
        
        # Open the archive
        backup_utility.extract_archive_with_passphrase(os.path.join(self.destination_dir, archive_file_name), self.destination_dir, verbose=True)
        
        # Create path of opened archive
        raw_extracted_archive_path = os.path.join(self.destination_dir, archive_file_name)
        extracted_archive_path = raw_extracted_archive_path.replace('archive_', '').replace('.7z', '')
                
        backup_path = os.path.join(extracted_archive_path, 'file1.txt')
        self.assertTrue(os.path.isfile(backup_path))
        backup_path = os.path.join(extracted_archive_path, 'file2.txt')
        self.assertTrue(os.path.isfile(backup_path))
        backup_path = os.path.join(extracted_archive_path, 'file3.txt')
        self.assertTrue(os.path.isfile(backup_path))
        backup_path = os.path.join(extracted_archive_path, 'subFolder1')
        self.assertTrue(os.path.isdir(backup_path))

if __name__ == '__main__':
    unittest.main()
