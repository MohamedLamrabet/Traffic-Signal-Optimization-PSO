### Creating a MySQL Database
1. Install WAMP or XAMPP for Windows, or LAMP for Linux. 
2. Create a MySQL database named `traffic` and import the SQL file located at `database/traffic.sql`

### Running the SUMO Project
1. Install SUMO software.
2. Install Python version 3.10 or higher. 
3. Set current directory where the project exists then to "scripts" and run the following command: `py traciinterface.py`

### Visualize the results of the simulation using Metabase
1. Verify that Java is installed on your computer.
2. Download the Metabase jar file from this link: https://www.metabase.com/start/oss/jar and place it in the metabase folder.
3. Run Metabase using the following command: `java -jar metabase.jar`
4. After metabase run, to view the simulation results, go to this link: : http://localhost:3000/dashboard/1-simulation-results using these credentials:
* **Login**: admin@admin.com 
* **Password**: Admin@0123
