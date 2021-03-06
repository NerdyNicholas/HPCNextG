When you know the format of the csv file and the structure you need in the xml file, it's fairly straightforward to make a script that can handle the conversion.

Take the file simple.csv:

Jack,35,United States
Jill,22,United Kingdom

You can create the following xml file:

<?xml version="1.0"?>
<Customers>
  <Customer>
    <Name>Jack</Name>
    <Age>35</Age>
    <Country>United States</Country>
 </Customer>
 <Customer>
    <Name>Jill</Name>
    <Age>22</Age>
    <Country>United Kingdom</Country>
 </Customer>
</Customers>

With the following script:

#!/bin/bash
file_in="simple.csv"
file_out="simple.xml"
echo '<?xml version="1.0"?>' > $file_out
echo '<Customers>' >> $file_out
while IFS=$',' read -r -a arry
do
  echo '  <Customer>' >> $file_out
  echo '    <Name>'${arry[0]}'</Name>' >> $file_out
  echo '    <Age>'${arry[1]}'</Age>' >> $file_out
  echo '    <Country>'${arry[2]}'</Country>' >> $file_out
  echo '  </Customer>' >> $file_out
done < $file_in
echo '</Customers>' >> $file_out

Even if you have never coded before, I think this should be easy to use and modify. The file is read line-by-line in the while loop.

IFS is the internal field specifier. The IFS=$',' declares that the value of the field separator is a comma. This is standard for a CSV file, but it can be changed as needed to match the input file format.

The -r argument to the read command tells it to treat any backslashes in your file as part of your data rather than as an escape for a following special character.

The -a arry argument places each column of your file into an array (named arry). The columns in this example are name, age, country. In other words the values between the commas. So each column in the line is stored in an array.

Then the needed text for xml is just wrapped around the values and the xml line is appended to the output file with echo.
