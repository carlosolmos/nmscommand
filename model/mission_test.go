package model

import (
	"database/sql"
	"errors"
	"testing"
	"time"

	"github.com/google/uuid"
	sqliteGo "github.com/mattn/go-sqlite3"
	log "github.com/sirupsen/logrus"
	"gorm.io/driver/sqlite"
	"gorm.io/gorm"
	"gorm.io/gorm/logger"
)

var (
	err error
)

func InitTestDB() *gorm.DB {
	// Setup test database
	const CustomDriverName = "sqlite3_extended"
	const File = "file:./foo.db?cache=shared&mode=memory"
	sql.Register(CustomDriverName,
		&sqliteGo.SQLiteDriver{
			ConnectHook: func(conn *sqliteGo.SQLiteConn) error {
				err = conn.RegisterFunc(
					"gen_random_uuid",
					func(arguments ...interface{}) (string, error) {
						return uuid.NewString(), nil // Return a string value.
					},
					true,
				)
				return err
			},
		},
	)

	conn, err := sql.Open(CustomDriverName, File)
	if err != nil {
		panic(err)
	}

	db, err := gorm.Open(sqlite.Dialector{
		DriverName: CustomDriverName,
		DSN:        File,
		Conn:       conn,
	}, &gorm.Config{
		Logger:                   logger.Default.LogMode(logger.Info),
		SkipDefaultTransaction:   true,
		DisableNestedTransaction: true,
	})

	if err != nil {
		log.Fatal(err)
	}
	// Migrate the schema
	db.AutoMigrate(&Mission{}, &System{}, &Planet{},
		&MissionLogEntry{}, &Discovery{}, &Base{})

	return db

}

func TestMissionCRUD(t *testing.T) {
	db := InitTestDB()

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
