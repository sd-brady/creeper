# TODO

* Add signal (which should be the same signal for any of the unit combo boxes) for changing 
the unit time, temp, and stress combo boxs in the gui.

    * Signal should initiate a series of commands that:
        1) Assemble a new UnitSystem class for the GUI
        2) Retrieve the test suite.
        3) Convert the test suite using the GUI UnitSystem class
        4) Display new test suite on all widgets and plots

* Make new empty test class for model.sent_test_class

* Initialize the unit combo box options in code vs in designer. This will allow
more flexibility if we want to add different units later. Also reduces chance
for bugs when passing unit systems around.

* Add unit tests for the unit conversion functions in src/frontend/modules/unit_system.py

* Add unit functionality. (this will get it's own development branch)
    * IN-PROGRESS

# Later
* Begin adding the load/save functionality so that this can be worked on as the project progresses (rather than trying to do it all at the end). This will make development easier because we won't have to load in the tests every time we launch the GUI.

