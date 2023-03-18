# Running the code on a research cluster with SLURM jobs

These instructions document the Python and module versions used to run this code. The code was updated to utilize the latest modules in 2023.
In the instructions that follow, replace `[projectDirectoryPath]` with the absolute path on the research computer (including leading and trailing / which will look something like `/nas/researchsystem/home/me/medication_natural_language_processing/`) where you cloned this code. These instructions assume a Linux command line research computer using modules and SLURM jobs. Also replace `[yourEmailAddress]` with your email address if your SLURM is setup to email you when jobs start or end. A `requirements.txt` file was added to this repository to list the Python modules required to run this code.

Note, this code and included medication data finished processing in less than a minute on our research computer with minimal resources.

Copying code to `[projectDirectoryPath]` on the research computer.

From a terminal command line, SSH into the research computer (if needed).

Execute the following commands in the terminal to start a Python Anaconda virtual environment (some commands only need to be run once).

```s bash
# start a virtual environment to run our Python scripts (we will just reuse our processMedsTest VE)
cd ~
module purge
module load anaconda/2021.11  # runs on RHEL8 and assumes conda v4.12.0
conda env remove --name processMedsTest    # ONLY RUN THIS ONCE
conda create --yes --name processMedsTest python=3.11    # ONLY RUN THIS ONCE
conda activate processMedsTest
mkdir --parents [projectDirectoryPath]slurmfiles/output/        # ONLY RUN THIS ONCE
```

Next we will create a SLURM script with our Python commands to process the data. You can simply copy the lines of code below and paste into the terminal command line (the commands assume we are using `nano` text editor, so replace with vim or your text editor of choice).

```s bash
(
rm nano [projectDirectoryPath]slurmfiles/processMeds.sh     # remove exiting script
nano [projectDirectoryPath]slurmfiles/processMeds.sh    # create new script
)
```

Below are the SLURM contents we will copy and paste into our `processMeds.sh` script.

```s SLURM
#!/bin/bash

#SBATCH -p general
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --time=02:00:00
#SBATCH --mem=200m
#SBATCH --mail-user=[yourEmailAddress]
#SBATCH --mail-type=begin   # event to send an email
#SBATCH --mail-type=end     # event to send an email
#SBATCH --error=[projectDirectoryPath]slurmfiles/output/job_%A.err
#SBATCH --output=[projectDirectoryPath]slurmfiles/output/job_%A.out

pip install -r [projectDirectoryPath]data-preprocess/requirements.txt
cd [projectDirectoryPath]data-preprocess

# count medications found in the list of raw data
python extract-med-count.py raw_data.csv 'medication' extract_med_count_OUTPUT.json

#take the medications list count and create a cooresponding dictionary
python create-med-dict-file.py extract_med_count_OUTPUT.json create_med_dict_file_OUTPUT.json

python preprocessMedFile.py

python buildSymptomDict_and_mapReasons.py med_processed_with_categories.csv df_all_patient_matched_reason_med.csv df_matched_reason_count.csv df_unmatched_reason_count.csv
```

Copy and paste the following commands into your terminal to clear the SLURM logs and execute a new SLURM job.

```s (bash)
(
rm [projectDirectoryPath]slurmfiles/output/*   # clear out job logs
sbatch [projectDirectoryPath]slurmfiles/processMeds.sh   # Submit job
)
```

## Issues

Make sure your column names in the raw data do not contain leading or trailing spaces (otherwise you might get failed jobs with 'key' errors).

## Running the scripts using Docker [https://hub.docker.com/_/python]

Not bothering since it is easier to setup on my research cluster using the processes above.
