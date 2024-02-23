package model

import (
	"database/sql"
	"errors"
	"os"
	"testing"
	"time"

	"github.com/google/uuid"
	"gorm.io/gorm"
)

func TestMain(m *testing.M) {
	SetupDBDriver()

	exitVal := m.Run()

	os.Exit(exitVal)
}

func TestMissionCRUD(t *testing.T) {
	db := InitTestDB(DBTestFile)

	// Create a new mission
	mission := Mission{
		Codename:    "TestMission",
		Description: NewNullString("Test description"),
		StartDate:   sql.NullTime{Time: time.Now().UTC(), Valid: true},
		EndDate:     sql.NullTime{Time: time.Now().UTC().Add(time.Hour * 24 * 7), Valid: true}, // 7 days from now
		Stage:       Planning,
		Milestones: []ListItem{
			{Description: "Milestone 1", Completed: false},
			{Description: "Milestone 2", Completed: true},
		},
		Swag: []ListItem{
			{Description: "Swag 1", Completed: true},
		},
		Tech: []ListItem{
			{Description: "Tech 1", Completed: false},
		},
		Resources: []ListItem{
			{Description: "Resource 1", Completed: true},
		},
		Media: []string{"media1.jpg", "media2.jpg"},
	}
	if db == nil {
		t.Fatalf("Database connection is nil")
	}
	// Create mission
	if err := db.Create(&mission).Error; err != nil {
		t.Fatalf("Failed to create mission: %v", err)
	}

	// Retrieve mission
	var retrievedMission Mission
	if err := db.First(&retrievedMission, "codename = ?", "TestMission").Error; err != nil {
		t.Fatalf("Failed to retrieve mission: %v", err)
	}

	// Check retrieved mission fields
	if retrievedMission.Codename != mission.Codename {
		t.Errorf("Expected codename: %s, got: %s", mission.Codename, retrievedMission.Codename)
	}

	// You can continue checking other fields similarly

	// Update mission
	retrievedMission.Description = NewNullString("Updated description")
	if err := db.Save(&retrievedMission).Error; err != nil {
		t.Fatalf("Failed to update mission: %v", err)
	}

	var removeMission Mission
	if err := db.First(&removeMission, "id = ?", retrievedMission.ID).Error; err != nil {
		t.Fatalf("Failed to retrieve mission: %v", err)
	}

	// Delete mission
	if err := db.Delete(&removeMission).Error; err != nil {
		t.Fatalf("Failed to delete mission: %v", err)
	}

	// Ensure mission is deleted
	var deletedMission Mission
	err := db.First(&deletedMission, "codename = ?", "TestMission").Error
	if !errors.Is(err, gorm.ErrRecordNotFound) {
		t.Fatalf("Mission is not deleted as expected: %v", err)
	}

}

// Test CRUD operations for System
func TestSystemCRUD(t *testing.T) {
	db := InitTestDB(DBTestFile)

	// Create a new system

	system := System{
		Galaxy:       "Euclid",
		Region:       NewNullString("Alpha"),
		System:       NewNullString("System 1"),
		Civilization: NewNullString("Gek"),
		StarColor:    NewNullInt16(StarYellow.Int16()),
		BlackHole:    false,
		Atlas:        true,
		Outlaw:       false,
	}
	if db == nil {
		t.Fatalf("Database connection is nil")
	}
	// Create system
	if err := db.Create(&system).Error; err != nil {
		t.Fatalf("Failed to create system: %v", err)
	}

	// Retrieve system
	var retrievedSystem System
	if err := db.First(&retrievedSystem, "galaxy = ?", "Euclid").Error; err != nil {
		t.Fatalf("Failed to retrieve system: %v", err)
	}

	// Check retrieved system fields
	if retrievedSystem.Galaxy != system.Galaxy {
		t.Errorf("Expected galaxy: %s, got: %s", system.Galaxy, retrievedSystem.Galaxy)
	}

	// You can continue checking other fields similarly

	// Update system
	retrievedSystem.Region = NewNullString("Beta")
	if err := db.Save(&retrievedSystem).Error; err != nil {
		t.Fatalf("Failed to update system: %v", err)
	}

	var removeSystem System
	if err := db.First(&removeSystem, "id = ?", retrievedSystem.ID).Error; err != nil {
		t.Fatalf("Failed to retrieve system: %v", err)
	}

	// Delete system
	if err := db.Delete(&removeSystem).Error; err != nil {
		t.Fatalf("Failed to delete system: %v", err)
	}

	// Ensure system is deleted
	var deletedSystem System
	err := db.First(&deletedSystem, "galaxy = ?", "Euclid").Error
	if !errors.Is(err, gorm.ErrRecordNotFound) {
		t.Fatalf("System is not deleted as expected: %v", err)
	}

}

// Test CRUD operations for Planet
func TestPlanetCRUD(t *testing.T) {
	db := InitTestDB(DBTestFile)

	// Create a new planet

	planet := Planet{
		SystemID:     uuid.NewString(),
		Name:         "TestPlanet",
		Type:         NewNullString("Lush"),
		Alias:        NewNullString("Paradise"),
		PortalCoords: []int8{1, 2, 3, 4, 5, 6},
		Resources:    []string{"Resource 1", "Resource 2"},
		Ecosystem:    []string{"Eco 1", "Eco 2"},
		Description:  "Test description",
		Dissonant:    false,
		Media:        []string{"media1.jpg", "media2.jpg"},
	}
	if db == nil {
		t.Fatalf("Database connection is nil")
	}
	// Create planet
	if err := db.Create(&planet).Error; err != nil {
		t.Fatalf("Failed to create planet: %v", err)
	}

	// Retrieve planet
	var retrievedPlanet Planet
	if err := db.First(&retrievedPlanet, "name = ?", "TestPlanet").Error; err != nil {
		t.Fatalf("Failed to retrieve planet: %v", err)
	}

	// Check retrieved planet fields
	if retrievedPlanet.Name != planet.Name {
		t.Errorf("Expected name: %s, got: %s", planet.Name, retrievedPlanet.Name)
	}

	// You can continue checking other fields similarly

	// Update planet
	retrievedPlanet.Description = "Updated description"
	if err := db.Save(&retrievedPlanet).Error; err != nil {
		t.Fatalf("Failed to update planet: %v", err)
	}

	var removePlanet Planet
	if err := db.First(&removePlanet, "id = ?", retrievedPlanet.ID).Error; err != nil {
		t.Fatalf("Failed to retrieve planet: %v", err)
	}

	// Delete planet
	if err := db.Delete(&removePlanet).Error; err != nil {
		t.Fatalf("Failed to delete planet: %v", err)
	}

	// Ensure planet is deleted
	var deletedPlanet Planet
	err := db.First(&deletedPlanet, "name = ?", "TestPlanet").Error
	if !errors.Is(err, gorm.ErrRecordNotFound) {
		t.Fatalf("Planet is not deleted as expected")
	}
}

// Test CRUD operations for MissionLogEntry
func TestMissionLogEntryCRUD(t *testing.T) {
	db := InitTestDB(DBTestFile)

	// Create a new mission log entry

	missionLogEntry := MissionLogEntry{
		MissionID: uuid.NewString(),
		Entry:     "Test entry",
		SystemID:  NewNullString(uuid.NewString()),
		PlanetID:  NewNullString(uuid.NewString()),
		BaseID:    NewNullString(uuid.NewString()),
		Media:     []string{"media1.jpg", "media2.jpg"},
	}
	if db == nil {
		t.Fatalf("Database connection is nil")
	}
	// Create mission log entry
	if err := db.Create(&missionLogEntry).Error; err != nil {
		t.Fatalf("Failed to create mission log entry: %v", err)
	}

	// Retrieve mission log entry
	var retrievedMissionLogEntry MissionLogEntry
	if err := db.First(&retrievedMissionLogEntry, "entry = ?", "Test entry").Error; err != nil {
		t.Fatalf("Failed to retrieve mission log entry: %v", err)
	}

	// Check retrieved mission log entry fields
	if retrievedMissionLogEntry.Entry != missionLogEntry.Entry {
		t.Errorf("Expected entry: %s, got: %s", missionLogEntry.Entry, retrievedMissionLogEntry.Entry)
	}

	// You can continue checking other fields similarly

	// Update mission log entry
	retrievedMissionLogEntry.Entry = "Updated entry"
	if err := db.Save(&retrievedMissionLogEntry).Error; err != nil {
		t.Fatalf("Failed to update mission log entry: %v", err)
	}

	var removeMissionLogEntry MissionLogEntry
	if err := db.First(&removeMissionLogEntry, "id = ?", retrievedMissionLogEntry.ID).Error; err != nil {
		t.Fatalf("Failed to retrieve mission log entry: %v", err)
	}

	// Delete mission log entry
	if err := db.Delete(&removeMissionLogEntry).Error; err != nil {
		t.Fatalf("Failed to delete mission log entry: %v", err)
	}

	// Ensure mission log entry is deleted
	var deletedMissionLogEntry MissionLogEntry
	err := db.First(&deletedMissionLogEntry, "entry = ?", "Updated entry").Error
	if !errors.Is(err, gorm.ErrRecordNotFound) {
		t.Fatalf("Mission log entry is not deleted as expected")
	}
}

// Test CRUD operations for Discovery
func TestDiscoveryCRUD(t *testing.T) {
	db := InitTestDB(DBTestFile)

	// Create a new discovery
	discovery := Discovery{
		SystemID:    NewNullString(uuid.NewString()),
		PlanetID:    NewNullString(uuid.NewString()),
		Description: "Test description",
		Wonder:      false,
		Media:       []string{"media1.jpg", "media2.jpg"},
	}
	if db == nil {
		t.Fatalf("Database connection is nil")
	}
	// Create discovery
	if err := db.Create(&discovery).Error; err != nil {
		t.Fatalf("Failed to create discovery: %v", err)
	}

	// Retrieve discovery
	var retrievedDiscovery Discovery
	if err := db.First(&retrievedDiscovery, "description = ?", "Test description").Error; err != nil {
		t.Fatalf("Failed to retrieve discovery: %v", err)
	}

	// Check retrieved discovery fields
	if retrievedDiscovery.Description != discovery.Description {
		t.Errorf("Expected description: %s, got: %s", discovery.Description, retrievedDiscovery.Description)
	}

	// You can continue checking other fields similarly

	// Update discovery
	retrievedDiscovery.Description = "Updated description"
	if err := db.Save(&retrievedDiscovery).Error; err != nil {
		t.Fatalf("Failed to update discovery: %v", err)
	}

	var removeDiscovery Discovery
	if err := db.First(&removeDiscovery, "id = ?", retrievedDiscovery.ID).Error; err != nil {
		t.Fatalf("Failed to retrieve discovery: %v", err)
	}

	// Delete discovery
	if err := db.Delete(&removeDiscovery).Error; err != nil {
		t.Fatalf("Failed to delete discovery: %v", err)
	}

	// Ensure discovery is deleted
	var deletedDiscovery Discovery
	err := db.First(&deletedDiscovery, "description = ?", "Updated description").Error
	if !errors.Is(err, gorm.ErrRecordNotFound) {
		t.Fatalf("Discovery is not deleted as expected")
	}
}
