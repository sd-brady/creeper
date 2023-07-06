# TODO

* Initialize the unit combo box options in code vs in designer. This will allow
    more flexibility if we want to add different units later. Also reduces chance
    for bugs when passing unit systems around.

* Add an enum for plotting colors (e.g., "Blue": "tab:blue", "Red": #102512 )
    * Make the inputDialog and the plots reference the enum names and values.
    This will make it easy to edit, add, and remove colors.

* Add enum for active_state for test on test suite tab

* Add unit tests for the unit conversion functions in src/frontend/modules/unit_system.py

* Add unit functionality. (this will get it's own development branch)

# Later
* Begin adding the load/save functionality so that this can be worked on as the project progresses (rather than trying to do it all at the end). This will make development easier because we won't have to load in the tests every time we launch the GUI.

