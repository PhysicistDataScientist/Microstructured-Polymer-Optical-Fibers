# Welcome to experiments on mPOFs!

In this repository you will find scientific work involving microstructured polymer optical fibers.

In the folder "General" you will find a manual to pull mPOFs using a drawing tower named "Manual.pdf". 
Also, you can check the "Technical Drawing Pulling.pdf" and "Technical Drawing Workshop.pdf". 
They are the technical drawings having the design of holes for a sample. 
The first helps me during the pulling process and the second is to create the preform.

Additionally, I uploaded the Excel sheets related to the control of the samples and their specifications.
The control of samples on the drying chamber is made by using "Samples Drying Chamber.xlsx".
The specification of each group of sample are in "Samples Group Specifications.xlsx".

To modify the archive "Samples Drying Chamber Control.xlsx" I created a python file "Samples Control.py", which I execute every time a change is made on a sample.
Also, this code relate the samples specifications from "Samples Group Specifications.xlsx".
The Excel sheets may be in the same folder and you need to pass the folder location to the file "Sample Path Manager.txt".

To help with the analysis of the pulling process, I developed a Python code named "Pulling Analyser.py".
In the file "Pulling Path Manager.txt" you shall pass the path location of the pulling data folder.
This file should be in the same folder as "Pulling Analyser.py"
There is one folder "E - 21" with example of different pulling bands ("Data Pulling Band A.txt", "Data Pulling Band B.txt" and "Data Pulling Band C.txt").
So, you need to pass the folder location which will contains the folder "E - 21".

A report on the pulling of the sample "E - 21" was elaborated and is available inside its folder as "Report.pdf".

A scientific paper about this fabrication process was published:
