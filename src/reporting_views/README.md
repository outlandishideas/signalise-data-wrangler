# Reporting views

Should query one or more underlying schemas and 
transform the data into something more useful.

The `util.create_reporting_views()` function creates the views in alphabetical order of the names of the files.

If you want to create views that rely on other views, use a higher number to start in the filename.

Create sets of views for a particular purpose in a single file, which also makes it easier to manage dependencies.

You can either create simple views and then do the processing in e.g. python
or you can create more complex views in SQL.