# local_xml_reader
An XML Reader with automated Invoice Emission, Excel Table handling and more...

This Repo is a work in progress, It basically features a project written in Python which automated the emission of invoices, with the added tools of XML reading and Excel table writting.

Given this project required (By merely a window check) an external software to run. You won't be able to direclty run it unless you have such software (which is Synchro DFE Manager).

Through code you can disable this window check and use another application if you wish.

In case you try to render it using pyInstaller, make sure that local_rfid.xlsx is available when saving the spreadsheets. (Given no table creation was implemented, it's best advised to use that file as a model).

By experience, do not try to open the spreadsheet in other editors (such as openOffice, WPS and etc). I've noticed that, for some reason, openpyxl is not able to read the xml tags which are embedded in the file (which seems to be "footprints" of the program last opened).

This is an educated conjecture, but the advice remains.
