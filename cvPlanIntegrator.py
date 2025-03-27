import pyodbc
import sys
import pandas as pd
import configparser
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL
from sqlalchemy import create_engine
from sqlmodels import JobInfo, PlanBuilder, PlanProject, Rooms, Cabinets
from PyQt6.QtWidgets import QApplication, QMainWindow
from CVPlanUploader import Ui_MainWindow

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

        #Setting up dropdown values
        self.customer_drop_downs = []
        self.project_drop_downs = []
        self.plan_drop_downs = []
        self.eo_drop_downs = []

        #Adding default values to dropdowns
        self.ui.builderDropdown.addItem("None")
        self.ui.projectDropdown.addItem("None")
        self.ui.planDropdown.addItem("None")
        self.ui.eoDropdown.addItem("None")

        #Setting up Job Variables
        self.job_id = ''
        self.job_name = ''
        self.cvj_exists = False
        self.drop_down_values = []
        
        self.newPlan = False
        self.newEO = False
        self.newProject = False
        self.newBuilder = False

        #Hide status label
        self.ui.statusLabel.hide()

        #Connecting function to buttons
        self.ui.addPlan.clicked.connect(self.planButton)
        self.ui.addEO.clicked.connect(self.EOButton)
        self.ui.addProject.clicked.connect(self.projectButton)
        self.ui.addBuilder.clicked.connect(self.builderButton)
        self.ui.submitCVJ.clicked.connect(self.pushTables)
        
        #Connecting method to combobox
        self.ui.builderDropdown.activated.connect(self.selectBuilder)
        self.ui.projectDropdown.activated.connect(self.selectProject)
        self.ui.eoDropdown.activated.connect(self.selectEO)

        self.ui.planInput.hide()
        self.ui.projectInput.hide()
        self.ui.builderInput.hide()
        self.ui.eoInput.hide()

        self.retrieveTables()
        self.retrieveBuilders()

    def fetchDropDowns(self, query, params=[]):
        try:
            connection = pyodbc.connect(server_string)
            cursor = connection.cursor()

            if(len(params) > 0):
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            dropDownValues = cursor.fetchall()
        except pyodbc.Error as e:
            print(f"Error: {e}")

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
        
        return dropDownValues

    def retrieveBuilders(self):
        self.ui.builderDropdown.clear()
        try:
            query = """SELECT planBuilderID, builderName
                       FROM [PlanBuilder]"""
            customers = self.fetchDropDowns(query)
        except pyodbc.Error as e:
            print(f"Error: {e}")

        if len(customers) > 0:
            self.customer_drop_downs = customers
            self.ui.builderDropdown.addItem("None")
            self.ui.builderDropdown.addItems([item[1] for item in customers])

    def selectBuilder(self, index):
        try:
            query = """SELECT planProjectID, projectName, planBuilderIDFK
                       FROM [PlanProject]
                       WHERE planBuilderIDFK = ?"""
            projects = self.fetchDropDowns(query, [self.customer_drop_downs[index - 1][0]])

        except pyodbc.Error as e:
            print(f"Error: {e}")

        self.ui.projectDropdown.clear()
        self.ui.planDropdown.clear()
        self.ui.projectDropdown.addItem("None")
        self.ui.planDropdown.addItem("None")
        
        if(index == 0):
            return

        if len(projects) > 0:
            self.project_drop_downs = projects
            self.ui.projectDropdown.addItems([item[1] for item in projects])

    def selectProject(self, index):
        try:
            query = """ SELECT eoID, eoPhase, planProjectIDFK
                       FROM [PlanEO]
                       WHERE planProjectIDFK = ? """
            eos = self.fetchDropDowns(query, [self.project_drop_downs[index - 1][0]])

        except pyodbc.Error as e:
            print(f"Error: {e}")

        self.ui.planDropdown.clear()
        self.ui.planDropdown.addItem("None")
        self.ui.eoDropdown.clear()
        self.ui.eoDropdown.addItem("None")

        if(index == 0):
            return

        if len(eos) > 0:
            self.eo_drop_downs = eos
            self.ui.eoDropdown.addItems([item[1] for item in eos])

    def selectEO(self, index):
        try:
            query = """SELECT jobInfoID, planNumber, [Job Name]
                       FROM [CV_JobInfo]
                       WHERE eoIDFK = ?"""
            plans = self.fetchDropDowns(query, [self.eo_drop_downs[index - 1][0]])

        except pyodbc.Error as e:
            print(f"Error: {e}")

        self.ui.planDropdown.clear()
        self.ui.planDropdown.addItem("None")

        if(index == 0):
            return

        if len(plans) > 0:
            self.plan_drop_downs = plans
            self.ui.planDropdown.addItems([item[1] for item in plans])

    def dropDownSelect(self, index):
        self.cvj_exists = self.drop_down_values[index][2] is not None
        self.updateCVJStatus(self.cvj_exists)

    def updateCVJStatus(self, cvj_exists):
        if cvj_exists:
            text = "CVJ Exists"
            color = '#d9a03e'
        else:
            text = "No CVJ"
            color = '#57d911'
        
        self.ui.cvjStatusLabel.setText(text)
        self.ui.cvjStatusLabel.setStyleSheet(f"color: {color}")

    def builderButton(self):
        if(not self.newBuilder):
            self.switchBuilderWidget(True)
            self.switchProjectWidget(True)
            self.switchPlanWidget(True)
            self.switchEOWidget(True)

            self.ui.addEO.hide()
            self.ui.addProject.hide()
            self.ui.addPlan.hide()
        else:
            self.switchBuilderWidget(False)
            self.switchProjectWidget(False)
            self.switchPlanWidget(False)
            self.switchEOWidget(False)

            self.ui.addEO.show()
            self.ui.addProject.show()
            self.ui.addPlan.show()

    def projectButton(self):
        if(not self.newProject):
            self.switchProjectWidget(True)
            self.switchPlanWidget(True)
            self.switchEOWidget(True)

            self.ui.addEO.hide()
            self.ui.addPlan.hide()
        else:
            self.switchProjectWidget(False)
            self.switchPlanWidget(False)
            self.switchEOWidget(False)

            self.ui.addEO.show()
            self.ui.addPlan.show()

    def EOButton(self):
        if(not self.newEO):
            self.switchEOWidget(True)
            self.switchPlanWidget(True)

            self.ui.addPlan.hide()
        else:
            self.switchEOWidget(False)
            self.switchPlanWidget(False)

            self.ui.addPlan.show()

    def planButton (self):
        if(not self.newPlan):
            self.switchPlanWidget(True)
        else:
            self.switchPlanWidget(False)
    
    def switchBuilderWidget(self, newBuilder):
        self.ui.addBuilder.show()

        if(newBuilder):
            self.ui.builderDropdown.hide()
            self.ui.builderInput.show()
            self.ui.addBuilder.setText("Select Builder")
        else:
            self.ui.builderDropdown.show()
            self.ui.builderInput.hide()
            self.ui.addBuilder.setText("Add Builder")

        self.ui.builderInput.setText("")
        self.newBuilder = newBuilder

    def switchProjectWidget(self, newProject):
        self.ui.addProject.show()

        if(newProject):
            self.ui.projectDropdown.hide()
            self.ui.projectInput.show()
            self.ui.addProject.setText("Select Project")
        else:
            self.ui.projectDropdown.show()
            self.ui.projectInput.hide()
            self.ui.addProject.setText("Add Project")

        self.ui.projectInput.setText("")
        self.newProject = newProject

    def switchEOWidget(self, newEO):
        self.ui.addEO.show()

        if(newEO):
            self.ui.eoDropdown.hide()
            self.ui.eoInput.show()
            self.ui.addEO.setText("Select EO")
        else:
            self.ui.eoDropdown.show()
            self.ui.eoInput.hide()
            self.ui.addEO.setText("Add EO")

        self.ui.projectInput.setText("")
        self.newEO = newEO

    def switchPlanWidget(self, newPlan):
        self.ui.addPlan.show()

        if(newPlan):
            self.ui.planDropdown.hide()
            self.ui.planInput.show()
            self.ui.addPlan.setText("Select Plan")
        else:
            self.ui.planDropdown.show()
            self.ui.planInput.hide()
            self.ui.addPlan.setText("Add Plan")
        
        self.ui.planInput.setText("")
        self.newPlan = newPlan

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
        builderIndex = self.ui.builderDropdown.currentIndex() - 1
        projectIndex = self.ui.projectDropdown.currentIndex() - 1
        planIndex = self.ui.planDropdown.currentIndex() - 1
        
        plan_builder_id = None
        with server_engine.begin() as conn:
            roomID_dict = {}
            cabinetID_dict = {}

            if(self.newBuilder):
                plan_builder_session = server_session.merge(PlanBuilder(builderName=self.ui.builderInput.text()))
                server_session.flush()
                plan_builder_id = plan_builder_session.planBuilderID
            else:
                selected_builder = self.customer_drop_downs[builderIndex]
                plan_builder_id = selected_builder[0]



            if(self.newProject):
                #Adding PlanProject row
                plan_project_session = server_session.merge(PlanProject(planBuilderIDFK=plan_builder_id, projectName=self.ui.projectInput.text()))
                server_session.flush()
                plan_project_id = plan_project_session.planProjectID

                self.job_info.insert(1, "planProjectIDFK", [plan_project_id], True)
            else:
                selected_project = self.project_drop_downs[projectIndex]
                self.job_info.insert(1, "planProjectIDFK", [selected_project[0]], True)


            if(self.newPlan):
                self.job_info.insert(1, "planNumber", [self.ui.planInput.text()], True)
            else:
                retrieved_job_info = self.plan_drop_downs[planIndex]
                selected_plan = self.plan_drop_downs[planIndex]
                
                self.job_info.insert(1, "planNumber", [selected_plan[1]], True)
                with server_engine.begin() as conn:
                    #Delete JobInfo and all associated rows for non bid
                    #conn.execute(sa.text(f"EXEC delete_CVJ @lotID = {lotID};"))

                    #Delete Bid and all associated rows
                    conn.execute(sa.text(f"EXEC delete_CVJBid @jobInfoID = {retrieved_job_info[0]};"))
                    conn.commit()

            #Adding JobInfo to Table
            #If linking Job Info to lot
            #self.job_info.insert(1, "lotIDFK", [lotID], True)

            #When adding new plan
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
            self.parts["Quantity"] = self.parts.groupby(['Cabinet ID', 'Part ID', 'Width', 'Length'])['Cabinet ID'].transform('size')
            unique_parts = self.parts.drop_duplicates(subset=['Cabinet ID', 'Part ID', 'Width', 'Length'], keep='first').copy()
            print(unique_parts)
            unique_parts["jobInfoIDFK"] = job_info_id
            unique_parts["cabinetIDFK"] = self.parts["Cabinet ID"].map(cabinetID_dict)
            unique_parts = unique_parts.drop(columns=["Cabinet ID", "Image", "IntBandMaterial", "IntBandColor", "ExtBandMaterial", "ExtBandColor", "DoorBandMaterial", "DoorBandColor", "TextureFace", "TextureBack", "TextureEdge", "Parameters"])
            unique_parts.to_sql("CV_Parts", server_engine, if_exists="append", index=False)

            """ print(self.parts)
            self.parts["jobInfoIDFK"] = job_info_id
            self.parts["cabinetIDFK"] = self.parts["Cabinet ID"].map(cabinetID_dict)
            self.parts = self.parts.drop(columns=["Cabinet ID", "Image", "IntBandMaterial", "IntBandColor", "ExtBandMaterial", "ExtBandColor", "DoorBandMaterial", "DoorBandColor", "TextureFace", "TextureBack", "TextureEdge", "Parameters"])
            self.parts.to_sql("CV_Parts", server_engine, if_exists="append", index=False) """
            print("Finished Adding Parts")

            #Reset Tables

            self.retrieveBuilders()
            self.retrieveTables()
            self.resetDropDowns()
    
    def resetDropDowns(self):
        #Change inputs and dropdowns
        self.switchBuilderWidget(False)
        self.switchPlanWidget(False)
        self.switchProjectWidget(False)

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('config.ini')

    prodServer = config['DEFAULT']['prodServer']
    reportURL = config['DEFAULT']['reportURL']

    #Database connections
    server_string = f"server={prodServer};Database=EXCELCVJ;Trusted_Connection=Yes;Driver={{ODBC Driver 17 for SQL Server}}"
    server_url = URL.create("mssql+pyodbc", query={"odbc_connect": server_string})
    server_engine = create_engine(server_url)

    Server_session = sessionmaker(bind=server_engine)
    server_session = Server_session()

    cv_string = r"server=ECSERVER\SOLID;Database=CVData_2021;Trusted_Connection=Yes;Driver={ODBC Driver 17 for SQL Server}"
    cv_url = URL.create("mssql+pyodbc", query={"odbc_connect": cv_string})
    cv_engine = create_engine(cv_url)

    report_string = f"DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={reportURL}"
    report_url = URL.create("access+pyodbc", query={"odbc_connect": report_string})
    report_engine = create_engine(report_url)


    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())
