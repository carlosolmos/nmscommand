package main

import (
	"database/sql"
	"nmscommand/model"

	"github.com/google/uuid"
	sqliteGo "github.com/mattn/go-sqlite3"
	log "github.com/sirupsen/logrus"
	"gorm.io/driver/sqlite"
	"gorm.io/gorm"
	"gorm.io/gorm/logger"
)

func main() {

	const CustomDriverName = "sqlite3_extended"
	const File = "./nmscommand.db"
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

	db.AutoMigrate(&model.Mission{}, &model.System{}, &model.Planet{},
		&model.MissionLogEntry{}, &model.Discovery{}, &model.Base{})

	mission := &model.Mission{Codename: "test"}
	db.Create(mission)
	log.Info(mission)

}
