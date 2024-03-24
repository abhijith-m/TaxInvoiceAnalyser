TaxInvoiceAnalyser


Download the directory TaxInvoiceAnalyser to your local,

- TaxInvoiceAnalyser:
	   |
	   |
		- db_helper
		- files
		- logs
		- scripts
		- utils
		- .env
		- pyproject.toml
		- requirements.txt
		- settings.py

Open command Prompt in the root folder.

Assuming the machine already has python3.11 and latest pip installed.

To set up pre-requisites, run 
	
	pip install -r requirements.txt

this will install the required packages.

The project has two scripts, extract_data and reports, located in scripts/ sub-directory

extract_data:
	This is the initial step, this is run to extract all the valid transactions from the PDF file and store data in the db.
 	Please place the file in files/ sub-directory. If not given, it will take the file "Test PDF.pdf" as default
  	
   from the command prompt, run
	
	python -m scripts.extract_data 'File_Name.pdf'
	
   or to take the default file..
	
	python -m scripts.extract_data
	
Voila! You are ready to generate results.

reports:
	This script is used to generate reports from the data. The user is prompted to select a report from a menu of all the different operations,
 	Once an option is selected, the script runs queries and displays the result in the prompt window.

  to run the script, use
  
  	 python -m scripts.reports


