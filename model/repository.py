from sqlalchemy import create_engine, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime
from dbmodels import Mission, Base


# Define the SQLAlchemy engine
#engine = create_engine('sqlite:///nmscommand.db', echo=True)
engine = create_engine('sqlite:///:memory:', echo=True)

# Create the database tables
Base.metadata.create_all(engine)

# Define a function to create a new session
def create_session():
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

# Example CRUD operations

# Create
def create_mission(session, codename, description, start_date, end_date, stage, milestones, swag, tech, resources, media):
    new_mission = Mission(
        codename=codename,
        description=description,
        start_date=start_date,
        end_date=end_date,
        stage=stage,
        milestones=milestones,
        swag=swag,
        tech=tech,
        resources=resources,
        media=media
    )
    session.add(new_mission)
    session.commit()
    return new_mission

# Read
def get_mission_by_codename(session, codename):
    mission = session.query(Mission).filter_by(codename=codename).first()
    return mission

# Update
def update_mission_stage(session, codename, new_stage):
    mission = get_mission_by_codename(session, codename)
    if mission:
        mission.stage = new_stage
        session.commit()

# Delete
def delete_mission(session, codename):
    mission = get_mission_by_codename(session, codename)
    if mission:
        session.delete(mission)
        session.commit()

# Example usage
if __name__ == "__main__":
    print("Running example usage")
    # Create a session
    session = create_session()
    
    # Create a new mission
    new_mission = create_mission(session,
                                 codename="Mission1",
                                 description="First mission",
                                 start_date=datetime.now(),
                                 end_date=datetime.now(),
                                 stage=1,
                                 milestones=["milestone1", "milestone2"],
                                 swag=["swag1", "swag2"],
                                 tech=["tech1", "tech2"],
                                 resources=["resource1", "resource2"],
                                 media=["media1", "media2"])

    # Read the mission
    mission = get_mission_by_codename(session, "Mission1")
    print("Mission:", mission.codename, mission.description)

    # Update the mission stage
    update_mission_stage(session, "Mission1", 2)

    # Read the updated mission
    mission = get_mission_by_codename(session, "Mission1")
    print("Updated Stage:", mission.stage)

    # Delete the mission
    delete_mission(session, "Mission1")

    # Close the session
    session.close()
