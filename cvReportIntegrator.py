import pyodbc
import sys
import pandas as pd
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL
from sqlalchemy import create_engine
from sqlmodels import JobInfo, Rooms, Cabinets
from PyQt6 import QtCore, uic, QtGui
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QVBoxLayout, QLineEdit, QMainWindow
from CVJobUploader import Ui_MainWindow

#Database connections
server_string = r"server=RENQ-PC\CV;Database=EXCELP&D;Trusted_Connection=Yes;Driver={ODBC Driver 17 for SQL Server}"
server_url = URL.create("mssql+pyodbc", query={"odbc_connect": server_string})
server_engine = create_engine(server_url)

Server_session = sessionmaker(bind=server_engine)
server_session = Server_session()

cv_string = r"server=ECSERVER\SOLID;Database=CVData_2021;Trusted_Connection=Yes;Driver={ODBC Driver 17 for SQL Server}"
cv_url = URL.create("mssql+pyodbc", query={"odbc_connect": cv_string})
cv_engine = create_engine(cv_url)

report_string = r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Cabinet Vision\Users\RenQ\report.mdb;"
report_url = URL.create("access+pyodbc", query={"odbc_connect": report_string})
report_engine = create_engine(report_url)

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        #Setting up Table Variables
        self.job_info = None
        self.room_info = None
        self.cabinet_info = None
        self.molding = None
        self.tops = None
        self.doors = None
        self.drawers = None
        self.rollouts = None
        self.sections = None
        self.scabinets = None
        self.parts = None
        self.cv_materials = None

        #Setting up Job Variables
        self.job_id = ''
        self.job_name = ''
        self.cvj_exists = False
        self.drop_down_values = []

        #Connecting function to buttons
        self.ui.jobIDSubmit.clicked.connect(self.retrieveJobID)
        """ self.ui.newPlanButton.clicked.connect(self.switchPlanWidget) """
        self.ui.submitCVJ.clicked.connect(self.pushTables)

        #Setting toggle for checkboxes
        self.ui.otherCheckBox.clicked.connect(lambda: self.toggleCheckBoxes(type='other'))
        self.ui.draftCheckBox.clicked.connect(lambda: self.toggleCheckBoxes(type='draft'))
        self.ui.standardCheckBox.clicked.connect(lambda: self.toggleCheckBoxes(type='standard'))
        
        #Connecting method to combobox
        self.ui.lotDropDown.activated.connect(self.dropDownSelect)

        #Hiding frame and error tag
        self.ui.frame.hide()
        self.ui.errorTag.hide()

        self.retrieveTables()

    def toggleCheckBoxes(self, type):
        if(type == 'standard'):
            self.ui.otherCheckBox.setChecked(False)
            self.ui.draftCheckBox.setChecked(False)
        elif(type == 'draft'):
            self.ui.standardCheckBox.setChecked(False)
            self.ui.otherCheckBox.setChecked(False)
        elif(type == 'other'):
            self.ui.draftCheckBox.setChecked(False)
            self.ui.standardCheckBox.setChecked(False)

    def dropDownSelect(self, index):
        self.cvj_exists = self.drop_down_values[index][1]
        self.updateCVJStatus(self.cvj_exists)

    def updateCVJStatus(self, status):
        if status:
            text = "CVJ Exists"
            color = '#d9a03e'
        else:
            text = "No CVJ"
            color = '#57d911'
        
        self.ui.cvjStatusLabel.setText(text)
        self.ui.cvjStatusLabel.setStyleSheet(f"color: {color}")

    """ def switchPlanWidget(self):
        if(not self.newPlan):
            self.ui.planInput.show()
            self.ui.lotDropDown.hide()
            self.ui.planInput.setText("")
            self.ui.newPlanButton.setText("Select Plan")
        else:
            self.ui.lotDropDown.show()
            self.ui.planInput.hide()
            self.ui.newPlanButton.setText("Add New Plan")
        
        self.newPlan = not self.newPlan """

    def retrieveJobID(self):
        self.job_id = self.ui.jobIDInput.text()

        try:
            connection = pyodbc.connect(r"server=RENQ-PC\CV;Database=EXCELP&D;Trusted_Connection=Yes;Driver={ODBC Driver 17 for SQL Server}")
            cursor = connection.cursor()

            query = """SELECT [Customer Name], [Project Name], [Phase] 
                       FROM [Jobs] AS J 
                       INNER JOIN [Projects] AS P ON P.[Project ID] = J.[Project IDFK] 
                       INNER JOIN [Customers] AS C ON C.[Customer ID] = P.[Customer IDFK]
                       WHERE [Job ID] = ?"""
            cursor.execute(query, self.job_id)

            job_details = cursor.fetchone()

            query = """
                        SELECT [Lot Number], [Lot ID], CJ.jobInfoID
                        FROM Lots AS L
                        LEFT JOIN CV_JobInfo AS CJ ON L.[Lot ID] = CJ.lotIDFK
                        WHERE [Job IDFK] = ?
                    """
            cursor.execute(query, self.job_id)

            lots = cursor.fetchall()
            print(lots)

        except pyodbc.Error as e:
            print(f"Error: {e}")

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
        if (job_details is None):
            self.ui.frame.hide()
        else:
            self.ui.frame.show()
            """ self.switchPlanWidget() """
            self.ui.jobLabel.setText(f"{job_details[0]} - {job_details[1]}")
            self.ui.phaseLabel.setText(f"Phase: {job_details[2]}")
            self.ui.lotDropDown.clear()
            if len(lots) > 0:
                self.drop_down_values = lots
                self.ui.lotDropDown.addItems([item[0] for item in lots])
                self.cvj_exists = lots[0][1] is not None
                self.updateCVJStatus(self.cvj_exists)

    def retrieveTables(self):
        with report_engine.begin() as conn:
            #Write code to recognize which version of CV we are using
            #If it is not CV2021 there should be a CxMaterials table that contains table names
            #If it is then we need to open a separate connection to the PSNC-CV.mdb file and open the Materials table there

            df = pd.read_sql_query(sa.text("SELECT * FROM [Job Info]"), conn)

            self.job_name = df['Job Name'][0]

            selected_columns = ["Job Number", "Job Name", "Key Name", "Customer ID", "Customer Name", "Customer Address"]
            df = df[selected_columns]
            df.rename(columns={
                "Job Number": "Job_Number",
                "Job Name": "Job_Name",
                "Key Name": "Key_Name",
                "Customer ID": "Customer_ID",
                "Customer Name": "Customer_Name",
                "Customer Address": "Customer_Address"
            }, inplace=True)
            self.job_info = df

            df = pd.read_sql_query(sa.text("SELECT * FROM [Rooms]"), conn)
            df = df.drop(columns=['Job ID', 'RoomID'])
            self.room_info = df

            df = pd.read_sql_query(sa.text("SELECT * FROM [Cabinets]"), conn)
            df.rename(columns={
                'Cabinet ID': 'cabinetNumber',
                "Wall ID": "Wall_ID",
                "Width String": "Width_String",
                "Height String": "Height_String",
                "Depth String": "Depth_String",
                "Cabinet Name": "Cabinet_Name",
                "Cabinet Type": "Cabinet_Type",
                "Cabinet Style": "Cabinet_Style",
                "Left Scribe": "Left_Scribe",
                "Left Scribe String": "Left_Scribe_String",
                "Right Scribe": "Right_Scribe",
                "Right Scribe String": "Right_Scribe_String",
                "Left End": "Left_End",
                "Right End": "Right_End",
                "Toe Height": "Toe_Height",
                "Toe Height String": "Toe_Height_String",
                "Toe Recess": "Toe_Recess",
                "Toe Recess String": "Toe_Recess_String",
                "Soffit Height": "Soffit_Height",
                "Soffit Height String": "Soffit_Height_String",
                "Elevation String": "Elevation_String",
                "Finished Area": "Finished_Area",
                "Assembly Labor": "Assembly_Labor",
                "Additional Labor": "Additional_Labor",
                "Cabinet Face": "Cabinet_Face"
            }, inplace=True)
            self.cabinet_info = df

            df = pd.read_sql_query(sa.text("SELECT * FROM [Molding]"), conn)
            self.molding = df

            df = pd.read_sql_query(sa.text("SELECT * FROM [Tops]"), conn)
            self.tops = df

            df = pd.read_sql_query(sa.text("SELECT * FROM [Doors]"), conn)
            self.doors = df

            df = pd.read_sql_query(sa.text("SELECT * FROM [Drawers]"), conn)
            self.drawers = df

            df = pd.read_sql_query(sa.text("SELECT * FROM [Rollouts]"), conn)
            df = df.drop(columns=['Image'])
            self.rollouts = df

            df = pd.read_sql_query(sa.text("SELECT * FROM [Sections]"), conn)
            self.sections = df

            df = pd.read_sql_query(sa.text("SELECT * FROM [Stock Cabinets]"), conn)
            self.scabinets = df

            df = pd.read_sql_query(sa.text("SELECT * FROM [Parts]"), conn)
            self.parts = df

            """ df = pd.read_sql_query(sa.text("SELECT C.Name, P.* FROM [Parts] AS P INNER JOIN [CxMaterial] AS C ON P.[Material ID] = C.ID"), conn)
            parts_df = df """

    def pushTables(self):
        #Determining size of materials given parts of a lot. Old PSNC Version

        #Determining size of materials given parts of a lot. Connection to CV_2021 on ecserver. Materials for cabinet vision 2021 can all be found on CVData_2021 but sizes are not stored there.
        #For CV11 it can be found on CxMaterials_12
        lotIndex = self.ui.lotDropDown.currentIndex()
        lot = self.drop_down_values[lotIndex][1]

        """ if(len(self.ui.lotDropDown.currentText()) == 0):
            self.ui.errorTag.show()
            return
        else:
            self.ui.errorTag.hide() """

        with server_engine.begin() as conn:
            #Delete JobInfo and all associated rows 
            conn.execute(sa.text(f"EXEC delete_CVJ @jobID = {self.job_id}, @plan = '{lot}';"))
            conn.commit()


        with server_engine.begin() as conn:
            roomID_dict = {}
            cabinetID_dict = {}

            #Adding JobInfo to Table
            self.job_info.insert(1, "lotIDFK", [planIDFK], True)
            for _, row in self.job_info.iterrows():
                job_info_session = server_session.merge(JobInfo(**row.to_dict()))
                server_session.flush()
                job_info_id = job_info_session.jobInfoID

            server_session.commit()
            print("Finished Adding JobInfo")   

            #Adding Rooms to Table
            self.room_info["jobInfoIDFK"] = job_info_id

            for _, row in self.room_info.iterrows():
                instance = server_session.merge(Rooms(**row.to_dict()))
                server_session.flush()
                roomID_dict[instance.RoomNumber] = instance.RoomID
                
            server_session.commit()
            print("Finished Adding Rooms")   

            #Adding Cabinets to Table
            self.cabinet_info["roomIDFK"] = self.cabinet_info["Room ID"].map(roomID_dict)
            self.cabinet_info = self.cabinet_info.drop(columns=['Room ID', 'Image'])

            for _, row in self.cabinet_info.iterrows():
                instance = server_session.merge(Cabinets(**row.to_dict())) 
                server_session.flush()
                cabinetID_dict[instance.cabinetNumber] = instance.Cabinet_ID
            cabinetID_dict[0] = 0
            server_session.commit()
            print("Finished Adding Cabinets")    

            #Adding Molding to Table
            self.molding["roomIDFK"] = self.molding["Room ID"].map(roomID_dict)
            self.molding = self.molding.drop(columns='Room ID')
            self.molding.to_sql("CV_Molding", server_engine, if_exists="append", index=False)
            print("Finished Adding Molding")

            #Adding Tops to Table
            self.tops["roomIDFK"] = self.tops["Room ID"].map(roomID_dict)
            self.tops = self.tops.drop(columns='Room ID')
            self.tops.to_sql("CV_Tops", server_engine, if_exists="append", index=False)
            print("Finished Adding Tops")

            #Adding Doors to Table
            self.doors["cabinetIDFK"] = self.doors["Cabinet ID"].map(cabinetID_dict)
            self.doors = self.doors.drop(columns=['Cabinet ID', 'Image'])
            self.doors.to_sql("CV_Doors", server_engine, if_exists="append", index=False)
            print("Finished Adding Doors")

            #Adding Drawers to Table
            self.drawers["cabinetIDFK"] = self.drawers["Cabinet ID"].map(cabinetID_dict)
            self.drawers = self.drawers.drop(columns='Cabinet ID')
            self.drawers.to_sql("CV_Drawers", server_engine, if_exists="append", index=False)
            print("Finished Adding Drawers")

            #Adding Rollouts to Table
            self.rollouts["cabinetIDFK"] = self.rollouts["Cabinet ID"].map(cabinetID_dict)
            self.rollouts = self.rollouts.drop(columns='Cabinet ID')
            self.rollouts.to_sql("CV_Rollouts", server_engine, if_exists="append", index=False)
            print("Finished Adding Rollouts")

            """ #Adding Sections to Table (NOT USABLE)
            sections.insert(0, "cabinetIDFK", cabinet_id, True)
            drawers = drawers.drop(columns='Cabinet ID')
            sections.to_sql("CV_Sections", server_engine, if_exists="append", index=False)
            print("Finished Adding Sections")"""

            #Adding Stock Cabinets to Table
            self.scabinets["cabinetIDFK"] = self.scabinets["SCabinet ID"].map(cabinetID_dict)
            self.scabinets = self.scabinets.drop(columns='SCabinet ID')
            self.scabinets.to_sql("CV_StockCabinets", server_engine, if_exists="append", index=False)
            print("Finished Adding Stock Cabinets")

            #Adding Parts to Table 
            self.parts["Quantity"] = self.parts.groupby(['Cabinet ID', 'Part ID'])['Cabinet ID'].transform('size')
            unique_parts = self.parts.drop_duplicates(subset=['Cabinet ID', 'Part ID'], keep='first').copy()
            print(unique_parts)
            unique_parts["jobInfoIDFK"] = job_info_id
            unique_parts["cabinetIDFK"] = self.parts["Cabinet ID"].map(cabinetID_dict)
            unique_parts = unique_parts.drop(columns=["Cabinet ID", "Image"])
            unique_parts.to_sql("CV_Parts", server_engine, if_exists="append", index=False)
            print("Finished Adding Parts")


            #Reset Tables
            self.retrieveTables()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())
