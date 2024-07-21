# Welcome to "Microstructured Polymer Optical Fibers"!

Overview: Study on the fabrication process of microstructured polymer optical fibers (mPOFs).

Files:
- "E - 21": folder corresponding to one sample;
  - "Band X - Data - Pulling.txt": .csv styled pulling parameters;
- "General": folder with the general procedures;
  - "Manual.pdf": tutorial on how to draw mPOFs;
  - "Technical Drawing Workshop.pdf": technical drawing for the preform preparation;
- "Pulling Analyser": folder corresponding to the pulling parameters analysis;
  - "Pulling Analyser.py": Python code to analyse the pulling parameters;
  - "Pulling Path Manager.txt": file with the path of the folder containing the sample folders; 
- "Samples Control": folder corresponding to the samples information;
  - "Samples Control.py": Python code to monitor the samples inside the drying chambers;
  - "Samples Drying Chamber.xlsx": Excel sheet with the information of each sample in the drying chambers;
  - "Samples Path Manager.TXT": File with the path location of "Samples Drying Chamber.xlsx".

Instructions:
1) Put "Pulling Path Manager.txt" in the same folder as "Pulling Analyser.py";
2) Write the path of the folder containing "E - 21" on "Pulling Path Manager.txt";
3) Run "Pulling Analyser.py";
4) Put "Samples Path Manager.txt" in the same folder as "Samples Control.py";
5) Write the path of "Drying Chamber.xlsx" on "Samples Path Manager.txt";
6) Run "Samples Control.py".

Scientific papers:
> https://ieeexplore.ieee.org/abstract/document/10560648?casa_token=8M7vaLN97ewAAAAA:UK_nWdh_bEQ2-33TGx_sRJk5CWOb5obSWx_9Qvz3P7tMnGzIPfgzdzxBOabnbepGBMI6RwoNR3IY
