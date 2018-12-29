# Multi-filter_classification_of_RNA_dataset
1. Create a python3 virtual environment 
      virtualenv -p python3 envname
      source envname/bin/activate

2. install all the packages needed. (sklearn, pandas)
      pip install sklearn 
      pip install pandas
      pip install matplotlib

3. Source codes:
  check.py:
		  Checks the integrity of the downloaded RNA files 
      Usage: python check.py 

  parse_file_case_id.py:  
		  Fetch the unique file id and the corresponding case ids.	
		  Usage: python parse_file_case_id.py

  request_meta.py: 
      Request the meta data for the files and cases using the GDC REST API.
		  Usage: python request_meta.py

  gen_miRNA_matrix.py: 
      Generates the matrix after pre-processing with the corresponding labels for the downloaded files.
		  Usage: gen_miRNA_matrix.py
      
For more details of the project please visit:
https://youtu.be/4qmLwbNc0xQ


