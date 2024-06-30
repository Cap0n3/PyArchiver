import os
import shutil
import datetime
import py7zr
import errno


class BackupUtility:
    """
    Class for backing up files and directories.

    Parameters
    ----------
    destination : str
        Path to the destination directory.
    archive : bool, optional
        If True, the backup will be saved as archive_YYYY-MM-DD__HH.MM.SS.7z in the destination path.
    passphrase : str, optional
        Passphrase for the archive.

    Examples
    --------

    # Create an archive of the backup list
    backup_utility = BackupUtility(destination="/path/to/destination", archive=True, passphrase="your_passphrase")
    backup_utility.process_list(["/path/to/source1", "/path/to/source2"])

    # Extract an archive with a passphrase
    backup_utility = BackupUtility(destination="/path/to/destination", passphrase="your_passphrase")
    backup_utility.extract_archive_with_passphrase("/path/to/archive.7z", "/path/to/destination")

    """

    def __init__(self, destination, archive=False, passphrase=None):
        """
        Initialize the backup utility.

        Parameters
        ----------
        destination : str
            Path to the destination directory.
        archive : bool, optional
            If True, the backup will be saved as archive_YYYY-MM-DD__HH.MM.SS.7z in the destination path.
        passphrase : str, optional
            Passphrase for the archive.
        """
        self.destination = destination
        self.archive = archive
        self.passphrase = passphrase

    def _copy_item(self, source, destination, verbose):
        """
        Copy a single file or directory.

        Parameters
        ----------
        source : str
            Path to the source file or directory.
        destination : str
            Path to the destination directory.
        verbose : bool
            If True, print information about the copy operation.
        """
        try:
            destination = os.path.join(destination, os.path.basename(source))
            shutil.copytree(
                source, destination, ignore=shutil.ignore_patterns("*.pyc", "tmp*")
            )
            if verbose:
                print(f"Copying directory {source} to {destination}")
        except OSError as e:
            if e.errno == errno.ENOTDIR:
                shutil.copy2(source, destination)
                print(f"Copying file {source} to {destination}")
            else:
                print(f"Directory not copied. Error: {e}")
        except Exception as e:
            print(f"Directory not copied. Error: {e}")

    def process_list(self, backup_list, verbose=False):
        """
        Copy a list of files and directories.

        Parameters
        ----------
        backup_list : list
            List of paths to the source files and directories.
        verbose : bool, optional
            If True, print information about the copy operation.
        """
        if self.archive:
            self._create_archive(backup_list, verbose=verbose)
        else:
            for item in backup_list:
                self._copy_item(item, self.destination, verbose=verbose)

    def _create_archive(self, backup_list, verbose=False):
        """
        Create an archive of the backup list.

        Parameters
        ----------
        backup_list : list
            List of paths to the source files and directories.
        """
        archive_name = datetime.datetime.now().strftime("%d-%m-%Y__%H.%M.%S")
        os.makedirs("tmp", exist_ok=True)
        for item in backup_list:
            self._copy_item(item, "tmp", verbose=verbose)
        with py7zr.SevenZipFile(
            f"{self.destination}/archive_{archive_name}.7z",
            "w",
            password=self.passphrase,
        ) as archive:
            archive.writeall("tmp", archive_name)
        shutil.rmtree("tmp")
        if verbose:
            print(f"Archive created: {self.destination}/archive_{archive_name}.7z")

    def extract_archive_with_passphrase(
        self, archive_path, destination_path, verbose=False
    ):
        """
        Extract an archive with a passphrase.

        Parameters
        ----------
        archive_path : str
            Path to the archive file.
        destination_path : str [optional]
            Path to the destination directory. If not provided, the destination path will be the same as provided destination.
        verbose : bool, optional
            If True, print information about the extraction operation.
        """
        if not destination_path:
            destination_path = self.destination
            if verbose:
                print(
                    f"Destination path not provided. Using {destination_path} as destination path."
                )

        with py7zr.SevenZipFile(archive_path, "r", password=self.passphrase) as archive:
            archive.extractall(destination_path)

        if verbose:
            print(f"Archive extracted: {archive_path}")


# # TO REVISIT
# def backup_with_rsync(source_paths, destination_path, test=False):
#     """
#     Backs up the source paths to the destination path using rsync.

#     Parameters
#     ----------
#     source_paths : list
#         List of paths to the source files and directories.
#     destination_path : str
#         Path to the destination directory.
#     test : bool, optional
#         If True, the backup will be saved as test_source.7z in the destination path.

#     Examples
#     --------
#     >>> source_paths = ['/path/to/source1', '/path/to/source2/file.txt']
#     >>> destination_path = '/path/to/backup'
#     >>> backup_with_rsync(source_paths, destination_path)
#     """
#     # Create temporary directory for storing the archives
#     current_dir = os.getcwd()
#     temp_dir = os.path.join(destination_path, ".temp")
#     archive_name = (
#         "test_source.7z"
#         if test
#         else datetime.now().strftime("%Y%m%d_%H%M%S") + "_archive.7z"
#     )
#     os.makedirs(temp_dir, exist_ok=True)

#     try:
#         # Copy the source files to the temporary directory
#         for source_path in source_paths:
#             # Generate the archive file path
#             subprocess.run(["cp", "-r", source_path, temp_dir])

#         # Create the archive
#         with py7zr.SevenZipFile(archive_name, "w") as archive:
#             archive.writeall(temp_dir, "")

#         # Copy the archives to the destination path using rsync
#         subprocess.run(
#             ["rsync", "-av", os.path.join(current_dir, archive_name), destination_path]
#         )

#     finally:
#         # Clean up the temporary directory and archive
#         shutil.rmtree(temp_dir)
#         os.remove(archive_name)
