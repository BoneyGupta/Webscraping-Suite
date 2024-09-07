Automation Test Suite

 Why this testing suite?
 • This project is a one stop shop for all automation needs like web testing, web scapping, monitoring and data population using simple commands. 
 • It enhances flexibility of maintaining the continuity of data, in lengthy automation scenarios through excel sheet.
 • The excel tables and predefined columns makes it easy to visualize the dataflow.
 • Suite is useful in simplifying the test and flow management in most scenarios, for those having no code knowledge.
 • The available source code can be altered using minimum steps.
 • Data is generated sequentially in logs and json files in easy to reuse format.
 • Pytest and AI is in queue. Possibility of exploring similar features are endless.
 
 Will this work for me?
 • This suite can cater from simplest to highly complex programs. Features to add short code snippets in excel itself is inbuilt. Any user with minimal 
knowledge of Python can use the feature as entire automation is handled by the application.
 • New features are being developed to minimise coding requirement for user and maximise flexibility & functionality in excel sheet.
 
 Tech?
 • The code engages with browser automation using Playwright. Possiblities are being explored to support Selenium, API testing and mobile testing
 (Appium) using the same excel format. 


Step 1: First steps to start the process											
											
1)	Go the the automation testing suite directory >> open excel directory										
2)	Open the Test.xlsx for your first program( you can refer to 'Template.xlsx' and 'Automation Test Suite Commands.xlsx')										
  	Presently, only the excel file named as 'Test.xlsx' will be run for automation.										
3)	A pre-filled sheets will be present for your aide.										
4)	There are three required sheets( Details, Sheet having 'test' in its name and Dropdown) for the execution of test cases.										
  	Update the name of all the sheets which are up for testing with 'test' as prefix. 										
											
All the sheets and fields are described with the help of test case: amazon product page details										
											
Step 2: Details Entry			Open the 'Details' sheet in 'Test.xlsx								
				
Field entry options:	Description:						
Test Name	(Any alphanumeric value):	Declares the name of the Test						
Browser	(Chrome, Firefox, Edge):	Select a browser						
Website	(Complete website url):	Website names should be complete with https:// or similar prefix						
Headless	(TRUE, FALSE):	Headless testing is a testing which allows the browser to run in the backgroud without GUI.						
cdp	(TRUE, FALSE):	cdp is required when we want to work with already logged on browser with wesites which requires login or captcha. Do not support Headless testing
													
											
