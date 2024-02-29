""" Class to write trial data to CSV. """

############
# IMPORTS  #
############
# Import system packages
import csv
from pathlib import Path
from datetime import datetime
import os


#########
# MODEL #
#########
class CSVModel:
    """ Write provided dictionary to CSV. """
    def __init__(self, sessionpars, **kwargs):
        """ Create datestamp for file name. 
            Create data directory.
        """

        # Assign variables
        self.sessionpars = sessionpars

        # Generate date stamp
        self.datestamp = datetime.now().strftime("%Y_%b_%d_%H%M")

        # Define data directory name
        if 'data_dir_name' in kwargs:
            self.data_directory = kwargs['data_dir_name']
        else:
            self.data_directory = "Data"


    def _check_for_data_folder(self):
        """ Check for existing data folder. Create a data folder if
            it doesn't currently exist.
        """
        data_dir_exists = os.access(self.data_directory, os.F_OK)
        if not data_dir_exists:
            print(f"\ncsvmodel: {self.data_directory} directory not " +
                "found! Creating it...")
            os.mkdir(self.data_directory)
            print(f"csvmodel: Successfully created {self.data_directory} " +
                  "directory!")


    def _create_filename(self):
        """ Create file name and path. """
        self.filename = f"{self.sessionpars['subject'].get()}_{self.sessionpars['condition'].get()}_{self.datestamp}.csv"
        self.file = Path(os.path.join(self.data_directory, self.filename))


    def _check_write_access(self):
        """ Check for write access to store CSV. """
        file_exists = os.access(self.file, os.F_OK)
        parent_writable = os.access(self.file.parent, os.W_OK)
        file_writable = os.access(self.file, os.W_OK)
        if (
            (not file_exists and not parent_writable) or
            (file_exists and not file_writable)
        ):
            msg = f"\ncsvmodel: Permission denied accessing file: \
                {self.filename}"
            raise PermissionError(msg)


    def _write_dict_to_csv(self, data):
        """ Write dict data to CSV. Check for existing file to determine 
            whether or not to include header when writing to CSV.
        """
        # Write file
        newfile = not self.file.exists()
        with open(self.file, 'a', newline='') as fh:
            csvwriter = csv.DictWriter(fh, fieldnames=data.keys())
            if newfile:
                csvwriter.writeheader()
            csvwriter.writerow(data)
        print("\ncsvmodel: Record successfully saved!")


    def save_record(self, data):
        """ Save a dictionary of data to .csv file. """
        # Create data directory if it does not exist
        self._check_for_data_folder()
        
        # Create file name and full path
        self._create_filename()

        # Check for write access
        try:
            self._check_write_access()
        except PermissionError:
            raise

        # Append data to CSV
        self._write_dict_to_csv(data)
