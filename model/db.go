package model

import (
	"database/sql"

	"github.com/google/uuid"
	sqliteGo "github.com/mattn/go-sqlite3"
	log "github.com/sirupsen/logrus"
	"gorm.io/driver/sqlite"
	"gorm.io/gorm"
	"gorm.io/gorm/logger"
)

const (
	CustomDriverName = "sqlite3_extended"
	File             = "file:./foo.db?cache=shared&mode=memory"
)

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

}

func InitTestDB() *gorm.DB {
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
	db.AutoMigrate(
		&Mission{},
		&System{},
		&Planet{},
		&MissionLogEntry{},
		&Discovery{},
		&Base{})

	return db

}