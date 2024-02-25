package model

import (
	"database/sql"

	"nmscommand/utils"

	"github.com/google/uuid"
	sqliteGo "github.com/mattn/go-sqlite3"
	log "github.com/sirupsen/logrus"
	"gorm.io/driver/sqlite"
	"gorm.io/gorm"
	"gorm.io/gorm/logger"
)

const (
	CustomDriverName = "sqlite3_extended"
	DBFile           = "file:./nmscommand.db"
	DBTestFile       = "file:./foo_test.db?cache=shared&mode=memory"
)

var DriverInitialized = false

func SetupDBDriver() {
	// Setup test database
	sql.Register(CustomDriverName,
		&sqliteGo.SQLiteDriver{
			ConnectHook: func(conn *sqliteGo.SQLiteConn) error {
				err := conn.RegisterFunc(
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
	DriverInitialized = true
}

func InitDB(dbFile string) *gorm.DB {
	if !DriverInitialized {
		SetupDBDriver()
	}
	conn, err := sql.Open(CustomDriverName, dbFile)
	if err != nil {
		panic(err)
	}
	gormConfig := gorm.Config{
		SkipDefaultTransaction:   true,
		DisableNestedTransaction: true,
	}
	if utils.GlobalDebug {
		gormConfig.Logger = logger.Default.LogMode(logger.Info)
	} else {
		gormConfig.Logger = logger.Default.LogMode(logger.Error)

	}
	db, err := gorm.Open(sqlite.Dialector{
		DriverName: CustomDriverName,
		DSN:        dbFile,
		Conn:       conn,
	}, &gormConfig)

	if err != nil {
		log.Fatal(err)
	}
	// Migrate the schema
	db.AutoMigrate(
		&Mission{},
		&System{},
		&Planet{},
		&MissionLogEntry{},
		&Discovery{},
		&Base{})

	return db

}

func NewNullString(s string) sql.NullString {
	return sql.NullString{String: s, Valid: true}
}

func NewNullInt16(i int16) sql.NullInt16 {
	return sql.NullInt16{Int16: i, Valid: true}
}
