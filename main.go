package main

import (
	"nmscommand/model"

	log "github.com/sirupsen/logrus"
)

func main() {

	model.SetupDBDriver()

	db := model.InitTestDB()

	db.AutoMigrate(&model.Mission{}, &model.System{}, &model.Planet{},
		&model.MissionLogEntry{}, &model.Discovery{}, &model.Base{})

	mission := &model.Mission{Codename: "test"}
	db.Create(mission)
	log.Info(mission)

}
