package model

import "gorm.io/gorm"

type MissionRepository interface {
	CreateMission(mission *Mission) error
	GetAllMissions() ([]Mission, error)
	GetMissionByCodename(codename string) (*Mission, error)
	GetMissionByID(id string) (*Mission, error)
	UpdateMission(mission *Mission) error
	DeleteMissionByID(id string) error

	CreateMissionLogEntry(entry *MissionLogEntry) error
	GetMissionLogEntryByID(id string) (*MissionLogEntry, error)
	GetMissionLogEntriesByMissionID(missionID string) ([]MissionLogEntry, error)

	CreateSystem(system *System) error
	GetAllSystems() ([]System, error)
	GetSystemByID(id string) (*System, error)
	UpdateSystem(system *System) error
	DeleteSystemByID(id string) error

	CreatePlanet(planet *Planet) error
	GetAllPlanets() ([]Planet, error)
	GetAllPlanetsBySystemID(systemID string) ([]Planet, error)
	GetPlanetByID(id string) (*Planet, error)
	UpdatePlanet(planet *Planet) error
	DeletePlanetByID(id string) error

	CreateDiscovery(discovery *Discovery) error
	GetAllDiscoveries() ([]Discovery, error)
	GetAllDiscoveriesByMissionID(missionID string) ([]Discovery, error)
	GetAllDiscoveriesByPlanetID(planetID string) ([]Discovery, error)
	GetAllDiscoveriesBySystemID(systemID string) ([]Discovery, error)
	UpdateDiscovery(discovery *Discovery) error
	DeleteDiscoveryByID(id string) error

	CreateBase(base *Base) error
	GetBaseByID(id string) (*Base, error)
	GetBaseByName(name string) (*Base, error)
	GetAllBases() ([]Base, error)
	UpdateBase(base *Base) error
	DeleteBaseByID(id string) error
}

// implement the MissionRepository interface with the gorm models

type missionRepositoryImpl struct {
	db *gorm.DB
}

func NewMissionRepository(db *gorm.DB) MissionRepository {
	return &missionRepositoryImpl{
		db: db,
	}
}

func (r *missionRepositoryImpl) CreateMission(mission *Mission) error {
	// Create mission
	if err := r.db.Create(&mission).Error; err != nil {
		return err
	}
	return nil
}

func (r *missionRepositoryImpl) GetAllMissions() ([]Mission, error) {
	// retrieve all missions
	var missions []Mission
	if err := r.db.Find(&missions).Error; err != nil {
		return nil, err
	}

	return missions, nil
}

func (r *missionRepositoryImpl) GetMissionByCodename(codename string) (*Mission, error) {
	// retrieve mission by codename
	var mission Mission
	if err := r.db.First(&mission, "codename = ?", codename).Error; err != nil {
		return nil, err
	}
	return &mission, nil
}

func (r *missionRepositoryImpl) GetMissionByID(id string) (*Mission, error) {
	// retreive mission by id
	var mission Mission
	if err := r.db.First(&mission, "id = ?", id).Error; err != nil {
		return nil, err
	}
	return &mission, nil
}

func (r *missionRepositoryImpl) UpdateMission(mission *Mission) error {
	// update the mission
	if err := r.db.Save(&mission).Error; err != nil {
		return err
	}
	return nil
}

func (r *missionRepositoryImpl) DeleteMissionByID(id string) error {
	// delete the mission
	if err := r.db.Delete(&Mission{}, "id = ?", id).Error; err != nil {
		return err
	}
	return nil
}

func (r *missionRepositoryImpl) CreateMissionLogEntry(entry *MissionLogEntry) error {
	// create mission log entry
	if err := r.db.Create(&entry).Error; err != nil {
		return err
	}
	return nil
}

func (r *missionRepositoryImpl) GetMissionLogEntryByID(id string) (*MissionLogEntry, error) {
	// get mission log entry by id
	var missionLogEntry MissionLogEntry
	if err := r.db.First(&missionLogEntry, "id = ?", id).Error; err != nil {
		return nil, err
	}
	return &missionLogEntry, nil

}

func (r *missionRepositoryImpl) GetMissionLogEntriesByMissionID(missionID string) ([]MissionLogEntry, error) {
	//  get all the mission log entries by mission id
	var missionLogEntries []MissionLogEntry
	if err := r.db.Find(&missionLogEntries, "mission_id = ?", missionID).Error; err != nil {
		return nil, err
	}
	return missionLogEntries, nil
}

func (r *missionRepositoryImpl) CreateSystem(system *System) error {
	// create a system
	if err := r.db.Create(&system).Error; err != nil {
		return err
	}
	return nil
}

func (r *missionRepositoryImpl) GetAllSystems() ([]System, error) {
	// retrive all systems
	var systems []System
	if err := r.db.Find(&systems).Error; err != nil {
		return nil, err
	}
	return systems, nil
}

func (r *missionRepositoryImpl) GetSystemByID(id string) (*System, error) {
	// get system by id
	var system System
	if err := r.db.First(&system, "id = ?", id).Error; err != nil {
		return nil, err
	}
	return &system, nil
}

func (r *missionRepositoryImpl) UpdateSystem(system *System) error {
	// update the system
	if err := r.db.Save(&system).Error; err != nil {
		return err
	}
	return nil
}

func (r *missionRepositoryImpl) DeleteSystemByID(id string) error {
	// delete the system
	if err := r.db.Delete(&System{}, "id = ?", id).Error; err != nil {
		return err
	}
	return nil
}

func (r *missionRepositoryImpl) CreatePlanet(planet *Planet) error {
	// create a planet
	if err := r.db.Create(&planet).Error; err != nil {
		return err
	}
	return nil
}

func (r *missionRepositoryImpl) GetAllPlanets() ([]Planet, error) {
	// retrieve all planets
	var planets []Planet
	if err := r.db.Find(&planets).Error; err != nil {
		return nil, err
	}
	return planets, nil
}

func (r *missionRepositoryImpl) GetAllPlanetsBySystemID(systemID string) ([]Planet, error) {
	// retrieve all planets by system id
	var planets []Planet
	if err := r.db.Find(&planets, "system_id = ?", systemID).Error; err != nil {
		return nil, err
	}
	return planets, nil
}

func (r *missionRepositoryImpl) GetPlanetByID(id string) (*Planet, error) {
	// get planet by id
	var planet Planet
	if err := r.db.First(&planet, "id = ?", id).Error; err != nil {
		return nil, err
	}
	return &planet, nil
}

func (r *missionRepositoryImpl) UpdatePlanet(planet *Planet) error {
	// update the planet
	if err := r.db.Save(&planet).Error; err != nil {
		return err
	}
	return nil
}

func (r *missionRepositoryImpl) DeletePlanetByID(id string) error {
	// delete the planet
	if err := r.db.Delete(&Planet{}, "id = ?", id).Error; err != nil {
		return err
	}
	return nil
}

func (r *missionRepositoryImpl) CreateDiscovery(discovery *Discovery) error {
	// create a discovery
	if err := r.db.Create(&discovery).Error; err != nil {
		return err
	}
	return nil
}

func (r *missionRepositoryImpl) GetAllDiscoveries() ([]Discovery, error) {
	// retrieve all discoveries
	var discoveries []Discovery
	if err := r.db.Find(&discoveries).Error; err != nil {
		return nil, err
	}
	return discoveries, nil
}

func (r *missionRepositoryImpl) GetAllDiscoveriesByMissionID(missionID string) ([]Discovery, error) {
	// retrieve all discoveries by mission id
	var discoveries []Discovery
	if err := r.db.Find(&discoveries, "mission_id = ?", missionID).Error; err != nil {
		return nil, err
	}
	return discoveries, nil
}

func (r *missionRepositoryImpl) GetAllDiscoveriesByPlanetID(planetID string) ([]Discovery, error) {
	// retrieve all discoveries by planet id
	var discoveries []Discovery
	if err := r.db.Find(&discoveries, "planet_id = ?", planetID).Error; err != nil {
		return nil, err
	}
	return discoveries, nil
}

func (r *missionRepositoryImpl) GetAllDiscoveriesBySystemID(systemID string) ([]Discovery, error) {
	// retrieve all discoveries by system id
	var discoveries []Discovery
	if err := r.db.Find(&discoveries, "system_id = ?", systemID).Error; err != nil {
		return nil, err
	}
	return discoveries, nil
}

func (r *missionRepositoryImpl) UpdateDiscovery(discovery *Discovery) error {
	// update the discovery
	if err := r.db.Save(&discovery).Error; err != nil {
		return err
	}
	return nil
}

func (r *missionRepositoryImpl) DeleteDiscoveryByID(id string) error {
	// delete the discovery
	if err := r.db.Delete(&Discovery{}, "id = ?", id).Error; err != nil {
		return err
	}
	return nil
}

func (r *missionRepositoryImpl) CreateBase(base *Base) error {
	// create a base
	if err := r.db.Create(&base).Error; err != nil {
		return err
	}
	return nil
}

func (r *missionRepositoryImpl) GetBaseByID(id string) (*Base, error) {
	// get base by id
	var base Base
	if err := r.db.First(&base, "id = ?", id).Error; err != nil {
		return nil, err
	}
	return &base, nil
}

func (r *missionRepositoryImpl) GetBaseByName(name string) (*Base, error) {
	// get base by name
	var base Base
	if err := r.db.First(&base, "base_name = ?", name).Error; err != nil {
		return nil, err
	}
	return &base, nil
}

func (r *missionRepositoryImpl) GetAllBases() ([]Base, error) {
	// retrieve all bases
	var bases []Base
	if err := r.db.Find(&bases).Error; err != nil {
		return nil, err
	}
	return bases, nil
}

func (r *missionRepositoryImpl) UpdateBase(base *Base) error {
	// update the base
	if err := r.db.Save(&base).Error; err != nil {
		return err
	}
	return nil
}

func (r *missionRepositoryImpl) DeleteBaseByID(id string) error {
	// delete the base
	if err := r.db.Delete(&Base{}, "id = ?", id).Error; err != nil {
		return err
	}
	return nil
}
