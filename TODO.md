# To Do
* Add functionality to remove the a test from the test list.
* Add functionality to rename tests.
* Begin adding the load/save functionality so that this can be worked on as the project progresses (rather than trying to do it all at the end). This will make development easier because we won't have to load in the tests every time we launch the GUI.
* Make change to test data viewing table so that the active data shown is completely controlled by the data for the test selected in the test list.
* Add functionality to move tests up and down in the test list.

# Done
* Remove the padding from the single test plot on the
  Test Suite tab.
  - Removed the padding by switching to maptlotlib. Plots are looking nice
  now.
* Stylize the single test plot on the Test Suite tab.
* Change the data structure of self.tests in the View class.
  The data structure should be a list of dictionaries, so that
  the dictionary for a test can directly be passed into functions.
  This will make updating tables and plots easier.
* Figure out why there is stairstepping in the in the QChart plots.
  - Fixed by changing from PyQt charts to matplotlib
* Add functionality for the global test plot (i.e., shows all of the test
  data on one plot).
  

# Maybe Later?
* Change the listbox to a table on the Test Suite tab.