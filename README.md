# PyArchiver

PyArchiver is a simple command-line interface (CLI) utility for creating backups and extracting them. It allows you to backup files and directories, optionally creating a password-protected archive.

## Features

- Backup files and directories.
- Create password-protected archives.
- Extract files from password-protected archives.
- Verbose mode for detailed information.

## Usage

### Backup

To backup files or directories:

```bash
python pyarchiver.py backup source1 source2 ... --destination /path/to/destination [--archive] [--passphrase your_passphrase] [--verbose]
```

- `backup`: Action to perform.
- `source1 source2 ...`: List of source files or directories to backup.
- `--destination`: Path to the destination directory.
- `--archive`: (Optional) Create a password-protected archive.
- `--passphrase`: (Optional) Passphrase for the archive.
- `--verbose`: (Optional) Print detailed information.

### Extract

To extract files from an archive:

```bash
python pyarchiver.py extract --destination /path/to/destination --archive-path /path/to/archive [--passphrase your_passphrase] [--verbose]
```

- `extract`: Action to perform.
- `--destination`: Path to the destination directory.
- `--archive-path`: Path to the archive file.
- `--passphrase`: (Optional) Passphrase for the archive.
- `--verbose`: (Optional) Print detailed information.

## Examples

### Backup Example

```bash
python pyarchiver.py backup /home/user/documents /home/user/photos --destination /backup --archive --passphrase mysecretpass --verbose
```

### Extract Example

```bash
python pyarchiver.py extract --destination /restore --archive-path /backup/archive.zip --passphrase mysecretpass --verbose
```