import re

def is_assembly(filepath):
    with open(filepath, 'r') as file:
        content = file.read()

        # Check for assembly or part keywords
        assembly_keywords = ['NEXT_ASSEMBLY_USAGE_OCCURRENCE']
        part_keywords = ['MANIFOLD_SOLID_BREP', 'ADVANCED_BREP_SHAPE_REPRESENTATION']

        is_assembly = any(re.search(keyword, content) for keyword in assembly_keywords)
        is_part = any(re.search(keyword, content) for keyword in part_keywords)
        print(f'is part value:{is_part}')
        if is_assembly:
            return True
        elif is_part:
            return False
        else:
            return False

if __name__=="__main__":
    import os
    import glob

    # Define the folder path where the STP files are located
    #folder_path =r'X:\25743_XOMETRY\3D'
    folder_path =r'D:\Analiza'

    # Get a list of all files in the folder with .stp extension
    stp_files = glob.glob(os.path.join(folder_path, '*.stp'))

    # Loop through each STP file and parse its contents
    for stp_file in stp_files:
        print(f'Parsing file: {stp_file}')

        # Add your parsing logic here
        # You can use a third-party library or implement your own parsing code
        result = is_assembly(stp_file)
        if result:
            print(f"The file is a {result}.")
        else:
            print("Unable to determine if the file is an assembly or part.")


        # Replace the "pass" statement with your parsing logic for each file

        print(f'Finished parsing file: {stp_file}\n')
