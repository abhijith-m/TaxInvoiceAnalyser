TaxInvoiceAnalyser


Download the directory TaxInvoiceAnalyser to your local,

- TaxInvoiceAnalyser:
	   |
	   |
		- db_helper
		- Files
		- Logs
		- Scripts
		- Utils
		- .env
		- pyproject.toml
		- requirements.txt
		- settings.py

Open command Prompt in the root folder.

Assuming the machine already has python3.11 installed.
To Check python Version, type the following in the prompt.
	
	python --version


To check is pip is already installed, type

	pip help

To install pip, 
download get-pip.py from https://bootstrap.pypa.io/get-pip.py
or type in the prompt:

	curl https://bootst/rap.pypa.io/get-pip.py -o get-pip.py

then run

	python get-pip.py

Verify installation

	pip -V

then run 
	
	pip install -r requirements.txt

this will install the required packages.

Running Scripts:
The scripts are located in Scripts/ folder.

Extract Data:
To start the process, please place the pdf file in Files/ folder. If not given, it will take the file "Test PDF.pdf" as default.

from the command prompt, run

	python -m Scripts.ExtractData 'File_Name.pdf'

or to take the default file..

	python -m Scripts.ExtractData

Voila! You are ready to generate results.


