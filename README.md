# Welcome to "Microstructured Polymer Optical Fibers"!

In the folder "General" you will find the "Manual.pdf", what gives instructions on how to pull mPOFs using a drawing tower. 
Also, you can check the technical drawings of a structured preform on "Technical Drawing Pulling.pdf" and "Technical Drawing Workshop.pdf". 
The first one, helps me during the pulling process and the second is to indeed create the preform.

Additionally, I uploaded an Excel sheet related to the control of the samples on the drying chambers named "Samples Drying Chamber.xlsx".
To modify the archive "Samples Drying Chamber.xlsx", I created a python file "Samples Control.py", which I execute every time a change is made on a sample.
You need to pass the folder location to the file "Sample Path Manager.txt".
"Sample Path Manager.txt" and "Samples Drying Chamber.xlsx" must be in the same folder as "Samples Control.py".

To help with the analysis of the pulling process, I uploaded to the folder "Pulling Analyser" a Python code named "Pulling Analyser.py".
In the file "Pulling Path Manager.txt" you shall pass the path location of the pulling data folder.
This file should be in the same folder as "Pulling Analyser.py".

There is one folder "E - 21" with example of different pulling bands ("Data Pulling Band A.txt", "Data Pulling Band B.txt" and "Data Pulling Band C.txt").
You need to pass the location to "Pulling Path Manager.txt" in which will contains the folder "E - 21".



Overview: Study on the fabrication process of microstructured polymer optical fibers (mPOFs).

Files:
- "Experimental Set 1": folder corresponding to one of the experimental acquisitions;
  - "E000X.TXT": .csv styled spectrums;
  - "Conversion Dictionary.xlsx": Excel sheet relating the spectrum file names with the input and output angles; 
- "Hi-Bi Fiber.py": Python code to effect the analysis over the experimental data and simulations;
- "Path Manager.txt": file to contain the path location of the folder with all the experimental data folders.

Instructions:
1) Put "Path Manager.txt" in the same folder as "Hi-Bi Fiber.py";
2) Write the path of the folder containing "Experimental Set 1" on "Path Manager.txt";
3) Put the "E000X.txt" files and "Conversion Dictionary.xlsx" inside "Experimental Set 1";
4) Fill the "Conversion Dictionary.xlsx" "Name" column with the angles corresponding spectrum file names.  
5) Run "Hi-Bi Fiber.py".

Scientific papers:
> https://ieeexplore.ieee.org/abstract/document/10560648?casa_token=8M7vaLN97ewAAAAA:UK_nWdh_bEQ2-33TGx_sRJk5CWOb5obSWx_9Qvz3P7tMnGzIPfgzdzxBOabnbepGBMI6RwoNR3IY
