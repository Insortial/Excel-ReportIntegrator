from sqlalchemy import Column, Integer, String, Float, SmallInteger, Boolean, LargeBinary
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class PlanBuilder(Base):
    __tablename__ = 'PlanBuilder'  # SQL table name

    planBuilderID = Column(Integer, primary_key=True, autoincrement=True)  # Primary key column
    builderName = Column(String(100), nullable=False)

class PlanEO(Base):
    __tablename__ = 'PlanEO'  # SQL table name

    eoID = Column(Integer, primary_key=True, autoincrement=True)  # Primary key column
    planProjectIDFK = Column(Integer, nullable=False)
    eoPhase = Column(String(10), nullable=False)

class PlanProject(Base):
    __tablename__ = 'PlanProject'  # SQL table name

    planProjectID = Column(Integer, primary_key=True, autoincrement=True)  # Primary key column
    planBuilderIDFK = Column(Integer, nullable=False)
    projectName = Column(String(50), nullable=False)

class JobInfo(Base):
    __tablename__ = 'CV_JobInfo'  # SQL table name

    jobInfoID = Column(Integer, primary_key=True, autoincrement=True)  # Primary key column
    lotIDFK = Column(Integer, nullable=True)
    eoIDFK = Column(Integer, nullable=True)
    planNumber = Column(String(50), nullable=True)
    Job_Name = Column("Job Name", String(128), nullable=True)
    Job_Number = Column("Job Number", String(50), nullable=True)
    Key_Name = Column("Key Name", String(50), nullable=True)
    Customer_ID = Column("Customer ID", Integer, nullable=True)
    Customer_Name = Column("Customer Name", String(50), nullable=True)
    Customer_Address = Column("Customer Address", String(102), nullable=True)

class Rooms(Base):
    __tablename__ = 'CV_Rooms'  # SQL table name

    RoomID = Column(Integer, primary_key=True, autoincrement=True)
    jobInfoIDFK = Column(Integer, nullable=False)
    RoomNumber = Column(Integer, nullable=True)
    RoomName = Column(String(50), nullable=True)
    RoomDescription = Column(String(255), nullable=True)
    Quantity = Column(SmallInteger, nullable=True)
    WallCount = Column(SmallInteger, nullable=True)
    ExtAsmFin = Column(String(30), nullable=True)
    IntAsmFin = Column(String(30), nullable=True)
    TopFin = Column(String(30), nullable=True)
    SplashFin = Column(String(30), nullable=True)
    CrownFin = Column(String(30), nullable=True)
    LightRailFin = Column(String(30), nullable=True)
    BaseBoardFin = Column(String(30), nullable=True)
    ChairRailFin = Column(String(30), nullable=True)
    CeilingFin = Column(String(30), nullable=True)
    EDoorFin = Column(String(30), nullable=True)
    WindowFin = Column(String(30), nullable=True)
    CabinetConstruction = Column(String(50), nullable=True)
    DrawerBoxConstruction = Column(String(50), nullable=True)
    RollOutConstruction = Column(String(50), nullable=True)
    BaseCabinetMaterials = Column(String(50), nullable=True)
    BaseExposedCabinetMaterials = Column(String(50), nullable=True)
    WallCabinetMaterials = Column(String(50), nullable=True)
    WallExposedCabinetMaterials = Column(String(50), nullable=True)
    DrawerBoxMaterials = Column(String(50), nullable=True)
    RollOutMaterials = Column(String(50), nullable=True)
    PullMaterials = Column(String(50), nullable=True)
    HingeMaterials = Column(String(50), nullable=True)
    GuideMaterials = Column(String(50), nullable=True)
    WallDoorName = Column(String(50), nullable=True)
    WallDoorMaterial = Column(String(50), nullable=True)
    DrawerFrontName = Column(String(50), nullable=True)
    DrawerFrontMaterial = Column(String(50), nullable=True)
    BaseDoorName = Column(String(50), nullable=True)
    BaseDoorMaterial = Column(String(50), nullable=True)
    WallEndPanelName = Column(String(50), nullable=True)
    WallEndPanelMaterial = Column(String(50), nullable=True)
    BaseEndPanelName = Column(String(50), nullable=True)
    BaseEndPanelMaterial = Column(String(50), nullable=True)
    TallEndPanelName = Column(String(50), nullable=True)
    TallEndPanelMaterial = Column(String(50), nullable=True)
    ClosetAssemblyConstruction = Column(String(50), nullable=True)
    ClosetDrawerBoxConstruction = Column(String(50), nullable=True)
    ClosetRollOutConstruction = Column(String(50), nullable=True)
    ClosetAssemblyMaterials = Column(String(50), nullable=True)
    ClosetDrawerBoxMaterials = Column(String(50), nullable=True)
    ClosetRollOutMaterials = Column(String(50), nullable=True)
    ClosetPullMaterials = Column(String(50), nullable=True)
    ClosetHingeMaterials = Column(String(50), nullable=True)
    ClosetGuideMaterials = Column(String(50), nullable=True)
    ClosetWireBasketMaterials = Column(String(50), nullable=True)
    ClosetWallDoorName = Column(String(50), nullable=True)
    ClosetWallDoorMaterial = Column(String(50), nullable=True)
    ClosetDrawerFrontName = Column(String(50), nullable=True)
    ClosetDrawerFrontMaterial = Column(String(50), nullable=True)
    ClosetBaseDoorName = Column(String(50), nullable=True)
    ClosetBaseDoorMaterial = Column(String(50), nullable=True)
    ClosetWallEndPanelName = Column(String(50), nullable=True)
    ClosetWallEndPanelMaterial = Column(String(50), nullable=True)
    ClosetBaseEndPanelName = Column(String(50), nullable=True)
    ClosetBaseEndPanelMaterial = Column(String(50), nullable=True)
    ClosetTallEndPanelName = Column(String(50), nullable=True)
    ClosetTallEndPanelMaterial = Column(String(50), nullable=True)
    CounterTopConstruction = Column(String(50), nullable=True)
    CounterTopMaterial = Column(String(50), nullable=True)
    CounterTopProfile = Column(String(50), nullable=True)
    CounterTopProfileMaterial = Column(String(50), nullable=True)
    CrownProfile = Column(String(50), nullable=True)
    CrownProfileMaterial = Column(String(50), nullable=True)
    LightRailProfile = Column(String(50), nullable=True)
    LightRailProfileMaterial = Column(String(50), nullable=True)
    ScribeProfile = Column(String(50), nullable=True)
    ScribeProfileMaterial = Column(String(50), nullable=True)
    BaseBoardProfile = Column(String(50), nullable=True)
    BaseBoardProfileMaterial = Column(String(50), nullable=True)
    ChairRailProfile = Column(String(50), nullable=True)
    ChairRailProfileMaterial = Column(String(50), nullable=True)
    CasingProfile = Column(String(50), nullable=True)
    CasingProfileMaterial = Column(String(50), nullable=True)
    AppliedProfile = Column(String(50), nullable=True)
    AppliedProfileMaterial = Column(String(50), nullable=True)
    CeilingProfile = Column(String(50), nullable=True)
    CeilingProfileMaterial = Column(String(50), nullable=True)

class Cabinets(Base):
    __tablename__ = 'CV_Cabinets' 

    Cabinet_ID = Column("Cabinet ID", Integer,  primary_key=True, autoincrement=True)
    roomIDFK = Column(Integer, nullable=True)
    Wall_ID = Column("Wall ID", Integer, nullable=True)
    cabinetNumber = Column(Integer, nullable=True)
    Width = Column(Float, nullable=True)
    Width_String = Column("Width String", String(12), nullable=True)
    Height = Column(Float, nullable=True)
    Height_String = Column("Height String", String(12), nullable=True)
    Depth = Column(Float, nullable=True)
    Depth_String = Column("Depth String", String(12), nullable=True)
    Cabinet_Name = Column("Cabinet Name", String(50), nullable=True)
    Cabinet_Type = Column("Cabinet Type", SmallInteger, nullable=True)
    Cabinet_Style = Column("Cabinet Style", SmallInteger, nullable=True)
    Left_Scribe = Column("Left Scribe", Float, nullable=True)
    Left_Scribe_String = Column("Left Scribe String", String(12), nullable=True)
    Right_Scribe = Column("Right Scribe", Float, nullable=True)
    Right_Scribe_String = Column("Right Scribe String", String(12), nullable=True)
    Left_End = Column("Left End", String(20), nullable=True)
    Right_End = Column("Right End", String(20), nullable=True)
    Back = Column(String(20), nullable=True)
    Toe_Height = Column("Toe Height", Float, nullable=True)
    Toe_Height_String = Column("Toe Height String", String(12), nullable=True)
    Toe_Recess = Column("Toe Recess", Float, nullable=True)
    Toe_Recess_String = Column("Toe Recess String", String(12), nullable=True)
    Soffit_Height = Column("Soffit Height", Float, nullable=True)
    Soffit_Height_String = Column("Soffit Height String", String(12), nullable=True)
    Elevation = Column(Float, nullable=True)
    Elevation_String = Column("Elevation String", String(12), nullable=True)
    Finished_Area = Column("Finished Area", Float, nullable=True)
    Assembly_Labor = Column("Assembly Labor", Float, nullable=True)
    Additional_Labor = Column("Additional Labor", Float, nullable=True)
    Cabinet_Face = Column("Cabinet Face", Integer, nullable=True)
    Retail = Column(Boolean, nullable=True)
    Stock = Column(Boolean, nullable=True)
    Openings = Column(SmallInteger, nullable=True)
    CustomPrice = Column(Float, nullable=True)
    Quantity = Column(SmallInteger, nullable=True)
    Comment = Column(String(5000), nullable=True)
    Hinge = Column(String(1), nullable=True)
    Description = Column(String(255), nullable=True)
    Assembly = Column(String(5000), nullable=True)
    Catalog = Column(String(128), nullable=True)
    CvcAsmID = Column(Integer, nullable=True)
    #SSMA_TimeStamp = Column(LargeBinary, nullable=True)